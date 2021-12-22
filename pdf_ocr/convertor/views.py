from django.shortcuts import render
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes
from django.core.files.storage import FileSystemStorage
from convertor.pdf_ocr_progs.pdf_text_extractor import func
import os
from pathlib import Path

base_dir = Path(__file__).resolve().parent
filename = ''
i = 0
# Create your views here.
def home(request):
    """Функция с главной страничкой, куда можно загрузить файл, выбрать язык
    и скачать проокээриный пдф файл

    Parameters
    ----------
    request: dict, required
        содержит сообщение о том, что нужно забрать файл, сам файл, выбранный язык
    return argument
    ----------
    render: func, required, used arguments(request, html_page, context):
        request: dict, stated
            содержит всю информацию о типе запроса
        html_page: file, stated
            просто штмл страничка
        context: dict, generated
            контекст для штмл странички
    """
    wrfe = 0
    norm = 0
    file = 0
    wtf_ar_doin = 0
    print(request.FILES)
    if request.method == 'POST' and len(request.FILES) == 0:
        wtf_ar_doin = 1
    elif request.method == 'POST' and request.FILES['file'].name.endswith('.pdf'):
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        if uploaded_file.name in (os.listdir(os.path.join(base_dir, 'pdf_ocr_progs', 'input_pdfs'))):
            global i
            uploaded_file.name = uploaded_file.name[:-4] + f'_{i}.pdf'
            i += 1
        fs.save(uploaded_file.name, uploaded_file)
        lang = request.POST['lang']
        file = func(uploaded_file.name, lang)
        global filename
        filename = uploaded_file.name[:-4] + '_ocred.pdf'
        fs.delete(uploaded_file.name)
    elif request.method == 'POST' and not(request.FILES['file'].name.endswith('.pdf')):
        wrfe = 1
    else:
        norm = 1

    context = {
        'wrfe': wrfe,
        'norm': norm,
        'file': file,
        'dude': wtf_ar_doin
    }
    return render(request, 'convertor/convertor.html', context)

def download(request):
    """Функция позволяющая загрузить созданный файл со страницы в браузере

    Parameters
    ----------
    request: dict, required
        содержит сообщение о том, что нужно забрать файл

    return argument
    ----------
    response: dict, generated
        содержит файл
    """
    filepath = os.path.join(base_dir, 'pdf_ocr_progs', 'output_pdfs', filename)
    ## часть отсюда https://stackoverflow.com/questions/36392510/django-download-a-file
    ## еще часть отсюда https://programtalk.com/
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(filepath, 'rb'), chunk_size),
                                     content_type=mimetypes.guess_type(filepath)[0])
    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = 'Attachement;filename=%s' % filename
    ##
    return response