from pathlib import Path
import tomllib
import json

def read_toml(path: Path) -> dict:
    data = tomllib.loads(path.read_text())
    return data

def pretty_print_json(data):
    """Prints JSON data in a human-readable format."""
    if isinstance(data, (str, bytes)):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            print(data)
            return
    print(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))
