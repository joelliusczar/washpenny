import sys
import subprocess
import re
import base64
import os
from typing import Iterator
from tempfile import NamedTemporaryFile


def scan_pems_file(certsFile: str):
	cert = b""
	lines = open(certsFile, "rb").readlines()
	for line in lines:
		line = line.rstrip(b"\n\r")
		if line == b"-----BEGIN CERTIFICATE-----":
			continue
		if line == b"-----END CERTIFICATE-----":
			cert = b"-----BEGIN CERTIFICATE-----\n" \
				+ cert \
				+ b"-----END CERTIFICATE-----"
			yield cert
			cert = b""
			continue
		cert += (line + b"\n")

def extract_subject_from_cert(cert: bytes):
	proc = subprocess.Popen([
			"openssl",
			"x509",
			"-subject"
		],
		stdin=subprocess.PIPE,
		stdout=subprocess.PIPE,
	)
	out, _ = proc.communicate(input=cert)
	return out.decode()

def extract_common_name_from_cert(cert: bytes):
	output = extract_subject_from_cert(cert)
	if match := re.match(r"CN *= *([^/\n]+)",output):
		return match.group(1)
	return ""

def cert_matches_common_name(cert: bytes, commonName: str):
	extracted_common_name = extract_common_name_from_cert(cert)
	return extracted_common_name == commonName

def extract_enddate_from_cert(cert: bytes):
	proc = subprocess.Popen([
			"openssl",
			"x509",
			"-enddate"
		],
		stdin=subprocess.PIPE,
		stdout=subprocess.PIPE,
	)
	out, _ = proc.communicate(input=cert)
	match = re.search(r"notAfter *= *([a-zA-Z0-9: ]+)", out.decode())
	if match:
		return match.group(1)
	return ""


def certs_matching_name(commonName: str) -> Iterator[bytes]:
	cert = b""
	line = sys.stdin.buffer.readline().rstrip(b"\n")
	while line:
		if line == b"-----BEGIN CERTIFICATE-----":
			line = sys.stdin.buffer.readline().rstrip(b"\n")
			continue
		if line == b"-----END CERTIFICATE-----":
			decoded = base64.b64decode(cert)
			#openssl is slow so check base64 decoded first
			if commonName.encode() in decoded:
				proc = subprocess.Popen([
						"openssl",
						"x509",
						"-subject"
					],
					stdin=subprocess.PIPE,
					stdout=subprocess.PIPE,
				)
				cert = b"-----BEGIN CERTIFICATE-----\n" \
					+ cert \
					+ b"-----END CERTIFICATE-----"
				res = proc.communicate(cert)
				output = res[0].decode()
				match = re.search(f"CN *= *({commonName})", output)
				if match:
					yield cert
			cert = b""
			line = sys.stdin.buffer.readline().rstrip(b"\n")
			continue
		cert += line + b"\n"
		line = sys.stdin.buffer.readline().rstrip(b"\n")

def is_cert_expired(cert: bytes) -> bool:
	proc = subprocess.Popen([
			"openssl",
			"x509",
			"-checkend",
			"3600",
			"-noout"
		],
		stdin=subprocess.PIPE,
		stdout=subprocess.DEVNULL,
		stderr=subprocess.DEVNULL
	)
	proc.communicate(input=cert)
	proc.wait(5)
	return proc.returncode == 1


def invalid_certs(commonName: str):
	for cert in certs_matching_name(commonName):
		if is_cert_expired(cert):
			yield cert

def valid_certs(commonName: str):
	for cert in certs_matching_name(commonName):
		if not is_cert_expired(cert) \
			and extract_subject_from_cert(cert) == commonName\
		:
			yield cert

def should_replace_cert(
	commonName: str,
	publicKeyFilePath: str,
	privateKeyFilePath: str
):
	if not os.path.exists(privateKeyFilePath):
		return True
	if not os.path.exists(publicKeyFilePath):
		return True
	certContent = open(publicKeyFilePath, "rb").read()
	if is_cert_expired(certContent):
		return True
	if not cert_matches_common_name(certContent, commonName):
		return True
	return False

def openssl_gen_cert(
	commonName: str,
	domain: str,
	publicKeyFilePath: str,
	privateKeyFilePath: str
):
	with NamedTemporaryFile("w") as tmp:
		tmp.write(open(os.environ["DSF_OPENSSL_DEFAULT_CONFIG"]).read())
		tmp.write(f"[SAN]\nsubjectAltName=DNS:{domain},IP:127.0.0.1")
		tmp.seek(0)
		proc = subprocess.Popen([
				"openssl", "req","-x509", "-sha256", "-new", "-nodes", "-newkey",
				"rsa:2048", "-days", "7",
				"-subj", f"/C=US/ST=CA/O=fake/CN={commonName}",
				"-reqexts", "SAN", "-extensions", "SAN",
				"-config", tmp.name, 
				"-keyout", privateKeyFilePath, "-out", publicKeyFilePath,
			],
		)
		proc.wait(5)
		if proc.returncode == 1:
			raise RuntimeError("Error while trying to create cert")

def setup_ssl_certs(commonName: str):
	pathPrefix = os.path.join(
		os.environ['DSF_SSH_DIR'],
		f"{os.environ['DSF_APP_NAME']}_localhost_local"
	)
	publicKeyFilePath = f"{pathPrefix}.public.key.crt"
	privateKeyFilePath = f"{pathPrefix}.private.key.pem"
	if not any(valid_certs(commonName)):
		openssl_gen_cert(
			commonName,
			commonName,
			publicKeyFilePath,
			privateKeyFilePath
		)
		return (publicKeyFilePath, privateKeyFilePath)
	return ("","")

def setup_ssl_cert_local_debug():
	pathPrefix = os.path.join(
		os.environ['DSF_SSH_DIR'],
		f"{os.environ['DSF_APP_NAME']}_localhost_debug",
		
	)
	publicKeyFilePath = f"{pathPrefix}.public.key.crt"
	privateKeyFilePath = f"{pathPrefix}.private.key.pem"
	openssl_gen_cert(
		f"{os.environ['DSF_APP_NAME']}-localhost",
		"localhost",
		publicKeyFilePath,
		privateKeyFilePath
	)
	return (publicKeyFilePath, privateKeyFilePath)


if __name__ == "__main__":
	commonName = sys.argv[2]
	if sys.argv[1] == "list-invalid":
		if any(invalid_certs(commonName)):
			print(commonName)
	if sys.argv[1] == "list-valid":
		if any(valid_certs(commonName)):
			print(commonName)
	elif sys.argv[1] == "debug":
		keys = setup_ssl_cert_local_debug()
		print(keys[0])
		print(keys[1])
	elif sys.argv[1] == "local":
		keys = setup_ssl_certs(commonName)
		print(keys[0])
		print(keys[1])
	elif sys.argv[1] == "check":
		if should_replace_cert(commonName, sys.argv[3], sys.argv[4]):
			print("true")
	else:
		sys.stderr.write(f"Invalid option selected\n {sys.argv[1]}")
