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

## LICENSE

MIT