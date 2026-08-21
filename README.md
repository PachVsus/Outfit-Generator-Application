<div align="center">

# 👔 Outfit Generator Application

### Your wardrobe, remixed.

Organize your clothes, discover new combinations, and build outfits that match your style and the weather—all from a private Windows desktop app.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-2C5E8D)](https://docs.python.org/3/library/tkinter.html)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows&logoColor=white)](#installation)
[![License](https://img.shields.io/badge/License-Choose%20a%20license-lightgrey)](#license)

**No accounts · No cloud · No terminal required for installed users**

</div>

---

## ✨ Why Outfit Generator?

That great outfit may already be in your closet—you just have not combined it yet. Outfit Generator turns your wardrobe into a visual collection and creates fresh combinations in seconds.

- 📸 **Build a visual wardrobe** with clothing names, photos, colors, types, and styles
- 🎲 **Generate random outfits** from the clothes you actually own
- 🌦️ **Filter by style and weather** before generating a combination
- 🧥 **Manage every item** with built-in editing and deletion
- ⭐ **Save favorite outfits** and revisit them later
- 💾 **Keep everything persistent** between sessions
- 🔒 **Stay private by default**—your wardrobe remains on your computer

## 🪄 How It Works

1. Add clothing items and their photos to your wardrobe.
2. Choose a preferred style and weather condition.
3. Generate a random outfit from matching pieces.
4. Save combinations you want to wear again.

Supported clothing categories include **Shirts, Jackets, Pants, Underwear, Shoes, Watches, and Caps**.

## 📦 Installation

### Recommended: Windows installer

Download `OutfitGeneratorSetup.exe` from the repository's **Releases** page and open it.

The installer includes the application and its private Python runtime, creates convenient shortcuts, and adds a normal Windows uninstall entry. Your friends do **not** need to install Python, Pillow, or any other dependency.

> Windows SmartScreen may display an “Unknown publisher” message for unsigned community builds. Review the release source and checksum before continuing.

### Run from source

For developers or contributors:

```powershell
git clone <your-repository-url>
cd "Outfit Generator Application"
python -m pip install -r requirements.txt
python app.py
```

Python 3.10 or newer is recommended.

## 🗂️ Your Data

Wardrobe records, saved outfits, and uploaded photos are stored locally under:

```text
%LOCALAPPDATA%\Outfit Generator Application
```

This keeps personal wardrobe data separate from the installed program and allows it to survive application upgrades. The app does not require an account or upload wardrobe information to a server.

## 🧱 Project Structure

```text
Outfit Generator Application/
├── app.py                       # Application entry point
├── outfit_generator/
│   ├── constants.py             # Clothing, style, color, and weather options
│   ├── generator.py             # Outfit-selection logic
│   ├── storage.py               # Persistent JSON storage
│   └── ui.py                    # Tkinter windows and controls
├── tests/                       # Core persistence and generator tests
├── build/                       # Windows installer build scripts
└── requirements.txt             # Python dependencies
```

## 🧪 Development

Run the automated tests:

```powershell
python -m unittest discover -s tests -v
```

Build the self-contained Windows installer:

```powershell
powershell -ExecutionPolicy Bypass -File .\build\build_installer.ps1
```

The finished installer is written to `dist\OutfitGeneratorSetup.exe`.

## 🛣️ Roadmap

Ideas for future releases:

- 🔎 Wardrobe search and advanced filters
- 🖼️ Larger outfit previews and gallery layouts
- 📅 Outfit planning by day or occasion
- 📤 Outfit-card image export
- 🎨 Custom themes and expanded clothing categories

Have an idea? Open an issue and describe the outfit-planning workflow you would love to see.

## 🤝 Contributing

Contributions are welcome. Fork the repository, create a focused branch, include tests when practical, and open a pull request explaining the change.

Please keep personal wardrobe images and generated JSON data out of commits.

## 📄 License

No license has been selected yet. Add a `LICENSE` file before inviting public reuse or contributions. For an open-source release, the MIT License is a simple and popular option.

---

<div align="center">

Made for anyone who has ever looked at a full closet and thought, **“I have nothing to wear.”** ✨

</div>

