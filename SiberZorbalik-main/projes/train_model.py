import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import pickle

# Veri setini yükle
data = pd.read_csv('veri_seti.csv')  # Veri setinizin dosya adını buraya yazın
texts = data['tweet_text']  # Metin sütunu
labels = data['cyberbullying_type']  # Etiket sütunu

# Veriyi eğitim ve test setlerine ayır
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

# TF-IDF vektörleştirme
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Modeli eğit
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Test verisi üzerinde modelin doğruluğunu kontrol et
accuracy = model.score(X_test_tfidf, y_test)
print(f"Model doğruluğu: {accuracy * 100:.2f}%")

# Modeli ve vectorizer'ı kaydet
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("Model ve vectorizer başarıyla kaydedildi.")