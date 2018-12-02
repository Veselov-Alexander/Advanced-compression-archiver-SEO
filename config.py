import configparser

class Config:

    @staticmethod 
    def initialize():
        Config.config = configparser.ConfigParser()
        Config.config.optionxform = str
        Config.config.read("config.ini")
        Config.properties = dict(Config.config.items("DEFAULT"))

    @staticmethod
    def __getitem__(property_name):
        return Config.properties[property_name]

Config.initialize()
__config = Config()

INPUT_PATH = __config["InputPath"]
DECOMPRESS_PATH = __config["DecompressPath"]
COMPRESS_PATH = __config["CompressPath"]

ARCHIVE_INPUT_DIRECTORY = __config["ArchiveInputDirectory"]
ARCHIVE_EXTRACT_DIRECTORY = __config["ArchiveExtractDirectory"]
ARCHIVE_FILE = __config["ArchiveFile"]
