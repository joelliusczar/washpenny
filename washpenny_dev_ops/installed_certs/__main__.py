import sys
import subprocess
import re
import base64
from typing import Iterator

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

if __name__ == "__main__":
	commonName = sys.argv[1]

	for cert in certs_matching_name(commonName):
		print(cert.decode())