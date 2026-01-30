import os
import json
import yaml
from tqdm import tqdm

from ingest.java_parser import parse_java_file
from ingest.xml_parser import parse_xml_file

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_config():
    with open(f"{ROOT}/config/paths.json") as f:
        paths = json.load(f)

    with open(f"{ROOT}/config/settings.yaml") as f:
        settings = yaml.safe_load(f)

    return paths, settings

def scan_files(base_path, extensions):
    collected = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                collected.append(os.path.join(root, file))
    return collected

def ingest():
    paths, settings = load_config()
    chunks = []

    for name, path in paths["codebases"].items():
        files = scan_files(
            path,
            settings["indexing"]["supported_extensions"]
        )

        for file_path in tqdm(files, desc=f"Ingesting {name}"):
            with open(file_path, "r", errors="ignore") as f:
                content = f.read()

            if file_path.endswith(".java"):
                parsed = parse_java_file(content)
            elif file_path.endswith(".xml"):
                parsed = parse_xml_file(content)
            else:
                continue

            for chunk in parsed:
                chunks.append({
                    "source": name,
                    "file": file_path,
                    **chunk
                })

    os.makedirs(f"{ROOT}/index", exist_ok=True)
    with open(f"{ROOT}/index/code_chunks.json", "w") as f:
        json.dump(chunks, f, indent=2)

    print(f"Total chunks indexed: {len(chunks)}")

if __name__ == "__main__":
    ingest()
