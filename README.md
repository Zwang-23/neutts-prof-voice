# 🗣️ NeuTTS Prof Voice — Long Text TTS

Turn long text into a natural, expressive voice using NeuTTS-Air. This small web app wraps the NeuTTS model so you can paste or load long text and synthesize speech fast.

![app screenshot](image.png)

---

## 🚀 Quick Start

Prerequisites

- Python 3.10 or newer
- Git
1. **Clone Git Repo**

2. **Install `espeak` (required dependency)**

   Please refer to the following link for instructions on how to install `espeak`:

   https://github.com/espeak-ng/espeak-ng/blob/master/docs/guide.md

   ```bash
   # Mac OS
   brew install espeak

   # Ubuntu/Debian
   sudo apt install espeak

   # Windows install
   # via chocolatey (https://community.chocolatey.org/packages?page=1&prerelease=False&moderatorQueue=False&tags=espeak)
   choco install espeak-ng
   # via wingit
   winget install -e --id eSpeak-NG.eSpeak-NG
   # via msi (need to add to path or folow the "Windows users who installed via msi" below)
   # find the msi at https://github.com/espeak-ng/espeak-ng/releases
   ```

   Mac users may need to put the following lines at the top of the neutts.py file.

   ```python
   from phonemizer.backend.espeak.wrapper import EspeakWrapper
   _ESPEAK_LIBRARY = '/opt/homebrew/Cellar/espeak/1.48.04_1/lib/libespeak.1.1.48.dylib'  #use the Path to the library.
   EspeakWrapper.set_library(_ESPEAK_LIBRARY)
   ```

   Windows users who installed via msi / do not have their install on path need to run the following (see https://github.com/bootphon/phonemizer/issues/163)
   ```pwsh
   $env:PHONEMIZER_ESPEAK_LIBRARY = "c:\Program Files\eSpeak NG\libespeak-ng.dll"
   $env:PHONEMIZER_ESPEAK_PATH = "c:\Program Files\eSpeak NG"
   setx PHONEMIZER_ESPEAK_LIBRARY "c:\Program Files\eSpeak NG\libespeak-ng.dll"
   setx PHONEMIZER_ESPEAK_PATH "c:\Program Files\eSpeak NG"
   ```
3. **Install Python dependencies**

   The requirements file includes the dependencies needed to run the model with PyTorch.
   When using an ONNX decoder or a GGML model, some dependencies (such as PyTorch) are no longer required.

   The inference is compatible and tested on `python>=3.11`.

   ```bash
   pip install -r requirements.txt
   ```

## Running the Model

Start the web UI with:

```powershell
python launcher.py
```

The script prints a local URL (for example http://127.0.0.1:5001). Open it in your browser, paste or load a text file, and click the UI controls to generate audio.

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
