import re

# 读取HTML文件
with open('temp.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# 搜索头像相关的HTML元素
avatar_pattern = r'<div class="author-info">(.*?)</div>'
avatar_matches = re.findall(avatar_pattern, html_content, re.DOTALL)

# 搜索头像图片URL
src_pattern = r'src="(.*?)"'

print(f'Found {len(avatar_matches)} author-info sections:')
for i, match in enumerate(avatar_matches):
    print(f'\nSection {i+1}:')
    print(match.strip())
    
    # 查找头像URL
    src_matches = re.findall(src_pattern, match)
    for src in src_matches:
        print(f'Avatar URL: {src}')