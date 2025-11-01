# 🗣️ NeuTTS Prof Voice — Long Text TTS

Turn long text into a natural, expressive voice using NeuTTS-Air. This small web app wraps the NeuTTS model so you can paste or load long text and synthesize speech fast.

![app screenshot](image.png)

---

## 🚀 Quick Start (2 minutes)

Prerequisites

- Python 3.10 or newer
- Git

Install dependencies

Open a PowerShell terminal in the project root and run:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Optional: create and activate a virtual environment

```powershell
# create venv and activate (PowerShell)
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the app

Start the web UI with:

```powershell
python launcher.py
```

The script prints a local URL (for example http://127.0.0.1:5000). Open it in your browser, paste or load a text file, and click the UI controls to generate audio.

Examples and files

- See the `examples/` folder for usage examples.
- The `samples/` folder contains example voices and text to test quickly.

Troubleshooting

- If a package is missing, make sure your environment is active and re-run `pip install -r requirements.txt`.
- If audio playback doesn't work in-browser, try downloading the generated file and play locally.

Contributing

Feel free to fork, improve docs/examples, and submit a pull request.

License

This project includes a `LICENSE` file — see it for usage terms.

---

Enjoy — paste long text and let NeuTTS bring it to life!
