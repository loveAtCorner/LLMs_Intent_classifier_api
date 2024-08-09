
# 输入文件路径
input_file_path = 'company_names.txt'
# 输出文件路径
output_file_path = 'company_names_clean.txt'

# 读取输入文件
with open(input_file_path, 'r', encoding='utf-8') as input_file:
    # 读取每一行，并过滤
    lines = input_file.readlines()
    filtered_lines = [line for line in lines if len(line.strip()) > 4]

# 写入到输出文件
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.writelines(filtered_lines)

print(f'处理完成，过滤后的数据已保存到{output_file_path}')
