# Sandbox Calculator

A small Windows desktop calculator for basic arithmetic — built with Python 3.13 and tkinter,
packaged as a standalone `.exe` with PyInstaller and an installer with Inno Setup.

**[Download the installer →](https://github.com/MintChocoDino/Calculator/releases/latest)**
&nbsp;·&nbsp;
**[Project page →](https://mintchocodino.github.io/Calculator/)**

<p align="center">
  <img src="assets/calculator.png" width="120" alt="Sandbox Calculator icon">
</p>

## Features

- Add, subtract, multiply, divide — evaluated left to right
- Percent and sign toggle (`±`), backspace, clear
- Full keyboard control: digits, operators, <kbd>Enter</kbd> to equal,
  <kbd>Backspace</kbd> to delete, <kbd>Esc</kbd> to clear
- Resizes cleanly — the keypad scales with the window
- Sane number formatting: `0.1 + 0.2` displays `0.3`, and dividing by zero
  says so instead of crashing

## Running from source

Requires Python 3.13+ (tkinter ships with the standard Windows installer).

```bash
python calculator.py
```

No third-party packages are needed to run the app — only to build it.

## Repository layout

| Path | What it is |
| --- | --- |
| `calculator.py` | The entire application |
| `index.html` | Project/download page (served via GitHub Pages) |
| `assets/calculator.ico` `.png` | App icon, generated from the app's palette |
| `build/make_icon.py` | Regenerates the icon (requires Pillow) |
| `build/installer.iss` | Inno Setup script for the installer |

Build output lands in `dist/` and is not committed — released binaries are
attached to the [GitHub Releases](https://github.com/MintChocoDino/Calculator/releases) page.

## Building the binaries

```bash
pip install pyinstaller pillow

# 1. icon
python build/make_icon.py

# 2. standalone executable -> dist/SandboxCalculator.exe
python -m PyInstaller --noconfirm --clean --onefile --windowed \
  --name SandboxCalculator \
  --icon "$PWD/assets/calculator.ico" \
  --distpath dist --workpath build/pyinstaller --specpath build \
  calculator.py

# 3. installer -> dist/SandboxCalculator-1.0.0-Setup.exe
"$LOCALAPPDATA/Programs/Inno Setup 6/ISCC.exe" build/installer.iss
```

The installer is configured with `PrivilegesRequired=lowest`, so it installs
per-user and never triggers an administrator prompt.

## Notes

The released binaries are **not code-signed**, so Windows SmartScreen will warn on
first run — choose *More info → Run anyway*. SHA-256 checksums for each build are
listed on the [project page](https://mintchocodino.github.io/Calculator/) and in the
release notes.
