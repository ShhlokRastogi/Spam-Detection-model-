import streamlit as st
import joblib
import pandas as pd
import re
from collections import Counter
from PIL import Image
import pytesseract
import os
import tempfile
import PyPDF2

# Set Tesseract executable path (Adjust if different)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# === Load model, vectorizer, feature names ===
model_path = "data/models/model.pkl"
vectorizer_path = "data/models/vectorizer.pkl"
feature_names_path = "data/models/feature_names.pkl"

if not os.path.exists(model_path) or not os.path.exists(vectorizer_path) or not os.path.exists(feature_names_path):
    st.error("❌ Model, Vectorizer, or Feature Names not found. Please run your training script first.")
    st.stop()

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)
feature_names = joblib.load(feature_names_path)

# === Streamlit UI Setup ===
st.set_page_config(page_title="Spam Email Detector", layout="centered")
st.title("📧 Spam / Phishing Email Detector")
st.markdown("Detect whether an email is **spam** or **legit** using your trained XGBoost model.")

# === Input Method Selection ===
input_method = st.radio(
    "Choose input type:",
    ["✍️ Paste Email Text", "🖼️ Upload Screenshot (OCR)", "📄 Upload PDF File"]
)

email_text = ""  # Always define upfront

# === Text Input Method ===
if input_method == "✍️ Paste Email Text":
    email_text = st.text_area("Paste email content here:", height=200)

# === Screenshot OCR Method ===
elif input_method == "🖼️ Upload Screenshot (OCR)":
    image_file = st.file_uploader("Upload screenshot", type=["png", "jpg", "jpeg"])
    if image_file:
        img = Image.open(image_file)
        st.image(img, caption="Uploaded Screenshot", use_column_width=True)

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                img.save(tmp_file.name)
                extracted_text = pytesseract.image_to_string(tmp_file.name)
        except pytesseract.TesseractNotFoundError:
            st.error("⚠️ Tesseract not found. Please install it and set the path.")
            extracted_text = ""

        email_text = st.text_area("Extracted Text (editable):", value=extracted_text, height=200)

# === PDF Upload Method ===
elif input_method == "📄 Upload PDF File":
    pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])
    if pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        extracted_text = ""
        for page in pdf_reader.pages:
            extracted_text += page.extract_text() or ""

        if extracted_text.strip():
            st.success("✅ Text extracted from PDF.")
        else:
            st.warning("⚠️ No text could be extracted from the PDF.")

        email_text = st.text_area("Extracted Text (editable):", value=extracted_text, height=200)

# === Prediction Button ===
if st.button("🔍 Predict"):
    if not email_text.strip():
        st.warning("⚠️ Please provide email content.")
    else:
        # Preprocess text to Bag-of-Words
        words = re.findall(r'\b\w+\b', email_text.lower())
        word_freq = Counter(words)

        # Build feature dictionary with consistent feature order
        input_bow = {word: word_freq.get(word, 0) for word in feature_names}
        X_input = pd.DataFrame([input_bow])[feature_names]

        # Make prediction
        pred = model.predict(X_input)[0]
        label = "🛑 Spam / Phishing" if pred == 1 else "✅ Legit Email"

        st.success(f"**Prediction:** {label}")
