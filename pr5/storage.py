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
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass
        return False


def _merge_defaults(default: dict, loaded: dict) -> dict:
    result = {}
    for key in default:
        if key in loaded:
            result[key] = loaded[key]
        else:
            result[key] = default[key]
    return result


def load_state(path: str, default: dict) -> dict:
    if not os.path.exists(path):
        return default.copy()

    try:
        with open(path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
    except Exception:
        return default.copy()

    if not isinstance(loaded, dict):
        return default.copy()

    state = _merge_defaults(default, loaded)

    if not isinstance(state["player_name"], str):
        state["player_name"] = default["player_name"]

    if not isinstance(state["level"], int) or state["level"] < 0:
        state["level"] = default["level"]

    if not isinstance(state["coins"], int) or state["coins"] < 0:
        state["coins"] = default["coins"]

    if not isinstance(state["inventory"], dict):
        state["inventory"] = default["inventory"]
    else:
        clean_inventory = {}
        for k, v in state["inventory"].items():
            if isinstance(k, str) and isinstance(v, int) and v >= 0:
                clean_inventory[k] = v
        state["inventory"] = clean_inventory

    if not isinstance(state["settings"], dict):
        state["settings"] = default["settings"]

    return state
