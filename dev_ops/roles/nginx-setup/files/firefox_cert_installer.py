import sys
import os
import re
import json

def create_firefox_cert_policy_file(
	publicKeyFilePath: str,
	policyFile: str
):
	pemFile = re.sub(r"\.crt",".pem", publicKeyFilePath)
	content = f'''
			{{
				"policies": {{
					"Certificates": {{
						"ImportEnterpriseRoots": true,
						"Install": [
							"{publicKeyFilePath}",
							"/etc/ssl/certs/{pemFile}"
						]
					}}
				}}
			}}
	'''
	open(policyFile).write(content)

def load_trusted_by_firefox_json_with_added_cert(
	publicKeyFilePath: str,
	policyContent: str
):
	config = json.loads(policyContent)
	installed = config["policies"]["Certificates"]["Install"]
	if publicKeyFilePath not in installed:
		installed.append(publicKeyFilePath)
	pemFile = re.sub(r"\.crt",".pem", publicKeyFilePath)
	if f"/etc/ssl/certs/{pemFile}" not in installed:
		installed.append(f"/etc/ssl/certs/{pemFile}")
	return json.dumps(config)


def introduce_public_key(publicKeyFilePath: str):
	policyFilePath="/usr/share/firefox-esr/distribution/policies.json"
	if re.match(r"[#\"'\\*]", publicKeyFilePath):
		raise RuntimeError(f"{publicKeyFilePath} contains illegal characters")
	if os.path.exists(policyFilePath):
		content = load_trusted_by_firefox_json_with_added_cert(
			publicKeyFilePath,
			open(policyFilePath).read()
		)
		open(policyFilePath, "w").write(content)
	else:
		create_firefox_cert_policy_file(publicKeyFilePath, policyFilePath)

if __name__ == "__main__":
	publicKeyPath = sys.argv[1]

	introduce_public_key(publicKeyPath)