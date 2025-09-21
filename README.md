# 🌲Directory Tree Creator

A Python desktop app for generating nested folder/file structures from a text-based tree.Paste a directory tree (like the ones you see in GitHub READMEs), choose an output location, and the app builds the structure on disk—folders, empty files, and all.

* * *

## Features

* **Tree-style input** – Write or paste a directory tree with `├──` and `└──` characters.
* **Automatic parsing** – Detects folders vs. files based on slashes and extensions.
* **GUI** – Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for a clean dark interface.
* **Instant creation** – Creates all nested directories and placeholder files in seconds.

* * *

## Screenshot
<img width="1002" height="914" alt="image" src="https://github.com/user-attachments/assets/72d9db0f-c89c-4777-8716-a00cbd917e9d" />

* * *

## Example Input

    roject/
    ├── src/
    │   ├── main.py
    │   └── utils.py
    ├── assets/
    │   └── logo.png
    └── README.md

* * *

Installation

1. **Clone the repo**`git clone https://github.com/Cristography/DirectoryMaker.git ` 
  `cd DirectoryMaker`
2. **Install deendencies**`pip install -r requirements.txt`
3. **Run the app**`python main.py`
   
* * *

Usage

1. Launch the app.
2. Choose an output folder.
3. Paste or edit your tree structure in the text box.
4. Click **Create Directory Structure**.
5. Check the output folder for your new project skeleton.
  
* * *

Requirements
* Python 3.8 or newer
* [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
  

* * *

License
MIT License
