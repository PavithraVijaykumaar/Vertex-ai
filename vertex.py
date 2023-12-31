# -*- coding: utf-8 -*-
"""vertex.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12bLz_5KH6zncAeCjndtj9Uyd_w2vBCTR
"""

import streamlit as st
from PyPDF2 import PdfReader

import vertexai
from vertexai.preview.language_models import ChatModel, InputOutputTextPair

import vertexai, streamlit as st
from vertexai.preview.language_models import TextGenerationModel

# Initialize Vertex AI with the required variables
PROJECT_ID = 'prodoc-ai-project' # @param {type:"string"}
LOCATION = 'us-central1'  # @param {type:"string"}
vertexai.init(project=PROJECT_ID, location=LOCATION)


import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file):
    pdf_text = ""
    pdf_document = fitz.open("pdf", uploaded_file.read())

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        pdf_text += page.get_text()

    pdf_document.close()

    return pdf_text

# Streamlit app
def main():
    st.title('MedicoBot')
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file is not None:
        st.write("File uploaded!")

        # Extract text from the PDF using PdfReader
        pdf_text = extract_text_from_pdf(pdf_file)

        # Shorten the prompt and use GPT-3.5-turbo to summarize the text
        # You may need to adjust the length of pdf_text to fit within token limits
        pdf_text_shortened = pdf_text[:4000]  # Adjust the length as needed

        prompt = (
               f"You are PRODOC's medical report summarizer who accepts only medical reports:\n"
               f"{pdf_text_shortened}\n"
               f"Note: Please make sure the uploaded document is a medical report."
               f"If not, do not read the report.\n"
               f"After confirming it as a medical report, you will summarize the entire report with a detailed explanation with 150 words and provide a list of specialists to consult for further evaluation and treatment.\n"
               f"Finally, end the summarization by saying 'Thanks for using PRODOC's Chat Application' in a new line."
      )
    try:
            model = TextGenerationModel.from_pretrained("text-bison@001")
            response = model.predict(
                prompt,
                temperature=0.2,
                max_output_tokens=256,
                top_k=40,
                top_p=0.8,
            )

            st.success(response)
    except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

