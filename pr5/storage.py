import json
import os


def save_state(path: str, state: dict) -> bool:
    tmp_path = path + ".tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, path)
        return True
    except Exception:
        return False


def load_state(path: str, default: dict) -> dict:
    if not os.path.exists(path):
        return default.copy()

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return default.copy()

    if not isinstance(data, dict):
        return default.copy()

    result = default.copy()

    # Злиття значень
    for key in default:
        if key in data:
            result[key] = data[key]

    # Мінімальна валідація
    if not isinstance(result.get("level"), int) or result["level"] < 0:
        result["level"] = default["level"]

    if not isinstance(result.get("coins"), int) or result["coins"] < 0:
        result["coins"] = default["coins"]

    if not isinstance(result.get("inventory"), dict):
        result["inventory"] = default["inventory"]
    else:
        fixed_inventory = {}
        for item, count in result["inventory"].items():
            if isinstance(count, int) and count >= 0:
                fixed_inventory[item] = count
        result["inventory"] = fixed_inventory

    if not isinstance(result.get("settings"), dict):
        result["settings"] = default["settings"]

    return result
