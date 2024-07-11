# OCR-Website-specialized-for-invoices
This project is an Optical Character Recognition (OCR) application designed to scan and extract text from invoice images, converting them into a structured format for easy reading and analysis.

Project Overview
The OCR Invoices project leverages the power of Tesseract OCR, Python, and Flask to create a web-based platform that allows users to upload images of invoices. The application processes these images to extract key information such as tax office names, tax numbers, dates, times, total amounts, and individual product details with their respective KDV (VAT) values.

Features
Image Upload: Users can upload single images or entire folders of invoice images.
Image Cropping: Users have the option to crop images before processing to focus on specific areas.
Text Extraction: The application uses Tesseract OCR to extract text from the uploaded images.
Data Parsing: Extracted text is parsed to identify and structure key invoice information including:
Tax Office and Tax Number
Date and Time
Total KDV (VAT) and Total Amount
Individual product names, quantities, prices, KDV rates, and KDV amounts
Error Handling: The application includes robust error handling to manage unreadable text or unrecognized formats.
User-Friendly Interface: Built with Bootstrap for a clean and responsive user interface.
Technologies Used
Python: Core programming language for the backend.
Flask: Web framework for building the application.
Tesseract OCR: Optical character recognition engine.
HTML/CSS/JavaScript: Frontend technologies for building the user interface.
Cropper.js: JavaScript library for image cropping.
FuzzyWuzzy: Library for fuzzy string matching, used to improve the accuracy of text extraction.
