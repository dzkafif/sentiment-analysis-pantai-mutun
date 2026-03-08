import pandas as pd
import matplotlib.pyplot as plt

# SETUP
Input_file = "data_bersih.csv"   
Output_file = "review_google_maps_sentiment_analysis.csv"

# LOAD DATA
df = pd.read_csv(Input_file)
print("Jumlah data awal:", len(df))

df = df.dropna(subset=['text_final'])

# SENTIMENT LEXICON
kata_positif = {"bagus","baik","nyaman","ramah","mantap","enak","bersih","murah",
    "puas","recommended","rekomendasi","lezat","cepat","keren","top"}

kata_negatif = {"buruk","jelek","mahal","lama","kecewa","kotor","parah","lambat",
    "tidak","kurang","mengecewakan","ribet","pelit,"}

# FUNGSI PELABELAN
def label_sentimen(text):
    score = 0
    text = str(text) # Pastikan formatnya teks
    for kata in text.split():
        if kata in kata_positif:
            score += 1
        elif kata in kata_negatif:
            score -= 1
            
    if score > 0:
        return "positif"
    elif score < 0:
        return "negatif"
    else:
        return "netral"

# TERAPKAN KE KOLOM YANG SUDAH BERSIH (text_final)
df['sentimen'] = df['text_final'].apply(label_sentimen)

# ANALISIS & VISUALISASI
print("\nDistribusi Sentimen:")
sentiment_count = df['sentimen'].value_counts()
print(sentiment_count)

sentiment_percent = (sentiment_count / len(df)) * 100
print("\nPersentase Sentimen (%):")
print(sentiment_percent.round(2))

plt.figure(figsize=(8,5))
sentiment_count.plot(kind='bar', color=['#2ca02c', '#d62728', '#7f7f7f'])
plt.title("Distribusi Sentimen Ulasan Pantai Mutun")
plt.xlabel("Sentimen")
plt.ylabel("Jumlah Ulasan")
plt.xticks(rotation=0)
plt.show()

# SIMPAN HASIL
df.to_csv(Output_file, index=False, encoding='utf-8-sig')
print(f"\n✅ SELESAI")
print(f"File hasil: {Output_file}")

print(df[['text', 'text_final', 'sentimen']].head(10))