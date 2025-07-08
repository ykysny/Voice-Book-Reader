# Voice Book Reader (Digital Narrator)

![CI](https://github.com/ykysny/Voice-Book-Reader/actions/workflows/tests.yml/badge.svg)

**Voice Book Reader** is a simple graphical text-to-speech (TTS) application that reads books aloud.

It provides a user-friendly GUI (built with PySide6/Qt) for the high-quality [Silero TTS models](https://github.com/snakers4/silero-models). While minimal in design, the app requires significant storage due to dependencies like PyTorch.

https://github.com/ykysny/Voice-Book-Reader/assets/174832664/f53cf66e-29cd-44ae-b385-3feff8c7b5c3

---

## Features

- Read multiple books simultaneously — the app remembers the last sentence and speaker for each one.
- Supported languages: English (default) and Russian.
- Easy to extend: add new languages, swap TTS models, or customize preprocessing.
- Supports both dark and light themes.

---

## Installation

1. **Create a virtual environment:**
   ```bash
   python3 -m venv path_to_virenv_folder
   ```

2. **Activate the virtual environment:**
   ```bash
   source path_to_virenv_folder/bin/activate
   ```

3. **Install dependencies:**

   - **Option 1: Install manually**
     ```bash
     pip install sounddevice nltk num2words numpy pyside6 torch torchaudio
     ```

   - **Option 2: Install from `requirements.txt`**
     ```bash
     pip install -r requirements.txt
     ```

4. **Place the** `src` **folder into** `path_to_virenv_folder/workspace`.

---

## Usage

1. **Activate the virtual environment:**
   ```bash
   source path_to_virenv_folder/bin/activate
   ```

2. **Run the app:**
   ```bash
   cd path_to_virenv_folder/workspace
   python -m src.main
   ```

---

### Optional: Desktop Shortcut for GNU/Linux

A ready-to-use shortcut file, `VBR.desktop`, is included in the root of this project.

To use it:

1. Open the file and update the paths to match your environment (`path_to_virenv_folder`).
2. *(Optional)* If your system requires it, make the file executable:
   ```bash
   chmod +x VBR.desktop
   ```

---

## Details

- Tested on GNU/Linux (Linux Mint).
- Books must be placed in the `books` folder.
- Only `.txt` files are supported.
- When a book is removed from the `books` folder, its saved settings are also deleted.
- The `book_samples` folder contains classic books in the public domain, available for free.
- The `languages` folder contains files for the English and Russian versions.
- The `nltk_data` folder is required for text preprocessing with the NLTK library.
- The Russian TTS model `v4_ru.pt` is faster than `v3_1_ru.pt`, but has lower audio quality.
- The total size of the virtual environment is approximately **6.2 GB** (PyTorch accounts for around 5 GB).
- You can download TTS models here:  
  - [English: v3_en.pt](https://models.silero.ai/models/tts/en/v3_en.pt)  
  - [Russian: v4_ru.pt](https://models.silero.ai/models/tts/ru/v4_ru.pt)  
  - [Russian: v3_1_ru.pt](https://models.silero.ai/models/tts/ru/v3_1_ru.pt)

---

## Switching the App to Russian

Copy and overwrite the files from:

```bash
languages/Russian/
```

into:

```bash
workspace/src/core/
```

---

## Adding a New Language

To add a new language, modify `voice_engine.py` and `preprocessing.py`. Only 6 small export functions need to be updated.  
You can use your own TTS model or check available languages at the [Silero models project](https://github.com/snakers4/silero-models).

---

## Credits

Icon pack: [Qvadrons Icons by EpicCoders](https://icon-icons.com/pack/Qvadrons-Icons/789)

---
