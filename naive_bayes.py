from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load hasil pre-processing sebelumnya
df = pd.read_csv('review_google_maps_sentiment_analysis.csv')

# Naive Bayes prediction & Evaluation
print("1. Mengubah teks menjadi vektor angka (TF-IDF)...")
vectorizer = TfidfVectorizer(max_features=1000, min_df=2, max_df=0.9)

# Validasi df['text_final'] tidak mengandung nilai 'Nan/Float' sebelum ke proses vektor.
df['text_final'] = df['text_final'].fillna('')

X = vectorizer.fit_transform(df['text_final']).toarray()
y = df['sentimen']

print("2. Membagi data: 80% Data Latih (Train) & 20% Data Uji (Test)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("3. Menerapkan Model Machine Learning (Naive Bayes)...")
model_nb = MultinomialNB()
model_nb.fit(X_train, y_train)

print("4. Melakukan Prediksi pada Data Uji...")
y_pred = model_nb.predict(X_test)

print("\n=== HASIL EVALUASI MODEL ===")
akurasi = accuracy_score(y_test, y_pred)
print(f"Tingkat Akurasi Model: {akurasi * 100:.2f}%")

print("\nDetail Classification Report:")
print(classification_report(y_test, y_pred))

# Membuat Confusion Matrix (Visualisasi Evaluasi)
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6,4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=model_nb.classes_,
            yticklabels=model_nb.classes_)
plt.title('Confusion Matrix - Naive Bayes')
plt.ylabel('Label Asli')
plt.xlabel('Prediksi Model')
plt.show()