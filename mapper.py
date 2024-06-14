import re

def intent_encoding(text):
    # 使用正则表达式匹配文本模式
    if re.match(r'enterprise_overview|企业概述', text):
        return 0, 0
    elif re.match(r'Q&A_on_enterprise_information|企业信息问答', text):
        return 0, 1
    elif re.match(r'solution|专线解决方案', text):
        return 1, 0
    elif re.match(r'products_overview|专线产品概述', text):
        return 1, 1
    elif re.match(r'Q&A_on_product_information|专线产品信息问答', text):
        return 1, 2
    elif re.match(r'others|其他', text):
        return 999, 0
    else:
        return 999, 0


if __name__ == '__main__':
    # 示例使用
    examples = [
        "enterprise_overview",
        "企业概述",
        "Q&A_on_enterprise_information",
        "企业信息问答",
        "solution",
        "专线解决方案",
        "products_overview",
        "专线产品概述",
        "Q&A_on_product_information",
        "专线产品信息问答",
        "others",
        "其他",
    ]

    for example in examples:
        print(f"'{example}' -> {intent_encoding(example)}")
