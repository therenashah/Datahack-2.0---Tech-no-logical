from PyPDF2 import PdfReader
import spacy
from collections import Counter

# Load the PDF file and extract text
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Tokenize the text into sentences using spaCy
def tokenize_text(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    return sentences

# Create a function for scoring sentences
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

# Generate the summary
def generate_summary(sentences, num_sentences=5):
    sentence_scores = score_sentences(sentences)
    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    summary = [sentence for sentence, _ in sorted_sentences[:num_sentences]]
    return ' '.join(summary)

# Main function
def main(pdf_docs, num_sentences=5):
    pdf_text = get_pdf_text(pdf_docs)
    sentences = tokenize_text(pdf_text)
    summary = generate_summary(sentences, num_sentences)
    return summary

# Example usage
if __name__ == "_main_":
    pdf_docs = [""]
    summary = main(pdf_docs, num_sentences=200)
    print(summary)