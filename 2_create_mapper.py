import os
from config import INTENTS_ch, INTENTS_en

def create_mapper_file():
    mapper_content = """import re

def intent_encoding(text):\n"""
    
    # Generate the mapping content
    for ch, en in zip(INTENTS_ch, INTENTS_en):
        mapper_content += f"    if re.match(r'{en}|{ch}', text):\n"
        index = INTENTS_en.index(en)
        mapper_content += f"        return {index // 2}, {index % 2}\n"
    
    # Default return statement
    mapper_content += """    else:
        return 999, 0

if __name__ == '__main__':
    # 示例使用
    examples = [
"""
    
    # Add example usage for testing
    examples = INTENTS_ch + INTENTS_en
    for example in examples:
        mapper_content += f"        '{example}',\n"
    
    mapper_content += """    ]

    for example in examples:
        print(f"'{example}' -> {intent_encoding(example)}")
"""

    # Write the mapper.py file
    with open('mapper.py', 'w', encoding='utf-8') as file:
        file.write(mapper_content)

    print("mapper.py has been created successfully.")

if __name__ == "__main__":
    create_mapper_file()
