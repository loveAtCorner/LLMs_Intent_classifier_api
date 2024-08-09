import os

def initialize_entities(directory):
    """
    从指定目录读取实体类型数据到字典中。

    :param directory: 包含实体类型文件的目录路径
    :return: 实体类型的字典
    """
    # 使用字典来存储每个文件名对应的列表
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
                    line = line.replace('(', '（').replace(')', '）')
                    # 移除行尾的换行符并添加到列表
                    entities[list_name].append(line.strip())

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

def get_highest_priority_match(matches):
    # 定义优先级列表
    priority = ['product_name', 'enterprise_name']
    
    highest_priority_key = None
    highest_priority_value = None
    
    # 按照优先级顺序查找最高优先级的键值对
    for key in priority:
        if key in matches and matches[key]:
            # 查找该键对应的最长文本
            longest_value = max(matches[key], key=len)
            highest_priority_key = key
            highest_priority_value = longest_value
            break
    
    if highest_priority_key and highest_priority_value:
        return {highest_priority_key: [highest_priority_value]}
    else:
        return None  # 如果没有找到任何匹配的键，返回None


if __name__ == "__main__":
    # 指定目录路径
    directory = "./entity_type"
    # 初始化entities
    entities_lists = initialize_entities(directory)
    
    # 测试函数
    test_text = "上海通昊成套电器有限公司浦阳办事处做什么的"
    matches = check_for_entity_matches(test_text, entities_lists)
    print(matches)

    # 示例调用
    # matches = {'metrics': ['专线', '专线潜客'], 'senario_names': ['浙江加达流体控制有限公司']}
    result = get_highest_priority_match(matches)
    print(result)  # 输出 {'metrics': ['专线潜客']}