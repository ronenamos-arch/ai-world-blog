"""
AI World Blog - Safety Rollback Script
This script provides a one-click rollback mechanism for any automated folder restructuring.
"""

import json
import os
import shutil
from pathlib import Path

REGISTRY_FILE = Path(__file__).parent / "logs" / "relocation_registry.json"

def rollback():
    if not REGISTRY_FILE.exists():
        print("No relocation registry found. Workspace is at its baseline state.")
        return

    try:
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            registry = json.load(f)
    except Exception as e:
        print(f"Error reading registry: {e}")
        return

    moves = registry.get("moves", [])
    if not moves:
        print("Registry has no pending moves to revert.")
        return

    print(f"Starting rollback of {len(moves)} file relocations...")
    reverted_count = 0

    # Process in reverse order
    for item in reversed(moves):
        src = Path(item["destination"])
        orig = Path(item["original"])

        if src.exists():
            orig.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(orig))
            print(f"Reverted: {src} -> {orig}")
            reverted_count += 1
        else:
            print(f"Warning: File {src} not found to revert.")

    # Remove or clear registry after successful rollback
    REGISTRY_FILE.unlink(missing_ok=True)
    print(f"Rollback complete. {reverted_count} files restored to their original paths.")

if __name__ == "__main__":
    rollback()
