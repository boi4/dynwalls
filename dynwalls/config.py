import json


class Config:

    def __init__(self, data_dir):
        self._conffile = data_dir+"/config.json"
        self._load_config()
        self._watching = True


    def __setattr__(self, name, value):
        """
        Save config to file after each attribute access
        """
        super().__setattr__(name, value)
        if hasattr(self,"_watching") \
            and self._watching \
            and not name.startswith("_"):
            self._save_config()


    def _save_config(self):
        with open(self._conffile, "w+") as f:
            serialized = json.dumps({k:v for (k,v) in vars(self).items() if not k.startswith("_")})
            f.write(serialized)


    def _load_config(self):
        try:
            with open(self._conffile, "r") as f:
                serialized = f.read()
                j = json.loads(serialized)
                for k in j:
                    setattr(self, k, j[k])
        except json.JSONDecodeError:
            print("Invalid config")
        except FileNotFoundError:
            print("No Config specified so far")
