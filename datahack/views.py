from . import views
from django.http import HttpResponse
from django.shortcuts import render
import spacy
from PyPDF2 import PdfReader, PdfWriter
from collections import Counter
from deep_translator import GoogleTranslator
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST



def index(request):
    return render(request, 'index.html')

def uploadhere(request):
    if request.method == 'POST':
        pdf_file = request.FILES['pdf_file']
        # Do something with the pdf_file
        return render(request, 'translator.html')
    else:
        return render(request, 'uploadhere.html')



def translator(request):
    if request.method == 'POST':
        # Get the uploaded PDF file from the form
        pdf_file = request.FILES['pdf_file']

        # Initialize PDF reader
        pdf_reader = PdfReader(pdf_file)
        
        # Create a translator instance
        translator = GoogleTranslator(source='auto', target='en')

        # Initialize the list of translated paragraphs
        translated_paragraphs = []

        # Iterate through each page of the input PDF
        for page_number in range(len(pdf_reader.pages)):
            # Get the page
            page = pdf_reader.pages[page_number]

            # Extract text from the page
            text = page.extract_text()
            print(text)
            # Translate the text to English
            translated_text = translator.translate(text)

            # Create a Paragraph with translated text
            translated_paragraph = Paragraph(translated_text, getSampleStyleSheet()['Normal'])

            translated_paragraphs.append(translated_paragraph)

        # Create the PDF document
        output_pdf_path = 'translatedPdf.pdf'
        doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)
        doc.build(translated_paragraphs)

        target_url = 'translator'
        response = HttpResponse(f"Translated pdf has been saved as translatedPdf.pdf")
        response['Refresh'] = f'10;url={target_url}'
        return render(request, 'translator.html')
    else:
        return render(request, 'translator.html')

def mydocs(request):
    return render(request, 'mydocs.html')

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def tokenize_text(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    return sentences

def score_sentences(sentences):
    word_frequencies = Counter()
    for sentence in sentences:
        for word in sentence.split():
            word_frequencies[word] += 1

    max_frequency = max(word_frequencies.values())

    sentence_scores = {}
    for sentence in sentences:
        for word in sentence.split():
            if word in word_frequencies:
                sentence_scores[sentence] = word_frequencies[word] / max_frequency

    return sentence_scores

def generate_summary(sentences, num_sentences=5):
    sentence_scores = score_sentences(sentences)
    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    summary = [sentence for sentence, _ in sorted_sentences[:num_sentences]]
    return ' '.join(summary)

def generate_summary(request):
    
    pdf_file = ['translatedPdf.pdf']
    num_sentences = 200  # Modify the number of sentences as needed

        # Process the PDF content
    pdf_text = get_pdf_text([pdf_file])
    sentences = tokenize_text(pdf_text)
    summary = generate_summary(sentences, num_sentences)
    return HttpResponse(summary, content_type='text/plain')

# def ajax_generate_summary(request):
#     if request.method == 'POST':
#         pdf_file = 'translatedPdf.pdf'  # The PDF file you want to summarize
#         num_sentences = 200  # Modify the number of sentences as needed

#         pdf_text = get_pdf_text([pdf_file])
#         sentences = tokenize_text(pdf_text)
#         summary = generate_summary(sentences, num_sentences)

#         return JsonResponse({'summary': summary})
#     else:
#         return JsonResponse({'error': 'Invalid request'}, status=400)