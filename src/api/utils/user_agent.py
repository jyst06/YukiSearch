import random
import os
from src.utils import get_application_root_path


ROOT_PATH = get_application_root_path()
CURRENT_PATH = os.path.join(ROOT_PATH, 'src', 'api', 'utils')
USER_AGENT_PATH = os.path.join(CURRENT_PATH, 'user_agents.txt')


def generate_user_agent() -> dict:
    with open(USER_AGENT_PATH, 'r') as file:
        user_agents = [line.strip() for line in file]

    user_agent = random.choice(user_agents)

    headers = {
        'User-Agent': user_agent
    }

    return headers


if __name__ == '__main__':
    print(USER_AGENT_PATH)
    print(generate_user_agent())
