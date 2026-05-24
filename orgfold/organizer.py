import os
import shutil
from pathlib import Path
from typing import Optional

from langchain_ollama import OllamaLLM

from langchain_community.document_loaders import (
    TextLoader,
    UnstructuredMarkdownLoader,
    PyPDFLoader,
)

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import (
    StrOutputParser
)

from .utils import (
    truncate_text,
    sanitize_folder_name,
    get_unique_destination,
)

# ─────────────────────────────────────────────────────

LLM_MODEL = "gemma3:1b"

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".md",
}

# ─────────────────────────────────────────────────────

CATEGORIZE_PROMPT = PromptTemplate.from_template(
    """
You are a file organizer assistant.

Based on the file name and content excerpt,
decide the BEST single folder category.

Rules:
- Return ONLY the folder name
- Use short names
- No explanations
- No full paths
- Use underscores instead of spaces

Examples:
Finance
Research
Medical
Resume
Code
Education
Legal
Notes

File name:
{filename}

Content excerpt:
\"\"\"
{content}
\"\"\"

Folder name:
"""
)

# ─────────────────────────────────────────────────────


def load_document(
    file_path: Path
) -> Optional[str]:

    ext = file_path.suffix.lower()

    try:

        if ext == ".pdf":
            loader = PyPDFLoader(
                str(file_path)
            )

        elif ext == ".md":
            loader = (
                UnstructuredMarkdownLoader(
                    str(file_path)
                )
            )

        else:
            loader = TextLoader(
                str(file_path),
                autodetect_encoding=True
            )

        docs = loader.load()

        full_text = " ".join(
            doc.page_content
            for doc in docs
        )

        return full_text.strip()

    except Exception as e:

        print(
            f"⚠ Could not read "
            f"{file_path.name}: {e}"
        )

        return None


# ─────────────────────────────────────────────────────


def organize_folder(
    folder: Path,
    dry_run: bool = False
):

    print(f"\n🗂 Organizing: {folder}\n")

    files = [
        f for f in folder.iterdir()
        if (
            f.is_file()
            and
            f.suffix.lower()
            in SUPPORTED_EXTENSIONS
        )
    ]

    if not files:

        print(
            "No supported files found."
        )

        return

    print(
        f"Found {len(files)} file(s)"
    )

    print(
        "Connecting to Ollama...\n"
    )

    llm = OllamaLLM(
        model=LLM_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0
    )

    chain = (
        CATEGORIZE_PROMPT
        | llm
        | StrOutputParser()
    )

    moves = []

    for idx, file_path in enumerate(
        files,
        start=1
    ):

        print(
            f"[{idx}/{len(files)}] "
            f"{file_path.name}"
        )

        text = load_document(file_path)

        if text is None:

            print("→ Skipped\n")

            continue

        excerpt = truncate_text(text)

        try:

            raw_category = chain.invoke({
                "filename": file_path.name,
                "content": excerpt,
            })

            category = sanitize_folder_name(
                raw_category
            )

        except Exception as e:

            print(f"⚠ LLM Error: {e}")

            category = "Uncategorized"

        dest_dir = folder / category

        dest_path = get_unique_destination(
            dest_dir,
            file_path.name
        )

        print(
            f"→ Category: {category}"
        )

        print(
            f"→ Destination: "
            f"{dest_path.relative_to(folder)}\n"
        )

        moves.append(
            (file_path, dest_path)
        )

    if not moves:

        print("Nothing to move.")

        return

    print("-" * 50)

    if dry_run:
        print("[DRY RUN MODE]\n")

    for src, dst in moves:

        if not dry_run:

            dst.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            shutil.move(
                str(src),
                str(dst)
            )

        print(
            f"{'(would move)' if dry_run else '✓'} "
            f"{src.name} "
            f"→ {dst.parent.name}/"
        )

    print(
        f"\n✅ Organized "
        f"{len(moves)} file(s)"
    )