import os

"""
实体，一条文本可以有多个实体
"""
def initialize_entities(directory):
    """
    从指定目录读取实体类型数据到字典中，自动忽略文本中的空行。
    
    :param directory: 包含实体类型文件的目录路径
    :return: 实体类型的字典
    """
    # 使用字典来存储每个文件名对应的实体列表
    entities = {}

    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        # 检查是否为文本文件
        if filename.endswith(".txt"):
            # 创建列表变量名称，移除文件扩展名
            list_name = filename[:-4]
            # 初始化列表
            entities[list_name] = []

            # 打开并读取文本文件
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                # 逐行读取文件
                for line in file:
                    # 去除空行和仅包含空白字符的行
                    stripped_line = line.strip()
                    if stripped_line:  # 仅在非空时添加到列表
                        stripped_line = stripped_line.replace('(', '（').replace(')', '）')
                        entities[list_name].append(stripped_line)

    return entities


def check_for_entity_matches(test_text, entities):
    """
    检查测试文本中是否出现任何列表中的元素。

    :param test_text: 需要检查的文本
    :param entities: 包含实体列表的字典
    :return: 匹配结果的字典
    """
    # 将所有的英文括号替换成中文括号
    test_text = test_text.replace('(', '（').replace(')', '）')

    matches = {}
    # 遍历每个实体列表
    for list_name, entity_list in entities.items():
        # 检查每个元素是否在测试文本中
        for entity in entity_list:
            if entity in test_text:
                if list_name not in matches:
                    matches[list_name] = []
                matches[list_name].append(entity)
    return matches


def get_required_match(entity_type, matches):
    """
    根据用户定义的实体类别抽取实体。

    :param entity_type: 用户定义的实体类别，支持单个或多个类别
    :param matches: 检查文本后得到的匹配结果字典
    :return: 仅包含指定类别的匹配结果
    """
    required_matches = {}

    # 支持传入单个字符串或多个实体类别（列表）
    if isinstance(entity_type, str):
        entity_type = [entity_type]  # 转换为列表形式
    
    for key in entity_type:
        if key in matches and matches[key]:
            # 查找该键对应的最长文本
            longest_value = max(matches[key], key=len)
            required_matches[key] = [longest_value]

    if required_matches:
        return required_matches
    else:
        return None  # 如果没有找到匹配的实体类别，返回None


if __name__ == "__main__":
    # 指定目录路径
    directory = "./entity_type"
    # 初始化entities
    entities_lists = initialize_entities(directory)

    # 测试文本
    test_text = "鼎盛物流有限公司在教育和培训买入了大量对冲基金产品"
    matches = check_for_entity_matches(test_text, entities_lists)
    print("匹配结果:", matches)

    # 示例调用get_required_match
    entity_type = ['product_name', 'industry_name']  # 用户定义的实体类别
    result = get_required_match(entity_type, matches)
    print("指定类别的匹配结果:", result)
