# 读取 input.txt 文件并将内容转化为列表，忽略空行
with open('location_name.txt', 'r', encoding='utf-8') as file:
    data = file.read()
    print(type(data))
    print(data)

"""
主要作用是将一个字符串data转换成列表，并对每一个元素执行特定的处理。具体的逻辑流程如下：

data: 假设这个变量是一个以逗号,作为分隔符的大字符串，例如：'apple, banana, "orange", 123, "456,789"'

for item in data.split(',')：
使用内置的split()方法将输入字符串按逗号分割为多个子项。对于例子中的数据，这会生成一个包含'apple', ' banana', '"orange"', '123', ' "456,789"' 的列表。

if item.strip(): 这个条件判断用于去除每个元素（即item)的空格和首尾引号。如果item在处理之后不是空白字符或者非数值字符串，才会执行后续的操作。

item.strip()移除字符串item中的前导和尾随空白字符。
strip('"'): 这一步用于去除字符串中剩余的单引号（如果存在）或双引号。例如：'apple', ' banana', 'orange', '123', '456,789'

data_list = [...]：
将处理后的结果放入一个列表data_list中。对于例子中的数据，最终的data_list可能是['apple', 'banana', 'orange', '123', '456,789']。
"""
data_list = [item.strip().strip('"') for item in data.split(',') if item.strip()]

# 将列表强制转换成字符串
output_string = str(data_list)

# 将格式化后的字符串写入 output.txt 文件
with open('location_name_output.txt', 'w', encoding='utf-8') as file:
    file.write(output_string)

print("数据处理完成，并已写入 location_name_output.txt 文件。")