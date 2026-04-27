from pathlib import Path
import tomllib
import json

def read_toml(path: Path) -> dict:
    data = tomllib.loads(path.read_text())
    return data

def update_key(data: dict, section: str, new_val: str, key: str) -> dict:
    data[section][key] = new_val

    return data

def add_section(data: dict, section: str):
    pass

def add_key(data: dict, section: str, key: str):
    data[section][key] = ""
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
