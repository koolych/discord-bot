import json
import os

class Config():
    def read(self):
        if not os.path.exists("./config.json"):
            raise FileNotFoundError("config.json not found.")

        with open("./config.json", "r", encoding="utf-8") as f:
            return json.load(f)
