import json
import os
import sys
import urllib.request

def fetch_certs(
	app_url_base: str,
	public_key_path: str,
	private_key_path: str
):
	url = f"https://api.porkbun.com/api/json/v3/ssl/retrieve/{app_url_base}"

	data = {
		"apikey": os.environ["PB_API_KEY"],
		"secretapikey": os.environ["PB_SECRET"],
	}

	json_data = json.dumps(data).encode("utf-8")

	req = urllib.request.Request(
		url,
		data=json_data,
		headers={ "Content-Type": "application/json"},
		method="POST"
	)

	with urllib.request.urlopen(req) as response:
		result = json.loads(response.read().decode("utf-8"))
		with open(public_key_path, "w") as file:
			file.write(result["certificatechain"])
		with open(private_key_path, "w") as file:
			file.write(result["privatekey"])


if __name__ == "__main__":
	fetch_certs(sys.argv[1], sys.argv[2], sys.argv[3])