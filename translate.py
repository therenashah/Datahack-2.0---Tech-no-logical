from PyPDF2 import PdfReader
from deep_translator import GoogleTranslator
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Input PDF file path
input_pdf_path = '/Users/malharbonde/Desktop/nlp pdfs/AFFAIRE JALOUD c. PAYS-BAS.pdf'
output_pdf_path = 'translatedPdf3.pdf'  # Output PDF file path

# Initialize PDF reader
pdf_reader = PdfReader(open(input_pdf_path, 'rb'))

# Create a translator instance
translator = GoogleTranslator(source='auto', target='en')

# Define the font for Unicode characters (Türkçe characters)
pdfmetrics.registerFont(TTFont('ArialUnicode', 'arial.ttf'))

# Initialize the list of translated paragraphs
translated_paragraphs = []

# Iterate through each page of the input PDF
for page_number in range(len(pdf_reader.pages)):
    # Get the page
    page = pdf_reader.pages[page_number]

    # Extract text from the page
    text = page.extract_text()

    # Translate the text to English
    translated_text = translator.translate(text)

    # Create a Paragraph with translated text
    translated_paragraph = Paragraph(translated_text, getSampleStyleSheet()['Normal'])
    # translated_paragraph.paragraphStyle.alignment = 1  # Center alignment
    # translated_paragraph.paragraphStyle.fontName = 'ArialUnicode'

    translated_paragraphs.append(translated_paragraph)

# Create the PDF document
doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)
doc.build(translated_paragraphs)