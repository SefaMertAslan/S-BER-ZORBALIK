from flask import Flask, request, render_template
import pickle

app = Flask(__name__,static_folder='static')
# Sayfalar
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/egitim')
def egitim():
    return render_template('egitim.html')

@app.route('/istatistik')
def istatistik():
    return render_template('istatistik.html')

@app.route('/hakkinda')
def hakkinda():
    return render_template('hakkinda.html')

# Model ve vectorizer'ı yükle
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

@app.route('/live_predict', methods=['POST'])
def live_predict():
    text = request.json.get('text', '').strip()

    if not text:
        return {"prediction": "Lütfen metin girin."}

    try:
        text_tfidf = vectorizer.transform([text])

        if text_tfidf.nnz == 0:
            return {"prediction": "Metin eğitim verisindeki kelimeleri içermiyor."}

        prediction = model.predict(text_tfidf)
        return {"prediction": prediction[0]}

    except Exception as e:
        return {"prediction": f"Hata: {str(e)}"}

# Tahmin
@app.route('/predict', methods=['POST'])
def predict():
    text = request.form.get('text', '').strip()

    if not text:
        return render_template('index.html', prediction="Lütfen metin girin.", text=text)

    try:
        text_tfidf = vectorizer.transform([text])

        if text_tfidf.nnz == 0:
            return render_template('index.html', prediction="Metin eğitim verisindeki kelimeleri içermiyor.", text=text)

        prediction = model.predict(text_tfidf)
        return render_template('index.html', prediction=prediction[0], text=text)

    except Exception as e:
        return render_template('index.html', prediction=f"Hata: {str(e)}", text=text)


if __name__ == "__main__":
    app.run(debug=True)
