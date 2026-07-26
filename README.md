# 🩹 PatchContext – GitHub Repository RAG Assistant

PatchContext is an AI-powered Retrieval-Augmented Generation (RAG) application that answers questions about a GitHub repository using its commits, issues, and pull requests. It combines semantic search with Google's Gemini model to provide accurate, context-aware responses.

## 🚀 Features

* Semantic search using **FAISS**
* High-quality embeddings with **BAAI/bge-small-en-v1.5**
* AI-powered answers using **Google Gemini**
* Retrieval from GitHub:

  * Commits
  * Issues
  * Pull Requests
* Streamlit web interface
* LangChain-based RAG pipeline
* MMR (Maximum Marginal Relevance) retrieval for diverse and relevant context

---

## 🛠️ Tech Stack

* Python
* Streamlit
* LangChain
* Google Gemini API
* FAISS
* Hugging Face Embeddings
* Pandas

---

## 📂 Project Structure

```text
PatchContext/
│
├── app.py
├── requirements.txt
├── commits.csv
├── issues.csv
├── pull_requests.csv
├── faiss_index/
├── create_vector_db.py
├── README.md
└── .env
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/Manishkushwahakr/PatchContext-RAG-Project.git
cd PatchContext-RAG-Project
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment

Windows

```bash
venv\Scripts\activate
```


### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 📊 Dataset

The knowledge base is built from:

* `commits.csv`
* `issues.csv`
* `pull_requests.csv`

These files are converted into vector embeddings and stored in a FAISS index.

---

## 🔍 Retrieval Pipeline

1. Load GitHub repository data
2. Split documents into chunks
3. Generate embeddings using BAAI/bge-small-en-v1.5
4. Store vectors in FAISS
5. Retrieve the most relevant documents using MMR
6. Send retrieved context to Gemini
7. Generate a grounded response

---

## 💬 Example Questions

* How are dependencies managed in the repository?
* Which pull request introduced authentication?
* What issues are related to API performance?
* Which commits fixed database bugs?
* Summarize the recent pull requests.

---

## 📸 Demo

Add screenshots or a short demo GIF here.

---

## 🔮 Future Improvements

* GitHub API integration for live repositories
* Repository URL input
* Multi-repository support
* Conversation memory
* Source highlighting
* Citation links to commits, issues, and pull requests
* Docker deployment
* Authentication and user management

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## 📄 License

This project is intended for educational and learning purposes.

---

## 👨‍💻 Author

**Manish Kumar**

* GitHub: https://github.com/Manishkushwahakr

If you found this project helpful, consider giving it a ⭐ on GitHub.

 outpots

 <img width="1920" height="1080" alt="Screenshot 2026-07-27 045719" src="https://github.com/user-attachments/assets/2568ae63-e4ca-4ada-92e5-b1548ce57a35" />
 
<img width="1920" height="1080" alt="Screenshot 2026-07-27 045853" src="https://github.com/user-attachments/assets/592231bb-8bb4-4279-889b-244454ff9f2c" />

<img width="1920" height="1080" alt="Screenshot 2026-07-27 045929" src="https://github.com/user-attachments/assets/8d270241-468d-4f4d-ae22-86637fc5fa33" />

<img width="1920" height="1080" alt="Screenshot 2026-07-27 045937" src="https://github.com/user-attachments/assets/680b7d91-26a4-4b7b-b365-8af03e7ea852" />
