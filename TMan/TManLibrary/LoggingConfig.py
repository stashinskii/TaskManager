import configparser
import logging
import os


class loggingConfig:
    """
    Класс, предназначенный для задания и получения информации о конфигурации
    """
    DATA_DIR = os.environ['HOME'] + '/tmandata/'

    @staticmethod
    def set_logging_config(section, format, file):

        if section is logging.INFO:
            section = "INFO"
        elif section is logging.WARNING:
            section = "WARNING"
        config = configparser.ConfigParser()
        config.read(loggingConfig.DATA_DIR + "/log_config.ini")
        config.set(section, 'format', format)
        config.set(section, 'file', os.environ['HOME'] +"/"+ file)
        with open(loggingConfig.DATA_DIR+"/log_config.ini", 'w') as f:
            config.write(f)

    @staticmethod
    def get_logging_config(section):
        if section is logging.INFO:
            section = "INFO"
        elif section is logging.WARNING:
            section = "WARNING"

        config = configparser.ConfigParser()
        config.read(loggingConfig.DATA_DIR + "/log_config.ini")
        format = config.get(section, 'format')
        file = config.get(section, 'file')
        return format, file


