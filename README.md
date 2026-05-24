# OrgFold

AI-powered file organizer using Ollama + LangChain.

## Features

- Organize PDF, TXT, and Markdown files
- AI-powered categorization
- Local LLM support with Ollama
- Dry-run preview mode
- CLI command support
- Docker support

---

## Installation

### Clone Repo

```bash
git clone YOUR_REPO_URL
cd orgfold
```

### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install

```bash
pip install -e .
```

---

## Usage

```bash
orgfold ~/Downloads
```

Dry run:

```bash
orgfold ~/Downloads --dry-run
```

---

## Ollama

Start Ollama:

```bash
ollama serve
```

Pull model:

```bash
ollama pull gemma3:1b
```

---

## Docker

Build image:

```bash
docker build -t orgfold .
```

Run:

```bash
docker run --rm \
-v ~/Downloads:/data \
-e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
orgfold /data
```