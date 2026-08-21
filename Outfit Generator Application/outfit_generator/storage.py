import json
from pathlib import Path
from typing import Any


class JsonStore:
    def __init__(self, data_dir: Path | str):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.wardrobe_path = self.data_dir / "wardrobe.json"
        self.outfits_path = self.data_dir / "outfits.json"
        self._ensure_file(self.wardrobe_path)
        self._ensure_file(self.outfits_path)

    @staticmethod
    def _ensure_file(path: Path) -> None:
        if not path.exists():
            path.write_text("[]\n", encoding="utf-8")

    @staticmethod
    def _load(path: Path) -> list[dict[str, Any]]:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            return value if isinstance(value, list) else []
        except (OSError, json.JSONDecodeError):
            return []

    @staticmethod
    def _save(path: Path, value: list[dict[str, Any]]) -> None:
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        temporary.replace(path)

    def load_wardrobe(self) -> list[dict[str, Any]]:
        return self._load(self.wardrobe_path)

    def save_wardrobe(self, wardrobe: list[dict[str, Any]]) -> None:
        self._save(self.wardrobe_path, wardrobe)

    def load_outfits(self) -> list[dict[str, Any]]:
        return self._load(self.outfits_path)

    def save_outfits(self, outfits: list[dict[str, Any]]) -> None:
        self._save(self.outfits_path, outfits)
