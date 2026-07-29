# 🌐 Website Summarizer

An AI-powered website summarizer built with **FastAPI**, **HTMX**, **Jinja2**, **BeautifulSoup**, and the **OpenAI API**. Simply enter a website URL to receive a structured, easy-to-read summary generated using GPT-5.

---

## ✨ Features

* 🌍 Summarize any publicly accessible website
* 🤖 AI-generated structured analysis
* 📝 GitHub-flavoured Markdown rendering
* ⚡ Fast, responsive UI powered by HTMX
* 🎨 Modern interface built with Tailwind CSS
* 🔍 Intelligent content extraction using BeautifulSoup
* 🛡️ Environment-based configuration with Pydantic Settings
* 🧩 Clean service-oriented architecture
* 🚀 Async FastAPI backend

---

## 🚀 Live Demo

🌍 **Website:** https://website-summarizer-znpu.onrender.com

Try summarizing any publicly accessible website in your browser.

## 📸 Screenshots


### Home Page


![Home Page](./docs/images/home.png)


### Generated Summary


![Generated Summary](./docs/images/summary.png)


---

## 🏗️ Architecture

```text
Browser
    │
    ▼
FastAPI
    │
    ▼
Website Fetcher
    │
    ▼
BeautifulSoup
    │
    ▼
OpenAI API
    │
    ▼
Markdown Renderer
    │
    ▼
HTMX Response
```

---

## 🛠️ Tech Stack

### Backend

* FastAPI
* Uvicorn
* httpx
* BeautifulSoup4
* OpenAI Python SDK
* Pydantic Settings

### Frontend

* Jinja2
* HTMX
* Tailwind CSS
* GitHub Markdown CSS

### Development

* uv
* Python 3.12+
* Ruff (recommended)
* Pytest (planned)

---

## 📂 Project Structure

```text
website-summarizer/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── services/
│   ├── static/
│   ├── templates/
│   └── main.py
│
├── tests/
├── README.md
├── pyproject.toml
├── uv.lock
└── .env.example
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/vr-krishna/website-summarizer.git
cd website-summarizer
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Create an environment file

```bash
cp .env.example .env
```

Add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key
MODEL_NAME=gpt-5-nano
```

### 4. Run the application

```bash
uv run uvicorn app.main:app --reload
```

Open your browser:

```
http://127.0.0.1:8000
```

---

## 💡 How It Works

1. Enter a website URL.
2. The application fetches and cleans the webpage content.
3. Relevant text is extracted using BeautifulSoup.
4. The content is sent to the OpenAI API.
5. The AI generates a structured Markdown summary.
6. Markdown is rendered into HTML and displayed in the browser.

---

## 📋 Example Output

The generated report includes sections such as:

* Website Overview
* Website Category
* Purpose
* Key Topics
* Important Information
* Products / Services
* News & Announcements
* Important Entities
* Target Audience
* Key Takeaways
* Overall Impression

---

## 🔒 Environment Variables

| Variable         | Description         |
| ---------------- | ------------------- |
| `OPENAI_API_KEY` | OpenAI API key      |
| `MODEL_NAME`     | OpenAI model to use |

---

## 🌐 Deployment

This application can be deployed on platforms such as:

* Render
* Fly.io
* Railway
* Azure App Service

Environment variables should be configured through the hosting platform and **never committed** to the repository.

---

## 🗺️ Roadmap

* [x] FastAPI backend
* [x] HTMX frontend
* [x] AI-powered website summaries
* [x] Markdown rendering
* [x] Responsive UI
* [ ] Download summaries as Markdown
* [ ] Copy summary to clipboard
* [ ] URL validation improvements
* [ ] Comprehensive test suite
* [ ] Docker support
* [ ] CI/CD with GitHub Actions
* [ ] Multiple analysis modes
* [ ] Summary caching
* [ ] User authentication
* [ ] Summary history

---

## 🤝 Contributing

Contributions, ideas, and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Krishna V**

GitHub: https://github.com/vr-krishna
