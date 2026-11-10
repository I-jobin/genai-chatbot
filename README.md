# Gemini Chatbot

A chatbot powered by Google Gemini and LangChain, with a Django web interface. Chat history is kept per browser session, and you can pick the model, edit the system prompt and clear the chat from the sidebar.

## Features

- Chat UI built with Django, plain HTML, CSS and JavaScript
- Gemini models via `langchain-google-genai`
- Model selector and editable system prompt
- Per-session chat history with a clear-chat button
- Optional Streamlit version (`chatbot.py`)

## Project structure

```
gen ai/
├── manage.py
├── config/          # Django project settings and URLs
├── chat/            # Chat app (views, urls, templates)
├── chatbot.py       # Streamlit version
├── requirements.txt
└── .env             # API key (not committed)
```

## Setup

1. Clone the repo and open the folder:

   ```bash
   git clone https://github.com/I-jobin/genai-chatbot.git
   cd genai-chatbot
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv myvenv
   myvenv\Scripts\activate      # Windows
   source myvenv/bin/activate   # macOS / Linux
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your Gemini API key from Google AI Studio:

   ```
   GEM=your_api_key_here
   ```

5. Set up the database and run the server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

6. Open http://127.0.0.1:8000 in your browser.

## Streamlit version (optional)

```bash
pip install streamlit
streamlit run chatbot.py
```

## Configuration

- **Models:** edit the `MODELS` list in `chat/views.py` when Google renames or retires models.
- **API key:** read from `GEM`, `GEMINI_API_KEY` or `GOOGLE_API_KEY` in `.env`.

## Security

Never commit your `.env` file or API key. They are listed in `.gitignore`.

## Tech stack

Python, Django, LangChain, Google Gemini API, Streamlit
