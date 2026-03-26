from pathlib import Path
import tomllib
import json

def read_toml(path: Path) -> dict:
    data = tomllib.loads(path.read_text())
    return data

def prettify_json(data):
    """Prints JSON data in a human-readable format."""
    if isinstance(data, (str, bytes)):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            print(data)

            return json.dumps(None)
    return json.dumps(data, indent=4, sort_keys=False, ensure_ascii=False)
