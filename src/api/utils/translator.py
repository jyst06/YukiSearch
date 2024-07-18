import translators as ts


def chinese_traditional_to_simplified(text):
    return ts.translate_text(text, translator="google", from_language="zh-TW", to_language="zh-CN")


def chinese_simplified_to_traditional(text):
    return ts.translate_text(text, translator="google", from_language="zh-CN", to_language="zh-TW")


if __name__ == '__main__':
    print(chinese_traditional_to_simplified("青春豬頭少年"))