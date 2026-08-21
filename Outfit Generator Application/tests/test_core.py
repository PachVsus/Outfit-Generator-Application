import random
import tempfile
import unittest
from pathlib import Path

from outfit_generator.generator import generate_outfit
from outfit_generator.storage import JsonStore


class CoreTests(unittest.TestCase):
    def test_json_persistence(self):
        with tempfile.TemporaryDirectory() as directory:
            store = JsonStore(Path(directory))
            wardrobe = [{"id": "1", "name": "Tee"}]
            outfits = [{"id": "o1", "items": ["1"]}]
            store.save_wardrobe(wardrobe); store.save_outfits(outfits)
            self.assertEqual(store.load_wardrobe(), wardrobe)
            self.assertEqual(store.load_outfits(), outfits)

    def test_generation_filters_style_and_weather(self):
        wardrobe = [
            {"id": "1", "type": "Shirt", "style": "Casual", "weather": "Warm"},
            {"id": "2", "type": "Shirt", "style": "Goth", "weather": "Cold"},
            {"id": "3", "type": "Shoes", "style": "Casual", "weather": "Any"},
        ]
        result = generate_outfit(wardrobe, "Casual", "Warm", random.Random(1))
        self.assertEqual([item["id"] for item in result], ["1", "3"])


if __name__ == "__main__": unittest.main()
