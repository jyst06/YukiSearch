import hashlib


def generate_id(input_str: str) -> str:
    encoded_str = input_str.encode('utf-8')
    hash_object = hashlib.sha256(encoded_str)
    hex_dig = hash_object.hexdigest()

    return hex_dig[:16]


if __name__ == '__main__':
    test_inputs = [
        '繁體中文',
        '简体中文',
        'English',
        '123456'
    ]

    for input_str in test_inputs:
        print(f"Input: {input_str}, ID: {generate_id(input_str)}")
