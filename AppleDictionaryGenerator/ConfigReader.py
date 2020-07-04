import configparser

class ConfigReader:

    def __init__(self, filename):
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    def input_file(self):
        return self.config["COMMON"]["dictionary_file"]
    
    def dictionary_name(self):
        return self.config["COMMON"]["dictionary_name"]
