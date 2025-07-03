
## 🔍 Features

- Trained with XGBoost on textual features (Bag-of-Words)
- Handles input from raw text and email screenshots
- OCR via Tesseract to extract text from screenshots
- Classifies emails as `Spam 🚫` or `Legit ✅`

## 🧠 Model

- Algorithm: `XGBoostClassifier`
- Input: Cleaned and vectorized email content
- Output: Binary classification (spam / ham)

## 🛠 Tech Stack

- Python
- Scikit-learn, XGBoost
- Pytesseract + Pillow (for OCR)
- Pandas, NumPy, Matplotlib

## 📦 How to Use

```bash
# Install dependencies
pip install -r requirements.txt

# Run model on text input
python predict_text.py

# Run model on screenshot
python predict_from_image.py
````

## 📊 Example Predictions

| Email Text                    | Prediction |
| ----------------------------- | ---------- |
| `"You won $1000! Click here"` | 🚫 Spam    |
| `"Meeting at 10am tomorrow"`  | ✅ Legit    |

## 📷 OCR Demo

> Upload any screenshot of a suspicious email — we'll extract text and classify it in real-time.

## 💡 Future Ideas

* Deploy as a Streamlit or Flask web app
* Highlight risky words in prediction output
* Use more advanced NLP (BERT or LLMs)

## 🤝 Contribute

Pull requests and suggestions are welcome
