
# 🧘 AntarAtma – Your AI-Powered Mental Wellness Companion

> _“In a world full of noise, **AntarAtma** listens deeply.”_

![banner](https://user-images.githubusercontent.com/placeholder/antaratma-banner.png)  
_A minimal yet powerful mental health chatbot powered by AI + NLP._

---

## 💡 About AntarAtma

**AntarAtma** is an empathetic, NLP-powered mental health chatbot that engages in emotionally intelligent conversations, recommends mental wellness exercises, and responds to crisis language with care — all in a sleek, modern chat interface.

🧠 Built using **Gemini 2.5 Flash**, **TextBlob NLP**, and a **custom safety engine**, AntarAtma aims to provide a quiet, comforting space to open up — anytime, anywhere.

---

## ✨ Features at a Glance

| 🧠 NLP Engine            | 💬 Emotion-Aware Chatbot    | 🚨 Crisis Detection         |
|-------------------------|-----------------------------|-----------------------------|
| Uses **TextBlob + NLTK** for real-time sentiment scoring | Generates compassionate, contextual replies using **Gemini 2.5 Flash** | Detects suicidal/self-harm intent and switches to **Crisis Mode** with curated responses & support links |

| 📓 Smart Suggestions     | 🧘 Self-Care Toolkit        | 🧠 Memory Retention         |
|-------------------------|-----------------------------|-----------------------------|
| Suggests exercises like breathing, grounding, or journaling based on tone | Built-in **4-7-8 breathing**, **5-4-3-2-1 grounding**, and reflective journaling prompts | Remembers user name, location, and mood during session (JSON memory) |

---

## 🛠️ Tech Stack

| Component         | Stack                                |
|-------------------|---------------------------------------|
| 💬 Chat Engine     | [Gemini 2.5 Flash API](https://ai.google.dev/) |
| 🧠 Sentiment Analysis | TextBlob + NLTK                   |
| 💻 UI Framework    | Streamlit (Python)                   |
| 🧠 Memory Engine   | Session & JSON-based memory system   |
| 📊 Exercises       | JSON-defined behavioral therapies    |

---

## 🚀 Getting Started

### 📥 1. Clone the Repo

```bash
git clone https://github.com/aromal-rm/mental_healthBot.git
cd mental_healthBot
```

### 🛠 2. Install Dependencies

```bash
pip install -r requirements.txt
python -m textblob.download_corpora
python -m nltk.downloader punkt stopwords
```

### 🔐 3. Add Your API Key

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_google_gemini_key_here
```

### ▶️ 4. Run the App

```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
antaratma/
├── app.py                  # Main application (Streamlit)
├── exercises/              # JSON: breathing, journaling, grounding
├── utils/                  # NLP, AI engine, memory, safety logic
│   ├── sentiment.py
│   ├── safety.py
│   ├── memory.py
│   └── ai_engine.py
├── memory.json             # Memory store (session)
├── .env                    # Gemini API key (never commit!)
└── README.md               # This file ❤️
```

---

## 🧪 Example Use Cases

| Input                               | AntarAtma Response                                                 |
|------------------------------------|----------------------------------------------------------------------|
| “I feel like I don’t matter.”      | Sentiment: -0.8 → Suggests grounding or journaling + caring message |
| “I want to end it all.”            | Enters **Crisis Mode** with emergency support messaging              |
| “My name is Ananya, I’m from Pune.”| Memory updated: remembers for natural future conversation            |

---

## ⚠️ Crisis Detection Mode (Safety First)

> AntarAtma actively scans for self-harm or suicidal phrases using pattern matching and sentiment scoring.

If detected:
- Pauses normal chat generation
- Triggers a **crisis-specific AI prompt**
- Provides comforting response & mental health resources (e.g. 988, iCall India)

---

## 🌍 Real-World Impact

- ✅ Perfect for **college students**, **corporate wellness tools**, or **personal journaling**
- ✅ Can run **locally** or deploy via Streamlit Cloud
- ✅ Built minimal by design — but emotionally intelligent in function

---

## ❤️ Why AntarAtma?

We believe mental health support should be:

- 🕊️ **Private**  
- 🤖 **Non-judgmental**  
- 🧘 **Emotionally aware**  
- 🧠 **Available 24/7**

**AntarAtma** isn’t a therapist — but it *is* a gentle companion when you're feeling low and don’t know who to talk to.

---

## 📜 License

MIT License © [Aromal RM](https://github.com/aromal-rm)

---

## 🙏 Acknowledgements

- [Google Gemini API](https://ai.google.dev/)
- [TextBlob NLP](https://textblob.readthedocs.io/en/dev/)
- [Streamlit](https://streamlit.io/)
- [You — for caring about mental wellness 💙]

---
