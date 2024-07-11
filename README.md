# OCR Invoices

OCR Invoices is a web-based application that leverages Optical Character Recognition (OCR) to extract and organize text from invoice images. This project is built using Flask, Python, and Tesseract OCR, providing an efficient solution for digitizing and managing invoice data.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Future Improvements](#future-improvements)
- [License](#license)
- [Acknowledgments](#acknowledgments)

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
