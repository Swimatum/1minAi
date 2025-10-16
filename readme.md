# 1minAi — Streaming test client

This small project contains a simple streaming client to exercise the 1min.ai streaming endpoint. The primary runnable script is `fonctions_streaming.py`. Other files in the repository are for testing or development purposes.

## What this does
- Calls the 1min.ai streaming API and prints received chunks.
- Includes helpers to safely decode bytes and to pretty-print JSON chunks or raw text.

## Main file
- `fonctions_streaming.py`: a runnable script that posts to the streaming endpoint and prints the stream. It also exposes helper functions (`print_streaming`, `safe_decode`) that you can import from other scripts.

## Requirements
- Python 3.8+
- `requests` (required)
- `python-dotenv` (optional — if you want to load a `.env` file automatically)

You can install dependencies with:

```powershell
pip install -r requirements.txt
```

## API key (important)
The script reads the API key from the environment variable `ONE_MIN_AI_API_KEY`. Do NOT put your API key directly into source files or commit it to version control.

Examples (PowerShell):

- Temporarily for the current session:
```powershell
$env:ONE_MIN_AI_API_KEY = 'your_key_here'
python fonctions_streaming.py
```

- Persistently for your user (requires reopening your shell to take effect):
```powershell
setx ONE_MIN_AI_API_KEY 'your_key_here'
# then restart your terminal
python fonctions_streaming.py
```

- Using a `.env` file (optional):
1. Create a file named `.env` next to `fonctions_streaming.py` containing:
```
ONE_MIN_AI_API_KEY=your_key_here
```
2. Install `python-dotenv` and the script will load the `.env` automatically:
```powershell
pip install python-dotenv
python fonctions_streaming.py
```

## Usage / Importing helpers
- Run the script directly to perform a streaming call:
```powershell
python fonctions_streaming.py
```

- Or import helper functions in other code without triggering the network call:
```python
from fonctions_streaming import print_streaming, safe_decode
# Now you can call print_streaming(resp) in tests or other scripts
```

## Troubleshooting
- Missing API key: the script will raise an error explaining `ONE_MIN_AI_API_KEY` is not set.
- HTTP 500 from the API: that's a server-side error — try again later or contact the API provider.
- Network/timeouts: adjust the `timeout` argument in `call_streaming()` if needed.

## Security note
- Never commit your API keys. Use environment variables or a secure secrets manager.

---
Files in this repo other than `fonctions_streaming.py` are intended for testing or experimentation.

