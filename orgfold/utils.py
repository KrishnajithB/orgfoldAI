from pathlib import Path


def truncate_text(
    text: str,
    max_chars: int = 1000
) -> str:

    return text[:max_chars].replace(
        "\n",
        " "
    ).strip()


def sanitize_folder_name(raw: str) -> str:

    name = raw.strip().splitlines()[0]

    name = "".join(
        c for c in name
        if c.isalnum() or c in ("_", "-")
    )

    name = name.strip("_- ")

    return name if name else "Uncategorized"


def get_unique_destination(
    dest_dir: Path,
    filename: str
) -> Path:

    dest = dest_dir / filename

    if not dest.exists():
        return dest

    stem = Path(filename).stem
    suffix = Path(filename).suffix

    counter = 1

    while True:

        candidate = (
            dest_dir /
            f"{stem}_{counter}{suffix}"
        )

        if not candidate.exists():
            return candidate

        counter += 1