from jinja2 import Environment, FileSystemLoader
import pickle as pikle
import os
iput_text = input("请输入文本内容：")
text = iput_text.replace('\n', '<br>')  # 将换行符
# 1. 创建模板环境，指定模板文件所在的目录
file_loader = FileSystemLoader(r'C:\Users\ZHD\Desktop\program\personalwebsite\mb')
env = Environment(loader=file_loader)

# 2. 从环境中加载指定的模板文件
template = env.get_template('mb.html')

# 3. 准备要填充到模板中的动态数据
data = {
    'content': f'<section class="text-hidden"><p>{text}</p></section>'
}
filename = 'data.pkl'

# 判断文件是否存在
if os.path.exists(filename):
    with open(filename, 'rb') as f:
        datas = pikle.load(f)  # 从文件中加载已有数据
else:
    datas = []  # 如果不存在，初始化为空列表

# 2. 将新的数据追加到列表中
# 注意：这里的 data 是你上面准备好的包含 content 的字典
datas.append(data)  
for i in range(len(datas)):
    content=''
    content = datas[i]['content'] = content['content'].replace('<br>', '\n')  # 将 <br> 替换回换行符
# 3. 将更新后的完整列表重新保存到文件中
with open(filename, 'wb') as f:
    pikle.dump(datas, f)  # 将数据保存到文件中以供后续使用


print("datas:", datas)
# 4. 渲染模板，将数据注入并生成完整的 HTML 字符串
output = template.render(content=content)

# 5. 打印结果或将其写入文件
print(output)

# 如果需要保存为真实的网页文件：
with open('../output.html', 'w', encoding='utf-8') as f:
    f.write(output)