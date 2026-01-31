import json
import os

class Config():
    def read():
        if not os.path.exists("./config.json"):
            raise Exception
        
        file = open("./config.json", "r")
        config = json.loads(file.read())
        file.close()

        return config