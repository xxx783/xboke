from app import app, db, User, Post

with app.app_context():
    # 检查用户数量
    users = User.query.all()
    print(f'Total users: {len(users)}')
    
    # 打印所有用户信息
    for user in users:
        print(f'User: {user.username}, ID: {user.id}')
    
    # 检查文章数量
    posts = Post.query.all()
    print(f'Total posts: {len(posts)}')
    
    # 打印所有文章信息
    for post in posts:
        print(f'Post: {post.title}, Author ID: {post.user_id}')