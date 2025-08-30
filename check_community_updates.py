import re

# 读取社区页面HTML文件
with open('community.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# 搜索头像相关的HTML元素
avatar_pattern = r'<div class="author-info">(.*?)</div>'
avatar_matches = re.findall(avatar_pattern, html_content, re.DOTALL)

# 搜索导航栏顺序
nav_pattern = r'<nav class="nav">(.*?)</nav>'
nav_matches = re.findall(nav_pattern, html_content, re.DOTALL)

# 检查导航栏中社区和首页的顺序
if nav_matches:
    nav_content = nav_matches[0]
    community_pos = nav_content.find('url_for(\'community\')')
    home_pos = nav_content.find('url_for(\'home\')')
    
    print('导航栏顺序检查:')
    if community_pos != -1 and home_pos != -1:
        if community_pos < home_pos:
            print('✓ 社区功能已成功移到第一位！')
        else:
            print('✗ 社区功能仍在首页之后。')
    else:
        print('✗ 未找到导航栏中的社区或首页链接。')
else:
    print('✗ 未找到导航栏。')

# 检查头像是否存在
print('\n头像显示检查:')
if avatar_matches:
    print(f'✓ 找到 {len(avatar_matches)} 个头像区域:')
    for i, match in enumerate(avatar_matches[:3]):  # 只显示前3个
        print(f'\n头像区域 {i+1}:')
        # 查找头像URL
        src_pattern = r'src="(.*?)"'
        src_matches = re.findall(src_pattern, match)
        for src in src_matches:
            print(f'  头像URL: {src}')
        # 查找用户名
        name_pattern = r'<span class="author-name">(.*?)</span>'
        name_matches = re.findall(name_pattern, match)
        for name in name_matches:
            print(f'  用户名: {name}')
else:
    print('✗ 未找到头像区域。')