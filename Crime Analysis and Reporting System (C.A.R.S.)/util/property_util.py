import configparser
import os

class PropertyUtil:
    @staticmethod
    def get_property_string():
        config = configparser.ConfigParser()
        file_path = os.path.join(os.path.dirname(__file__), 'db.ini')
        print("Looking for DB config at:", file_path)

        with open(file_path, 'r') as f:
            print("File content:\n", f.read())

        config.read(file_path)

        print("Sections found:", config.sections())

        return {
            'host': config.get('database', 'host'),
            'port': config.getint('database', 'port'),
            'user': config.get('database', 'user'),
            'password': config.get('database', 'password'),
            'database': config.get('database', 'database')
        }
