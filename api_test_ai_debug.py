import requests
import json
import os

API_KEY = os.environ.get("ONE_MIN_AI_API_KEY")
if not API_KEY:
    raise RuntimeError("ONE_MIN_AI_API_KEY not set in environment")

URL_STREAM = "https://api.1min.ai/api/features?isStreaming=true"

headers = {
    "Content-Type": "application/json",
    "API-KEY": API_KEY,
    "Accept": "*/*",
}

data = {
    "type": "CHAT_WITH_AI",
    "model": "gpt-4o-mini",
    "metadata": {},
    "promptObject": {
        "prompt": "Receive me ?",
        "isMixed": False,
        "webSearch": True,
        "numOfSite": 1,
        "maxWord": 500
    }
}

def safe_decode(x):
    """Decode bytes to str, or return str unchanged."""
    if isinstance(x, bytes):
        return x.decode("utf-8", errors="replace")
    return x

def print_streaming(resp):
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        print("HTTP error (stream):", e)
        try:
            print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
        except Exception:
            print(resp.text)
        return

    print("Streaming response (chunks):\n---")
    reconstructed = []  # si tu veux reconstituer tout le texte
    # on met decode_unicode=False pour être sûr d'avoir des bytes parfois ; on décode nous-même
    for raw_line in resp.iter_lines(decode_unicode=False):
        if not raw_line:
            continue
        line = safe_decode(raw_line).strip()

        # gérer SSE "data: ..." si présent
        if line.startswith("data:"):
            payload = line[len("data:"):].strip()
        else:
            payload = line

        # tenter de parser JSON
        try:
            parsed = json.loads(payload)
            # si c'est un objet structuré contenant du texte, essaye d'extraire un champ commun
            # sinon affiche l'objet
            if isinstance(parsed, dict) and "text" in parsed:
                text = parsed["text"]
                print(text)
                reconstructed.append(text)
            else:
                print(json.dumps(parsed, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            # pas du JSON -> texte brut (morceau de la réponse)
            print(payload)
            reconstructed.append(payload)

    print("---\nStream ended.")
    # afficher la réponse reconstituée si besoin
    full = "".join(reconstructed).strip()
    if full:
        print("\n=== Reconstructed full response ===")
        print(full)
        print("=== end reconstructed ===\n")

def call_streaming():
    print("Calling streaming endpoint...")
    resp = requests.post(URL_STREAM, headers=headers, json=data, stream=True, timeout=300)
    print_streaming(resp)

if __name__ == "__main__":
    call_streaming()
