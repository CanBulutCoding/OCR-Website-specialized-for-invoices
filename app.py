import logging
import os
import io
import base64
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
from fuzzywuzzy import fuzz, process
import re
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # Maximum file size: 16MB

# Loading tax office names from the text file
with open('vergidaireleri.txt', 'r', encoding='utf-8') as f:
    vergi_daireleri = [line.strip().upper() for line in f.readlines() if line.strip() and not line.startswith('Vergi Daireleri')]

def get_best_match(possible_names, reference_list, threshold=50):
    best_match = None
    highest_score = 0
    for name in possible_names:
        match, score = process.extractOne(name, reference_list, scorer=fuzz.token_sort_ratio)
        logging.debug(f"Matching '{name}' resulted in '{match}' with score {score}")
        if score > highest_score and score >= threshold:
            best_match = match
            highest_score = score
    return best_match

def extract_tax_office(text):
    lines = text.split('\n')
    tax_office = None
    tax_number = 'OKUNAMADI'
    
    tax_office_keywords = [
        r'VD', r'VERGİ DAİRESİ', r'VERGİ D\.', r'V\.D\.', r'VERGİ DAİRESI', r'VERGİ DAIRESI'
    ]
    
    for i, line in enumerate(lines):
        for keyword in tax_office_keywords:
            if re.search(keyword, line, re.IGNORECASE):
                current_line = line.strip()
                possible_names = []
                if i > 0:
                    previous_line = lines[i - 1].strip()
                    possible_names += previous_line.split()
                possible_names += current_line.split()
                
                # Checking the word right before the keyword
                keyword_pos = current_line.find(re.search(keyword, current_line, re.IGNORECASE).group())
                if keyword_pos > 0:
                    before_keyword = current_line[:keyword_pos].strip().split()[-1]
                    possible_names = [before_keyword] + possible_names
                
                best_match = get_best_match(possible_names, vergi_daireleri)
                if best_match:
                    tax_office = best_match
                    # Extracting the 10-digit tax number from the same line
                    tax_number_match = re.search(r'\b\d{10}\b', current_line)
                    if tax_number_match:
                        tax_number = tax_number_match.group()
                    break
        if tax_office:
            break
    
    return tax_office, tax_number

def extract_date(text):
    # Defining regex patterns for different date formats
    date_patterns = [
        r'\b\d{2}/\d{2}/\d{4}\b',  # Matches DD/MM/YYYY
        r'\b\d{2}-\d{2}-\d{4}\b',  # Matches DD-MM-YYYY
        r'\b\d{4}/\d{2}/\d{2}\b',  # Matches YYYY/MM/DD
        r'\b\d{4}-\d{2}-\d{2}\b'   # Matches YYYY-MM-DD
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            date_str = match.group()
            if validate_date(date_str):
                return date_str
            else:
                corrected_date_str = correct_date(date_str)
                if validate_date(corrected_date_str):
                    return corrected_date_str
    return 'OKUNAMADI'

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            return True
        except ValueError:
            try:
                datetime.strptime(date_str, "%Y/%m/%d")
                return True
            except ValueError:
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                    return True
                except ValueError:
                    return False

def correct_date(date_str):
    parts = re.split(r'[-/]', date_str)
    if len(parts) == 3:
        day, month, year = parts
        # Correcting common OCR misreading issues for the day part
        if int(day) > 31:
            tens_digit = int(day[0])
            units_digit = day[1]
            if tens_digit >= 4:
                tens_digit = min(range(4), key=lambda x: abs(x - 1))  # Closest to 1
            day = f'{tens_digit}{units_digit}'
        month = '01' if int(month) > 12 else month
        if len(year) == 2:
            year = '20' + year
        return f'{day}/{month}/{year}'
    return date_str

def extract_time(text):
    # Defining regex patterns for different time formats
    time_patterns = [
        r'\b\d{2}:\d{2}:\d{2}\b',  # Matches HH:MM:SS
        r'\b\d{2}:\d{2}\b'         # Matches HH:MM
    ]
    for pattern in time_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()
    return 'OKUNAMADI'

def extract_topkdv(text):
    # Defining regex pattern for TOPKDV
    topkdv_pattern = r'\bTOPKDV\s*[-~]*\s*\*?([\d\s,.]+)\b'
    match = re.search(topkdv_pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).replace(" ", "").replace(",", ".")
    return 'OKUNAMADI'

def extract_toplam(text):
    # Defining regex pattern for TOPLAM
    toplam_pattern = r'\bTOPLAM\s*[-~]*\s*\*?([\d\s,.]+)\b'
    match = re.search(toplam_pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).replace(" ", "").replace(",", ".")
    return 'OKUNAMADI'

def extract_products_kdv(text):
    # Defining regex pattern for extracting products and their prices
    product_pattern = re.compile(r'([A-ZÇĞİÖŞÜ\s]+)\s+X?(\d+)\s+\*?([\d\s,.]+)', re.IGNORECASE)
    products_kdv = []
    total_kdv = 0.0
    head_part_end = text.find('TOPKDV')
    if head_part_end == -1:
        return products_kdv, total_kdv

    head_part_text = text[:head_part_end]
    for match in product_pattern.findall(head_part_text):
        product_name, quantity, price = match
        product_name = product_name.strip()
        quantity = int(quantity)
        price = sanitize_price(price)

        # Determine KDV rate
        kdv_rate = 0.10  # Default KDV rate

        # Check for common misreading issues in KDV rate
        if quantity in [4, 7]:  # If the quantity is misread, it should be a percentage
            kdv_rate = int(f'{quantity}{str(price)[:2]}') / 100

        kdv_amount = price * kdv_rate
        products_kdv.append((product_name, quantity, price, kdv_rate, kdv_amount))
        total_kdv += kdv_amount

    return products_kdv, total_kdv

def sanitize_price(price_str):
    try:
        return float(price_str.replace(" ", "").replace(",", ".").strip())
    except ValueError:
        return 0.0

def process_image(image_path):
    try:
        img = Image.open(image_path).convert('L')  # Converting image to grayscale
        text = pytesseract.image_to_string(img).upper()  # Converting OCR output to uppercase for consistency
        tax_office, tax_number = extract_tax_office(text)
        tax_office = tax_office or 'OKUNAMADI'
        date = extract_date(text)
        time = extract_time(text)
        topkdv = extract_topkdv(text)
        toplam = extract_toplam(text)
        products_kdv, total_kdv = extract_products_kdv(text)
        return text, tax_office, tax_number, date, time, topkdv, toplam, products_kdv, total_kdv
    except Exception as e:
        raise RuntimeError(f'Failed to process image {image_path}: {str(e)}')

@app.route('/')
def index():
    logging.debug('Rendering Index Page')
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    logging.debug('Received Upload Request')
    try:
        cropped_data = request.form.get('cropped_data')
        if not cropped_data:
            flash('No file part')
            return redirect(request.url)
        
        # Decoding the base64 image data
        if "base64" in cropped_data:
            cropped_data = cropped_data.split(",")[1]
        img_data = base64.b64decode(cropped_data)
        img = Image.open(io.BytesIO(img_data))

        # Saving the image to a file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.png')
        img.save(file_path)

        # Processing the image
        text, tax_office, tax_number, date, time, topkdv, toplam, products_kdv, total_kdv = process_image(file_path)
        logging.debug('Image Processed')
        return render_template('result.html', text=text, tax_office=tax_office, tax_number=tax_number, date=date, time=time, topkdv=topkdv, toplam=toplam, products_kdv=products_kdv, total_kdv=total_kdv)
    except Exception as e:
        logging.error(f'An error occurred while processing the file: {str(e)}')
        flash(f'An error occurred while processing the file: {str(e)}')
        return redirect(url_for('index'))

@app.route('/upload_folder', methods=['POST'])
def upload_folder():
    logging.debug('Received Folder Upload Request')
    try:
        folder = request.files.getlist('folder')
        if not folder:
            flash('No folder part')
            return redirect(request.url)
        
        texts = []
        for file in folder:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                text, tax_office, tax_number, date, time, topkdv, toplam, products_kdv, total_kdv = process_image(file_path)
                texts.append((filename, text, tax_office, tax_number, date, time, topkdv, toplam, products_kdv, total_kdv))
            else:
                flash(f'File {file.filename} is not an allowed type')
        
        logging.debug('Folder Processed')
        return render_template('result_folder.html', texts=texts)
    except Exception as e:
        logging.error(f'An error occurred while processing the folder: {str(e)}')
        flash(f'An error occurred while processing the folder: {str(e)}')
        return redirect(url_for('index'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'jfif'}

if __name__ == '__main__':
    app.run(debug=True)
