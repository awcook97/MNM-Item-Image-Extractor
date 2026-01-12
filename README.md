# MNM Item Image Extractor

This project extracts text from Monsters & Memories-style item images using OCR, renames the image based on the item name, and writes a .txt file containing the extracted item data.

The title is read from the item’s top banner, while the body text is extracted from the item description area.

--------------------------------------------------

## PROJECT STRUCTURE
```
MNM Item Image Extractor
| .venv/                  (Python virtual environment – ignored by git)
| testimages/
|| *.ext                 (Images with their extension)
|| *.txt                 (OCR output files – ignored by git)
| ocr_rename_items.py     (Main application)
```
--------------------------------------------------

## REQUIREMENTS

- Python 3.10 or newer (3.11 recommended)
- Tesseract OCR installed
- Works on Linux and Windows

--------------------------------------------------

## INSTALL TESSERACT OCR

### LINUX (Debian / Ubuntu)
```
sudo apt update
sudo apt install tesseract-ocr
```
Verify installation:
```
tesseract --version
```
--------------------------------------------------

### WINDOWS

1. Download Tesseract from:
   https://github.com/UB-Mannheim/tesseract/wiki

2. Install using the default options.

3. If Tesseract is not found automatically, open ocr_rename_items.py and uncomment / edit this line if needed:
```
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```
--------------------------------------------------

## CREATE A VIRTUAL ENVIRONMENT

### LINUX / macOS
```
cd /path/to/MNM\ Item\ Image\ Extractor
python3 -m venv .venv
source .venv/bin/activate
```
### WINDOWS (PowerShell)
```
cd /path/to/MNM\ Item\ Image\ Extractor
python -m venv .venv
.venv\Scripts\Activate.ps1
```
If activation is blocked, run this once:
```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
--------------------------------------------------

## INSTALL PYTHON DEPENDENCIES

With the virtual environment activated:
```
pip install --upgrade pip
pip install pytesseract opencv-python numpy
```
--------------------------------------------------

PREPARE TEST IMAGES

Place item screenshots in:

testimages/

Supported formats:
png
jpg / jpeg
webp
bmp
tif / tiff

--------------------------------------------------

## RUN THE APPLICATION

From the project root:

### LINUX / macOS
```
python ocr_rename_items.py testimages
```
### WINDOWS
```
python ocr_rename_items.py testimages
```
--------------------------------------------------

## OUTPUT BEHAVIOR

For each image:

- The image is renamed to the detected item title
  Example:
  SANGREL_RING_OF_THE_STRIKER.png

- A matching text file is created:
  SANGREL_RING_OF_THE_STRIKER.txt

Example text file contents:
```
SANGREL RING OF THE STRIKER
MAGIC
Slot: FINGER
STR: +2 STA: +1
HP: +5
A simple ring worn by initiates of the Sangrel Fist.
Weight: 0.1 Size: SMALL
Class: ALL
Race: ALL
```
--------------------------------------------------

## NOTES

- All .txt files inside testimages/ are ignored by git
- The .venv directory is ignored by git
- OCR accuracy depends on image quality and banner layout
- Banner crop settings can be adjusted in ocr_rename_items.py if needed

--------------------------------------------------

Here is the **same content**, rewritten with **proper Markdown formatting** so it renders cleanly on GitHub and is easy to read and copy.

You can paste this directly into your README.

---

## Windows Setup (Step-by-Step)

This section walks through installing Python and running the project on **Windows**, starting from a clean system.

---

### 1. Install Python

1. Go to the official Python download page:
   [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)

2. Click **Download Python 3.x.x** (latest stable version).

3. Run the installer.

4. **Important:**
   ✔ Check **“Add Python to PATH”** at the bottom of the installer window.

5. Click **Install Now** and wait for installation to finish.

---

### 2. Verify Python Installation

Open **Command Prompt** or **PowerShell** and run:

```powershell
python --version
```

You should see output similar to:

```text
Python 3.11.x
```

If you do, Python is installed correctly.

---

### 3. Clone or Download the Project

Using Git:

```powershell
git clone <your-repo-url>
cd "MNM Item Image Extractor"
```

Or download the ZIP from GitHub, extract it, and open the project folder.

---

### Change Directory to the Project Folder

After extracting the ZIP file, you need to change into the project directory before running any commands.

#### Example (replace with your actual path)

```powershell
cd path\to\MNM Item Image Extractor
```

#### Common examples

If you extracted it to your **Downloads** folder:

```powershell
cd $HOME\Downloads\MNM Item Image Extractor
```

If you extracted it to your **Desktop**:

```powershell
cd $HOME\Desktop\MNM Item Image Extractor
```

You can confirm you’re in the correct directory by running:

```powershell
dir
```

You should see:

```text
testimages
ocr_rename_items.py
README.md
requirements.txt
```

---

### 4. Create a Virtual Environment

From inside the project folder:

```powershell
python -m venv .venv
```

---

### 5. Activate the Virtual Environment

In **PowerShell**:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this **once**:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Then activate again:

```powershell
.venv\Scripts\Activate.ps1
```

When activated, your prompt will show:

```text
(.venv)
```

---

### 6. Install Python Dependencies

With the virtual environment active:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 7. Install Tesseract OCR

1. Download the Windows installer from:
   [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

2. Install using the default options.

3. If Tesseract is not found automatically, open `ocr_rename_items.py` and set:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

(Uncomment the line if needed.)

---

### 8. Run the Application

1. Place test images in:

```text
testimages\images\
```

2. Run the script:

```powershell
python ocr_rename_items.py testimages
```

---

### 9. Verify Output

* Images will be renamed based on the detected item title.
* Matching `.txt` files will be created alongside the images.

---
