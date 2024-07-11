# OCR Invoices

OCR Invoices is a web-based application that leverages Optical Character Recognition (OCR) to extract and organize text from invoice images. This project is built using Flask, Python, and Tesseract OCR, providing an efficient solution for digitizing and managing invoice data.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Future Improvements](#future-improvements)

## Features

- **Image Upload**: Upload single images or entire folders of invoice images.
- **Image Cropping**: Option to crop images before processing.
- **Text Extraction**: Extracts text from images using Tesseract OCR.
- **Data Parsing**: Identifies and structures key invoice information:
  - Tax Office and Tax Number
  - Date and Time
  - Total KDV (VAT) and Total Amount
  - Individual product details including names, quantities, prices, KDV rates, and KDV amounts
- **Error Handling**: Manages unreadable text or unrecognized formats.
- **User-Friendly Interface**: Built with Bootstrap for a clean and responsive design.

## Technologies Used

- **Python**: Core programming language for the backend.
- **Flask**: Web framework for building the application.
- **Tesseract OCR**: Optical character recognition engine.
- **HTML/CSS/JavaScript**: Frontend technologies for building the user interface.
- **Cropper.js**: JavaScript library for image cropping.
- **FuzzyWuzzy**: Library for fuzzy string matching, enhancing text extraction accuracy.

## Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/your-username/ocr-invoices.git
   cd ocr-invoices

2. **Ensure Tesseract OCR is installed**:

Download and install Tesseract OCR from [here](https://github.com/tesseract-ocr/tesseract).
Update the tesseract_cmd.py file with the correct path to the Tesseract executable.

3. **Run the Application**:
   ```sh
python app.py

## Usage
**Home Page**:

The home page allows users to upload single images or folders of images.
Optionally, users can crop images before uploading.

**Upload Image**:

Choose an image file and click "Upload Image".
The application will process the image and display the extracted and parsed information.

**Upload Folder**:

Choose a folder containing multiple images and click "Upload Folder".
The application will process each image in the folder and display the extracted information for all images.


## Screenshots

![image](https://github.com/CanBulutCoding/OCR-Website-specialized-for-invoices/assets/127326150/b348183c-5f75-42e3-9da6-f643952afade)
![image](https://github.com/CanBulutCoding/OCR-Website-specialized-for-invoices/assets/127326150/1cd15f30-a1dc-4a2e-9935-0daf7d8257f7)
![image](https://github.com/CanBulutCoding/OCR-Website-specialized-for-invoices/assets/127326150/dac9b6bb-de8d-45ca-b61d-26e29480362b)
![image](https://github.com/CanBulutCoding/OCR-Website-specialized-for-invoices/assets/127326150/0d684d0a-18f1-4e21-8878-bc21b3ed559a)
![image](https://github.com/CanBulutCoding/OCR-Website-specialized-for-invoices/assets/127326150/de184768-0df1-4288-b021-1fc631399896)

## Future Improvements
- Enhancing OCR and data parsing accuracy.
- Adding support for more invoice formats.
- Implementing user authentication for secure access.
- Improving handling of different languages and character sets.





