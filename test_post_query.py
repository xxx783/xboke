from app import app, db, Post

with app.app_context():
    # 直接测试Post.query.all()
    posts = Post.query.all()
    print(f'Direct query - Total posts: {len(posts)}')
    for post in posts:
        print(f'Post: {post.title}, Author ID: {post.user_id}')
        
    # 测试排序查询
    ordered_posts = Post.query.order_by(Post.date_posted.desc()).all()
    print(f'Ordered query - Total posts: {len(ordered_posts)}')
    for post in ordered_posts:
        print(f'Post: {post.title}, Date: {post.date_posted}')