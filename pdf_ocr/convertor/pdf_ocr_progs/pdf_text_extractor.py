# Import libraries
from PyPDF2 import PdfFileMerger
import pytesseract
import os
from pathlib import Path
import subprocess
import shutil

def create_folders(base_dir, file):
    """Создает папки output_pdfs, input_pdfs, и папку folder в которой будут хранится картинки

    Parameters
    ----------
    file: str, required
        название изначального файла
    base_dir: str, stated
        базовая папка к которй присоединяются все пути

    return arguments
    ----------
    PDF_file: str, generated
        путь к пдф файлу
    folder: str, generated
        путь к папке в которую надо складывать картинки
    """
    shutil.rmtree(os.path.join(base_dir, 'output_pdfs'))
    os.makedirs(os.path.join(base_dir, 'output_pdfs'))

    # Path of the pdf + folder
    PDF_file = os.path.join(base_dir, "input_pdfs", file)
    folder = os.path.join(base_dir, f'{file[:-4]}')
    os.makedirs(folder)
    return PDF_file, folder

def convert_to_png(base_dir, PDF_file, folder):
    """берет пдф файл и разбивает его на картинки

    Parameters
    ----------
    base_dir: str, stated
        базовая папка к которй присоединяются все пути
    PDF_file: str, required
        путь к пдф файлу
    folder: str, required
        путь к папке в которую надо складывать картинки
    PDFTOPPMPATH: str, stated
        путь к попплеру
    return arguments
    ----------
    png_pages: list, generated
        список из путей к каждой картинке
    """
    PDFTOPPMPATH = os.path.join(base_dir, "poppler-0.67.0", "bin", "pdftoppm.exe")

    p = subprocess.Popen('"%s" -jpeg "%s" "%s"' % (PDFTOPPMPATH, PDF_file, folder + '/png'))

    # need to calculate sleep time for dif sizes
    p.wait()
    # Store all the png pages of the PDF in a variable
    png_pages = [os.path.join(base_dir, folder, file) for file in os.listdir(os.path.join(base_dir, folder)) if file.endswith(".jpg")]
    return png_pages

def ocr_png_to_pdf_and_merge_pdfs(base_dir, folder, png_pages, lang, file):
    """Берет список картинок и окээрит их по одной, после чего создает пдф файл
    создает пдф файл из картинки и полученного текста,
    потом объединяет все пдф странички в 1 файл и возвращает путь к нему

    Parameters
    ----------
    base_dir: str, stated
        базовая папка к которй присоединяются все пути
    folder: str, required
        путь к папке в которую надо складывать картинки
    png_pages: list, required
        список из путей к каждой картинке
    lang: str, required
        выбранный язык
    file: str, required
        название изначального файла

    return arguments
    ----------
    new_file: str, generated
        путь к созданному файлу
    """
    pytesseract.pytesseract.tesseract_cmd = os.path.join(base_dir, 'Tesseract-OCR/tesseract.exe')
    for i in png_pages:
        pdf = pytesseract.image_to_pdf_or_hocr(i, extension='pdf', lang=lang)
        with open(os.path.join(base_dir, folder, f"{i[:-4]}.pdf"), 'w+b') as f:
            f.write(pdf)  # pdf type is bytes by default
    """literally merger"""
    txt_files = [os.path.join(base_dir, folder, file) for file in os.listdir(os.path.join(base_dir, folder)) if
                 file.endswith(".pdf")]
    new_file = os.path.join(base_dir, 'output_pdfs', f'{file[:-4]}_ocred.pdf')
    merger = PdfFileMerger()

    for pdf in txt_files:
        merger.append(pdf)

    merger.write(new_file)
    merger.close()
    return new_file

def func(file, lang_n):
    """ Получает файл file в пдф формате, конвертирует каждую страницу в картинку,
    потом берет все получившиеся картинки png_imgs и окээрит каждую картинку,
    создает пдф к каждой картинки, и после соединяет их,
    удаляет созданные папки и возвращает путь до созданного файла

    Parameters
    ----------
    file: str, required
        название изначального файла
    lang_n: str, required
        номер выбранного языка
    base_dir: str, stated
        базовая папка к которй присоединяются все пути

    return arguments
    ----------
    new_file: str, generated
        путь к созданному файлу
    """
    languages = ['eng', 'rus', 'deu', 'spa', 'jpn', 'ita', 'fra', 'ces', 'chi_sim']
    base_dir = Path(__file__).resolve().parent
    lang = languages[int(lang_n)]
    '''Part #1 : Making folders'''
    PDF_file, folder = create_folders(base_dir, file)
    '''Part #2 : Converting PDF to images'''
    png_imgs = convert_to_png(base_dir, PDF_file, folder)
    '''Part #3 - Recognizing text from the images using OCR + converting it to pdf'''
    edited_file = ocr_png_to_pdf_and_merge_pdfs(base_dir, folder, png_imgs, lang, file)
    # + delete created folders
    shutil.rmtree(folder)

    return edited_file
