import configparser
import os


CONFIG_FILE_NAME = 'api.ini'
CONFIG_FILE_PATH = r"C:\Users\guguc\PycharmProjects\AnimeSearcher\configs\api.ini"#os.path.join(os.getcwd(), "configs/"+CONFIG_FILE_NAME)


def read_search_apis() -> dict:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

    return {
        "ani_gamer": config['SearchApi']['ani_gamer'],
        "nineciyuan": config['SearchApi']['nineciyuan'],
        "anime1": config['SearchApi']['anime1'],
        "sakura": config['SearchApi']['sakura']
    }


def read_video_apis() -> dict:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

    return {
        "ani_gamer": config['VideoApi']['ani_gamer'],
        "nineciyuan": config['VideoApi']['nineciyuan'],
        "anime1": config['VideoApi']['anime1'],
        "sakura": config['VideoApi']['sakura']
    }
