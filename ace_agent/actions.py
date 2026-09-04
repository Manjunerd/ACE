import re
from .models import Action

def box(value: str):
    nums = [int(x) for x in re.findall(r"\d+", value)]
    if len(nums) >= 4:
        return nums[:4]
    if len(nums) >= 2:
        return [nums[0], nums[1], nums[0], nums[1]]
    raise ValueError("invalid coordinate box")

def parse_call(text: str) -> Action:
    text = text.strip()
    m = re.search(r"Action:\s*(.*)$", text, re.I | re.S)
    call = (m.group(1).strip() if m else text).splitlines()[0].strip()
    name_m = re.match(r"([a-zA-Z_]+)\s*\((.*)\)", call)
    if not name_m:
        raise ValueError("No valid action call")
    name, args_s = name_m.groups()
    args = {}
    pattern = r"(\w+)\s*=\s*('(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\")"
    for key, val in re.findall(pattern, args_s):
        raw = val[1:-1]
        try:
            args[key] = bytes(raw, "utf-8").decode("unicode_escape")
        except UnicodeDecodeError:
            args[key] = raw
    return Action(name, args)

def normalize(action: Action) -> Action:
    n = action.name.lower()
    allowed = {"click", "left_double", "right_single", "drag", "hotkey", "type", "scroll", "wait", "finished", "call_user"}
    if n not in allowed:
        raise ValueError(f"unsupported action: {n}")
    a = dict(action.args)
    if n in {"click", "left_double", "right_single"}:
        a["box"] = box(a.get("start_box", ""))
    elif n == "drag":
        a["start_box"] = box(a.get("start_box", ""))
        a["end_box"] = box(a.get("end_box", ""))
    elif n == "scroll":
        a["direction"] = a.get("direction", "down").lower()
        if a["direction"] not in {"up", "down", "left", "right"}:
            raise ValueError("bad scroll direction")
        if a.get("start_box"):
            a["box"] = box(a["start_box"])
    elif n == "hotkey":
        keys = a.get("key", "").lower().split()
        if not keys or len(keys) > 3:
            raise ValueError("hotkey must have 1-3 keys")
        a["keys"] = keys
    elif n == "type" and "content" not in a:
        raise ValueError("type requires content")
    return Action(n, a)
