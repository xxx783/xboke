# 个人博客网站

这是一个使用Flask框架开发的个人博客网站，具有用户注册、登录、发布文章、编辑文章、删除文章等功能。

## 功能特点

- 用户注册和登录系统
- 发布、编辑和删除博客文章
- 查看所有文章和单篇文章详情
- 管理员面板，用于管理用户和文章
- 响应式设计，适配各种设备屏幕

## 技术栈

- 后端：Python 3, Flask
- 数据库：SQLite
- 前端：HTML, CSS, JavaScript

## 安装和运行

1. 确保你已经安装了Python 3

2. 安装依赖包：

   ```
   pip install -r requirements.txt
   ```

3. 运行应用程序：

   ```
   python app.py
   ```

4. 打开浏览器，访问 http://localhost:5000

## 管理员账户

应用程序启动时会自动创建一个管理员账户：
- 用户名：admin
- 密码：admin123

请登录后修改管理员密码以确保安全。

## 项目结构

```
├── app.py              # 主应用程序文件
├── requirements.txt    # 依赖包列表
├── README.md           # 项目说明文件
├── templates/          # HTML模板文件
│   ├── base.html       # 基础模板
│   ├── index.html      # 首页
│   ├── login.html      # 登录页面
│   ├── register.html   # 注册页面
│   ├── admin.html      # 管理员页面
│   ├── create_post.html # 创建/编辑文章页面
│   ├── post.html       # 文章详情页面
│   └── user_posts.html # 用户文章页面
└── static/             # 静态文件
    ├── css/            # CSS样式文件
    └── js/             # JavaScript文件
```

## 注意事项

- 本项目仅作为学习和演示使用
- 在生产环境中，请修改SECRET_KEY为随机生成的安全密钥
- 考虑使用更安全的数据库和认证方式

## License

MIT