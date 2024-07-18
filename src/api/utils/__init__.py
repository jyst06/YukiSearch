from src.api.utils.user_agent import generate_user_agent
from src.api.utils.translator import chinese_traditional_to_simplified, chinese_simplified_to_traditional
from src.api.utils.config_reader import read_search_apis, read_video_apis


__all__ = [
    "generate_user_agent",
    "chinese_traditional_to_simplified",
    "chinese_simplified_to_traditional",
    "read_search_apis",
    "read_video_apis"
]


if __name__ == '__main__':
    print(generate_user_agent())
    print(read_video_apis())
    print(read_search_apis())
