from app import app, db, User, Post
from passlib.hash import sha256_crypt
from datetime import datetime

with app.app_context():
    # 创建一个测试用户
    hashed_password = sha256_crypt.hash('testpassword')
    test_user = User(
        username='testuser',
        password=hashed_password,
        profile_picture='default.jpg',  # 使用默认头像
        bio='This is a test user.',
        theme_preference='light'
    )
    
    # 添加用户到数据库
    db.session.add(test_user)
    db.session.commit()
    
    # 创建几篇测试文章
    test_post1 = Post(
        title='First Test Post',
        content='This is the content of the first test post.',
        date_posted=datetime.utcnow(),
        user_id=test_user.id
    )
    
    test_post2 = Post(
        title='Second Test Post',
        content='This is the content of the second test post.',
        date_posted=datetime.utcnow(),
        user_id=test_user.id
    )
    
    # 添加文章到数据库
    db.session.add(test_post1)
    db.session.add(test_post2)
    db.session.commit()
    
    print('Test data added successfully!')