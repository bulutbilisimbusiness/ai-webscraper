# 🤖 AI Web Scraper

AI destekli web scraping uygulaması. Herhangi bir web sitesini tarayıp, AI ile istediğiniz bilgileri çıkarır.

## 🌐 **Canlı Demo**

**[🚀 Uygulamayı Deneyin](https://ai-webscraper-bksaugxfgbjmzwerprtr29.streamlit.app/)**

## ⚡ Hızlı Başlangıç

### 1. Groq API Key Alın (Ücretsiz)

- https://console.groq.com adresine gidin
- Hesap açın ve API key oluşturun

### 2. Kurulum

```bash
pip install -r requirements.txt
cp .env.example .env
```

### 3. .env Dosyasını Doldurun

```
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Çalıştırın

```bash
streamlit run main.py
```

## 💡 Kullanım

1. Web sitesi URL'si girin
2. "Scrape Site" tıklayın
3. AI'ya ne çıkarmasını istediğinizi yazın
4. "Parse Content" tıklayın

## 🛠️ Test Siteleri

- https://quotes.toscrape.com
- https://books.toscrape.com
- https://news.ycombinator.com

## 📋 Özellikler

- ✅ Ücretsiz AI (Groq Llama3)
- ✅ Captcha çözümü
- ✅ Kolay deployment
- ✅ Error handling
