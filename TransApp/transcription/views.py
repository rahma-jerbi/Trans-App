from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.http import HttpResponse

from django.conf import settings
from .models import Transcription
import requests
from fpdf import FPDF
import spacy
import fitz
import os
from django.contrib.auth.decorators import login_required

# Fonction pour appeler l'API FastAPI pour la transcription
def transcribe_audio_with_fastapi(audio_file):
    url = 'http://127.0.0.1:8000/transcribe/'  # Remplacez ceci par l'URL de votre API FastAPI
    files = {'audio_file': audio_file}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        return response.json().get('transcription')
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

@login_required
def transcriptions(request):
    message = ''
    pdf_file_url = ''
    if request.method == 'POST':
        audio_file = request.FILES.get('audio_file')
        if audio_file:
            try:
                # Appeler l'API FastAPI pour la transcription
                transcribed_text = transcribe_audio_with_fastapi(audio_file)
                
                # Générer le PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(200, 10, txt=transcribed_text)
                
                transcription_instance = Transcription.objects.create(audio_file=audio_file, transcribed_text=transcribed_text)
                pdf_file_name = f"transcription_{transcription_instance.id}.pdf"
                pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'pdf_files', pdf_file_name)
                pdf.output(pdf_file_path)
                transcription_instance.pdf_file.save(pdf_file_name, ContentFile(open(pdf_file_path, 'rb').read()))
                pdf_file_url = os.path.join(settings.MEDIA_URL, 'pdf_files', pdf_file_name)
                
                message = 'Transcription done successfully! Your PDF file is ready for download.'
            except Exception as e:
                message = f'Transcription failed: {e}'
    return render(request, 'transcription/transcriptions.html', {'message': message, 'pdf_file_url': pdf_file_url})

@login_required
def extract_informations(request):
    message = ''
    results = {}
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')
        keywords = request.POST.get('keywords').split(',')
        if pdf_file:
            try:
                pdf_path = save_uploaded_file_temporarily(pdf_file)
                results = extract_paragraphs_with_keywords_and_context(pdf_path, keywords)
                message = 'Extraction done successfully!'
            except Exception as e:
                message = f'Extraction failed: {e}'
    return render(request, 'transcription/extract_informations.html', {'message': message, 'results': results})

def save_uploaded_file_temporarily(file):
    temp_path = f'/tmp/{file.name}'
    with open(temp_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return temp_path

def extract_paragraphs_with_keywords_and_context(pdf_path, keywords):
    relevant_paragraphs = {keyword: [] for keyword in keywords}

    nlp = spacy.load("en_core_web_sm")
    nlp = spacy.load("fr_core_news_sm")

    with fitz.open(pdf_path) as pdf_document:
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            text = page.get_text()

            doc = nlp(text)

            current_paragraph = ""
            for sent in doc.sents:
                current_paragraph += sent.text + " "
                for keyword in keywords:
                    if keyword.lower() in sent.text.lower():
                        relevant_paragraphs[keyword].append(current_paragraph.strip())
                        current_paragraph = ""

    return relevant_paragraphs
