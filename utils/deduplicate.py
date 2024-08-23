def remove_duplicates(input_file, output_file):
    seen = set()
    unique_lines = []

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # 去除行首尾的空白字符
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as file:
        for line in unique_lines:
            file.write(line + '\n')

if __name__ == "__main__":
    input_file = '../test/mix_query.txt'
    output_file = '../test/query.txt'
    remove_duplicates(input_file, output_file)
    print(f"已生成去重后的文件: {output_file}")
