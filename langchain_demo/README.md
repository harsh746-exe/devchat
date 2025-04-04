# LangChain Demo with Hugging Face

This is a simple demo project that showcases how to use LangChain with Hugging Face models for text generation.

## Features

- Uses LangChain for LLM orchestration
- Integrates with Hugging Face's Mistral-7B-Instruct model
- Implements a simple chat interface
- Uses modern LangChain components (ChatPromptTemplate, StrOutputParser)

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd langchain-demo
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Hugging Face API token:
```bash
export HUGGINGFACEHUB_API_TOKEN="your-api-token"
```

## Usage

Run the demo:
```bash
python demo.py
```

## Requirements

- Python 3.11+
- LangChain and related packages
- Hugging Face API token

## License

MIT 