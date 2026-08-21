import random
from collections.abc import Iterable

from .constants import CLOTHING_TYPES


def item_matches(item: dict, style: str, weather: str) -> bool:
    if style != "Any" and item.get("style") != style:
        return False
    if weather == "Any":
        return True
    item_weather = item.get("weather", "Any")
    return item_weather in ("Any", weather)


def generate_outfit(wardrobe: Iterable[dict], style: str = "Any", weather: str = "Any", rng=None) -> list[dict]:
    picker = rng or random
    items = list(wardrobe)
    outfit = []
    for clothing_type in CLOTHING_TYPES:
        candidates = [i for i in items if i.get("type") == clothing_type and item_matches(i, style, weather)]
        if candidates:
            outfit.append(picker.choice(candidates))
    return outfit
