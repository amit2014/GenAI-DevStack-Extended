import argparse
import glob
import os

from .pipeline import get_store

def iter_texts(source_dir: str):
    patterns = ["*.txt", "*.md", "*.markdown"]
    for p in patterns:
        for path in glob.glob(os.path.join(source_dir, p)):
            with open(path, "r", encoding="utf-8") as f:
                yield os.path.basename(path), f.read()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, default="data/sample_docs")
    parser.add_argument("--store", type=str, default=".cache/faiss")
    args = parser.parse_args()

    store = get_store()
    texts, metas = [], []
    for name, text in iter_texts(args.source):
        texts.append(text)
        metas.append({"source": name})

    if texts:
        store.add_texts(texts, metadatas=metas)
        print(f"Ingested {len(texts)} docs.")
    else:
        print("No docs found.")

if __name__ == "__main__":
    main()
