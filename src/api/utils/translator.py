import translators as ts


def chinese_traditional_to_simplified(text):
    return ts.translate_text(text, translator="google", from_language="zh-TW", to_language="zh-CN")


if __name__ == '__main__':
    print(chinese_traditional_to_simplified("青春豬頭少年"))