# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request, flash, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, RadioField
from wtforms.validators import InputRequired, Length, EqualTo
from passlib.hash import sha256_crypt
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 数据库模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(100), default='default.jpg')
    bio = db.Column(db.Text, default='')
    theme_preference = db.Column(db.String(10), default='light')  # light, dark, system
    blur_effect_enabled = db.Column(db.Boolean, default=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    is_default = db.Column(db.Boolean, default=False)
    primary_color = db.Column(db.String(20), nullable=False)
    secondary_color = db.Column(db.String(20), nullable=False)
    accent_color = db.Column(db.String(20), nullable=False)
    background_color = db.Column(db.String(20), nullable=False)
    text_color = db.Column(db.String(20), nullable=False)
    text_secondary = db.Column(db.String(20), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    comment_count = db.Column(db.Integer, default=0)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    is_pinned = db.Column(db.Boolean, default=False)

# 表单类
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[InputRequired()])
    submit = SubmitField('Post')

from flask_wtf.file import FileField, FileAllowed

class SettingsForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    bio = TextAreaField('个人简介', validators=[Length(max=500)])
    profile_picture = FileField('头像上传', validators=[FileAllowed(['jpg', 'jpeg', 'png'], '图片文件！')])
    blur_effect = BooleanField('开启毛玻璃效果', default=True)
    theme_preference = RadioField('主题模式', choices=[
        ('light', '浅色模式'),
        ('dark', '深色模式'),
        ('system', '跟随系统')
    ], default='light')
    submit = SubmitField('保存设置')

class PasswordForm(FlaskForm):
    current_password = PasswordField('当前密码', validators=[InputRequired()])
    new_password = PasswordField('新密码', validators=[InputRequired(), Length(min=8, max=20)])
    confirm_new_password = PasswordField('确认新密码', validators=[InputRequired(), EqualTo('new_password')])
    submit = SubmitField('修改密码')

class CommentForm(FlaskForm):
    content = TextAreaField('评论内容', validators=[InputRequired(), Length(min=1, max=500)])
    submit = SubmitField('发表评论')

# 路由
@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        posts = Post.query.filter_by(author=current_user).order_by(Post.date_posted.desc()).all()
    else:
        posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = sha256_crypt.hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and sha256_crypt.verify(form.password.data, user.password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    settings_form = SettingsForm(prefix='settings')
    password_form = PasswordForm(prefix='password')
    
    import secrets
    import os
    from PIL import Image
    
    # 头像保存路径
    UPLOAD_FOLDER = 'static/profile_pics'
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    if request.method == 'GET':
        settings_form.username.data = current_user.username
        settings_form.bio.data = current_user.bio
        settings_form.blur_effect.data = current_user.blur_effect_enabled
        settings_form.theme_preference.data = current_user.theme_preference
    
    if settings_form.validate_on_submit():
        # 处理头像上传
        if settings_form.profile_picture.data:
            # 生成随机文件名
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(settings_form.profile_picture.data.filename)
            picture_fn = random_hex + f_ext
            picture_path = os.path.join(app.root_path, UPLOAD_FOLDER, picture_fn)
            
            # 调整图片大小
            output_size = (200, 200)
            i = Image.open(settings_form.profile_picture.data)
            i.thumbnail(output_size)
            i.save(picture_path)
            
            # 删除旧头像（如果不是默认头像）
            if current_user.profile_picture != 'default.jpg':
                old_picture_path = os.path.join(app.root_path, UPLOAD_FOLDER, current_user.profile_picture)
                if os.path.exists(old_picture_path):
                    os.remove(old_picture_path)
            
            current_user.profile_picture = picture_fn
        
        # 检查用户名是否已被使用
        if settings_form.username.data != current_user.username and User.query.filter_by(username=settings_form.username.data).first():
            flash('用户名已被使用', 'danger')
        else:
            current_user.username = settings_form.username.data
            current_user.bio = settings_form.bio.data
            current_user.blur_effect_enabled = settings_form.blur_effect.data
            current_user.theme_preference = settings_form.theme_preference.data
            db.session.commit()
            flash('设置已保存', 'success')
            return redirect(url_for('settings'))
    
    if password_form.validate_on_submit():
        # 验证当前密码
        if not sha256_crypt.verify(password_form.current_password.data, current_user.password):
            flash('当前密码错误', 'danger')
        else:
            current_user.password = sha256_crypt.hash(password_form.new_password.data)
            db.session.commit()
            flash('密码已修改', 'success')
            return redirect(url_for('settings'))
    
    # 获取所有主题
    themes = Theme.query.all()
    
    return render_template('settings.html', settings_form=settings_form, password_form=password_form, themes=themes)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', form=form, legend='New Post')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', form=form, legend='Update Post')

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route('/user_profile/<int:user_id>')
@login_required
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).all()
    return render_template('user_posts.html', user=user, posts=posts)

@app.route('/user/<string:username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).all()
    return render_template('user_posts.html', posts=posts, user=user)

@app.route('/admin')
@login_required
def admin():
    if current_user.username != 'admin':
        abort(403)
    users = User.query.all()
    posts = Post.query.all()
    return render_template('admin.html', users=users, posts=posts)

@app.route('/community')
def community():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('community.html', posts=posts)

@app.route('/community/post/<int:post_id>', methods=['GET', 'POST'])
def community_post(post_id):
    post = Post.query.get_or_404(post_id)
    comment_form = CommentForm()
    
    if comment_form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(content=comment_form.content.data, author=current_user, post=post)
        db.session.add(comment)
        
        # 更新评论计数
        post.comment_count = Comment.query.filter_by(post_id=post.id).count()
        db.session.commit()
        
        flash('评论已发表', 'success')
        return redirect(url_for('community_post', post_id=post.id))
    
    # 获取所有评论
    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.is_pinned.desc(), Comment.date_posted.desc()).all()
    
    return render_template('community_post.html', title=post.title, post=post, comment_form=comment_form, comments=comments)

# API路由 - 更新主题设置
@app.route('/api/update-theme', methods=['POST'])
@login_required
def update_theme():
    data = request.get_json()
    theme = data.get('theme')
    
    if theme in ['light', 'dark']:
        current_user.theme = theme
        db.session.commit()
        return jsonify({'status': 'success', 'theme': theme})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid theme'}), 400

@app.route('/api/update-blur-effect', methods=['POST'])
@login_required
def update_blur_effect():
    data = request.get_json()
    blur_effect = data.get('blur_effect')
    
    if isinstance(blur_effect, bool):
        current_user.blur_effect = blur_effect
        db.session.commit()
        return jsonify({'status': 'success', 'blur_effect': blur_effect})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid blur_effect value'}), 400

@app.route('/api/update-theme-preference', methods=['POST'])
@login_required
def update_theme_preference():
    data = request.get_json()
    theme_preference = data.get('theme_preference')
    
    if theme_preference in ['light', 'dark', 'system']:
        current_user.theme_preference = theme_preference
        db.session.commit()
        return jsonify({'status': 'success', 'theme_preference': theme_preference})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid theme_preference'}), 400

@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post_id
    
    # 只有评论作者或管理员可以删除评论
    if current_user.id != comment.user_id and current_user.username != 'admin':
        abort(403)
    
    db.session.delete(comment)
    
    # 更新评论计数
    post = Post.query.get(post_id)
    post.comment_count = Comment.query.filter_by(post_id=post_id).count()
    db.session.commit()
    
    flash('评论已删除', 'success')
    return redirect(url_for('community_post', post_id=post_id))

@app.route('/comment/<int:comment_id>/pin', methods=['POST'])
@login_required
def pin_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post_id
    
    # 只有文章作者或管理员可以置顶评论
    post = Post.query.get(post_id)
    if current_user.id != post.user_id and current_user.username != 'admin':
        abort(403)
    
    comment.is_pinned = not comment.is_pinned
    db.session.commit()
    
    action = '置顶' if comment.is_pinned else '取消置顶'
    flash(f'评论已{action}', 'success')
    return redirect(url_for('community_post', post_id=post_id))

if __name__ == '__main__':
    with app.app_context():
        # 更新数据库结构，添加新字段
        db.create_all()
        
        # 检查并更新管理员用户，确保新字段有值
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_password = sha256_crypt.hash('admin123')
            admin_user = User(username='admin', password=admin_password, bio='网站管理员')
            db.session.add(admin_user)
            db.session.commit()
        else:
            # 确保现有用户有默认值
            if admin_user.bio is None:
                admin_user.bio = '网站管理员'
                db.session.commit()
        
        # 检查并添加示例文章
        if not Post.query.first():
            sample_post = Post(
                title='关于拥有一辆车的思考',
                content='已经起床，可身体还未苏醒。其实如果早起出门跑个步是很好的一个选择。在这样的清晨，在广州还有些热，或许需要更早一些。看看不同上班时那炙热的阳光。还可以呼吸下或许不够新鲜的城市晨光空气。\n\n要不去偏离城市更远一点的地方跑步？离我现在住的不远其实就有这样一个地方。那里有很大的小区，有大道，现在还是道路的尽头。或许为了以后不久的时间拓展为车水马龙的街道，但是现在还没有。崭新的道路，稀少的行人，几乎没有车辆。只有路尽头边上停放了好多私家车。\n\n我还没有属于自己的小车。其实总间隔一段时间我就有欲望自己能拥有一台属于自己的车。这段时间往往是在老家。老家虽是在村里，但现在四通的都是宽宽的水泥路。在家没有车去哪都不方便。以前有拉客的三轮，去镇上很方便，现在母亲有时候实在没有人载她一程还会走路去镇上，跟我还很小时候一样。我妈不会骑电动车。电动车家里有，是妹妹买的。\n\n每年回家，总会由于没有车错过一些事情似的。同学群里约的聚会、亲戚家走走...甚至是时同学朋友都跟我说："你该有辆车，没有房子这车还是要有的，平时带个女孩，她都更愿意跟你接触。"每每在家我都会有几天的动摇。\n\n其实我总有另一个想法，我出了门来广州打工。用车的需求不大。大城市道路虽宽广，可是公共交通更适合我这随性的人。即便是只坐地铁去哪也都方便。出了地铁即使离目的地还有一段距离。这共享单车不就派上用场了。\n\n我有一辆美利达公爵山地车。19寸的架子，现在是我的上下班代步工具，去公司现在只有3公里的路程。骑车只需要十几分钟。骑车很方便。偶而周末也会骑，边骑车边听电台。这两年听歌很少，倒是很喜欢听电台。听几个会说话的人聊各种话题的电台。就边听边漫无目的的骑车，或许去城市中心，或许去城市边缘，很适合我。\n\n我想，如果我有车了，我会周末开车去哪哪吗？或许能远远扩大我的活动范围。但骑行我可以漫无目的去任何可以去的地方，不管道路好坏，不管道路限行、拥挤，不考虑停车，不考虑消耗，用钱就是个大问题，出门没目的的瞎逛还花钱，还有还有还能当作锻炼，还有还能随时停下来看看。当然有车有更多可能。我现在还没有，我设想有些狭隘。',
                author=admin_user
            )
            db.session.add(sample_post)
            db.session.commit()
    app.run(debug=True)