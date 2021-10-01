# Import libraries
from PyPDF2 import PdfFileMerger
import pytesseract
import os
from pathlib import Path
import subprocess
import shutil
import glob

def func(file, lang_n):
    languages = ['eng', 'rus', 'deu', 'spa', 'jpn', 'ita', 'fra', 'ces', 'chi_sim']
    base_dir = Path(__file__).resolve().parent
    lang = languages[int(lang_n)]

    shutil.rmtree(os.path.join(base_dir, 'output_pdfs'))
    os.makedirs(os.path.join(base_dir, 'output_pdfs'))

    # Path of the pdf + folder
    PDF_file = os.path.join(base_dir, "input_pdfs", file)
    folder = os.path.join(base_dir, f'{file[:-4]}')
    os.makedirs(folder)
    '''
    Part #1 : Converting PDF to images
    '''
    PDFTOPPMPATH = os.path.join(base_dir, "poppler-0.67.0", "bin", "pdftoppm.exe")

    p = subprocess.Popen('"%s" -jpeg "%s" "%s"' % (PDFTOPPMPATH, PDF_file, folder +'/png'))

    # need to calculate sleep time for dif sizes
    p.wait()
    # Store all the png pages of the PDF in a variable
    png_pages = [os.path.join(base_dir, folder, file) for file in os.listdir(os.path.join(base_dir, folder)) if file.endswith(".jpg")]
    '''
    Part #2 - Recognizing text from the images using OCR + converting it to pdf
    '''
    pytesseract.pytesseract.tesseract_cmd = os.path.join(base_dir, 'Tesseract-OCR/tesseract.exe')
    for i in png_pages:
        pdf = pytesseract.image_to_pdf_or_hocr(i, extension='pdf', lang=lang)
        with open(os.path.join(base_dir, folder, f"{i[:-4]}.pdf"), 'w+b') as f:
            f.write(pdf)  # pdf type is bytes by default
    """
    literally merger
    """
    txt_files = [os.path.join(base_dir, folder, file) for file in os.listdir(os.path.join(base_dir, folder)) if file.endswith(".pdf")]

    merger = PdfFileMerger()

    for pdf in txt_files:
        merger.append(pdf)

    merger.write(os.path.join(base_dir, 'output_pdfs', f'{file[:-4]}_ocred.pdf'))
    merger.close()
    # + deleter
    shutil.rmtree(folder)

    return os.path.join(base_dir, 'output_pdfs', f'{file[:-4]}_ocred.pdf')
