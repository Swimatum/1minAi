import requests
import json
import os

url = "https://api.1min.ai/api/features?isStreaming=true"
API_KEY = os.environ.get("ONE_MIN_AI_API_KEY")

headers = {
	"Content-Type": "application/json",
	"API-KEY": API_KEY,
}

data = {
"type": "CHAT_WITH_AI",
"model": "gpt-4o-mini",
"promptObject": {
"prompt": "Tell me about artificial intelligence",
"isMixed": False,
"webSearch": True,
"numOfSite": 1,
"maxWord": 500
}
}

response = requests.post(url, headers=headers, json=data, stream=True)


def _print_response(resp):
	"""Print an HTTP response neatly.

	- Prints HTTP errors if status is not 2xx
	- Pretty-prints JSON when possible
	- Falls back to text for other content types
	- Streams line-delimited responses (SSE/chunked)
	"""
	try:
		resp.raise_for_status()
	except requests.HTTPError as e:
		print("HTTP error:", e)
		print("Status code:", resp.status_code)
		# Try to show body for debugging
		try:
			print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
		except Exception:
			print(resp.text)
		return

	content_type = resp.headers.get("Content-Type", "").lower()

	# JSON response (most common for APIs)
	if "application/json" in content_type or content_type.endswith("+json"):
		try:
			parsed = resp.json()
			print(json.dumps(parsed, indent=2, ensure_ascii=False))
		except ValueError:
			# Invalid JSON fallback
			print(resp.text)
		return

	# Streaming / event-stream or chunked transfer
	if "text/event-stream" in content_type or resp.headers.get("Transfer-Encoding", "").lower() == "chunked":
		print("Streaming response (line chunks):")
		for line in resp.iter_lines(decode_unicode=True):
			if line:
				print(line)
		return

	# Default: print text
	print(resp.text)


_print_response(response)
