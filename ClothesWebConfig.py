import json


class AppConfig:
    def __init__(self):
        self.hostname = "localhost"
        self.port = 5566
        self.load_config()

    def load_config(self, filename="config.json"):

        try:
            with open(filename) as f:
                config = json.load(f)
        except IOError:
            pass
        else:
            if "hostname" in config:
                self.hostname = config["hostname"]
            if "port" in config:
                self.port = config["port"]
