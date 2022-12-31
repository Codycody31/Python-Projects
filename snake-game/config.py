# Create a class to store all game data such as score, high score, etc. and to update the config file
import configparser


class GameData:
    """
    This class stores all game data such as score, high score, etc. and updates the config file
    """

    def __init__(self, config_path):
        self.config_path = config_path
        try:
            open(self.config_path)
        except FileNotFoundError:
            config = configparser.ConfigParser()
            config['DEFAULT'] = {
                'highscore': '0',
                'max_fps': '0',
                'volume': '0.5',
                'difficulty': '1',
                'controls': 'default',
                'fullscreen': 'False',
                'resolution': '800x600',
                'music': 'True',
                'sound': 'True'
            }
            with open(self.config_path, 'w') as configfile:
                config.write(configfile)

    def set(self, option, value, section="DEFAULT"):
        """
        It reads the config file, sets the option to the value, and writes the config file
        
        param option: The option to set
        param value: The value you want to set the option to
        param section: The section of the config file to write to, defaults to DEFAULT (optional)
        """
        config = configparser.ConfigParser()
        config.read(self.config_path)
        config.set(section, option, value)
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)

    def get(self, option, section="DEFAULT"):
        """
        It reads the config file and returns the value of the option
        
        param option: The option to get
        param section: The section of the config file to read from, defaults to DEFAULT (optional)
        """
        config = configparser.ConfigParser()
        config.read(self.config_path)
        return config.get(section, option)

    def reset(self):
        """
        It resets the config file to default values
        """
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            'highscore': '0',
            'max_fps': '0',
            'volume': '0.5',
            'difficulty': '1',
            'controls': 'default',
            'fullscreen': 'False',
            'resolution': '800x600',
            'music': 'True',
            'sound': 'True'
        }
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)
