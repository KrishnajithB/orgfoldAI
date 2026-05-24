import sys
import argparse
from pathlib import Path

from .organizer import organize_folder


def main():

    parser = argparse.ArgumentParser(
        prog="orgfold",
        description=(
            "AI-powered file organizer "
            "using Ollama + LangChain"
        )
    )

    parser.add_argument(
        "folder",
        type=str,
        help="Folder path to organize"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Preview actions "
            "without moving files"
        )
    )

    args = parser.parse_args()

    folder = Path(
        args.folder
    ).expanduser().resolve()

    if not folder.exists():

        print(
            f"❌ Folder not found: "
            f"{folder}"
        )

        sys.exit(1)

    if not folder.is_dir():

        print(
            f"❌ Not a directory: "
            f"{folder}"
        )

        sys.exit(1)

    organize_folder(
        folder,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    main()