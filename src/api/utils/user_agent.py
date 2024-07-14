import random
import os


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
USER_AGENT_PATH = os.path.join(CURRENT_PATH, 'user_agents.txt')


def generate() -> dict:
    with open(USER_AGENT_PATH, 'r') as file:
        user_agents = [line.strip() for line in file]

    user_agent = random.choice(user_agents)

    headers = {
        'User-Agent': user_agent
    }

    return headers


if __name__ == '__main__':
    print(USER_AGENT_PATH)
    print(generate())
