# Tommy – NovaPay AI Assistant 🤖

<p align="center">
  <img src="assets/tommy.png" width="220" alt="Tommy">
</p>

<p align="center">
An AI-powered customer support assistant for NovaPay built with the OpenAI Agents SDK, OpenRouter and Streamlit.
</p>

 Tommy – NovaPay AI Assistant 

The assistant answers customer questions about NovaPay products and services using NovaPay's official documentation as its knowledge source.

## Features

- AI-powered customer support
- Official documentation search
- OpenRouter integration
- DeepSeek V3 language model
- OpenAI Agents SDK
- Streamlit chat interface
- Conversation memory
- Docker deployment
- Hugging Face Spaces deployment

## Tech Stack

- Python 3.12
- OpenAI Agents SDK
- OpenRouter
- DeepSeek Chat V3
- Streamlit
- BM25 (rank_bm25)
- PyPDF
- Docker
- Hugging Face Spaces

## Project Structure

```
.
├── agent.py
├── app.py
├── Dockerfile
├── requirements.txt
├── pyproject.toml
├── resources/
│   └── NovaPay Profile.pdf
├── assets/
│   ├── style.css
│   └── tommy.png
└── .streamlit/
    └── config.toml
```

## Installation

Clone the repository.

```bash
git clone <repository-url>
cd NovaPay
```

Install dependencies.

```bash
uv sync
```

Create a `.env` file.

```env
API_KEY=your_openrouter_api_key
```

Run the application.

```bash
streamlit run app.py
```

## Deployment

The application is containerized with Docker and can be deployed directly to Hugging Face Spaces using the Docker SDK.

## Knowledge Source

Tommy retrieves information from the official NovaPay documentation.

Current knowledge source:

- NovaPay Profile.pdf

## Future Improvements

- Retrieval-Augmented Generation (RAG)
- Multiple document support
- Source citations
- Conversation history
- Smart contract assistant
- API documentation search
- Analytics dashboard

## License

This project is provided for educational and demonstration purposes.