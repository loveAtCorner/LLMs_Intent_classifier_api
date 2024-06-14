import os
import re

def remove_punctuation(word):
    # `\W` 表示匹配任何非单词字符，等价于 `[^a-zA-Z0-9_]`。
    return re.sub(r'^\W+|\W+$', '', word)

def initialize_regexp_lists(directory):
    regexp_lists = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            list_name = filename[:-4]
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                regexps = [line.strip() for line in file]
            regexp_lists[list_name] = regexps
    return regexp_lists

def match_text_with_regex(input_text, regex_patterns):
    match_results = {}
    input_text = remove_punctuation(input_text)
    for category, patterns in regex_patterns.items():
        matched_patterns = []
        for pattern in patterns:
            if re.fullmatch(pattern, input_text):
                matched_patterns.append(pattern)
                # break  # 如果匹配到，则跳出循环，不再检查该分类的其他模式
        if matched_patterns:
            match_results[category] = matched_patterns
    return match_results



if __name__ == "__main__":
    directory = "./intent_classification"
    regexp_lists = initialize_regexp_lists(directory)

    input_text = "杭州亚信科技有限公司有人去过吗？"
    # input_text = "我那个指标做的好"
    match_results = match_text_with_regex(input_text, regexp_lists)

    for list_name, matched_regexps in match_results.items():
        print(f"In {list_name}.txt, matched regexps: {', '.join(matched_regexps)}")
