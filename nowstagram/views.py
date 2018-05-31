#-*- encoding=UTF-8 -*-

from nowstagram import app,db
from flask import render_template, redirect, request, flash,get_flashed_messages,send_from_directory
from nowstagram.models import Image,User,Comment
import random, hashlib, json, uuid, os
from flask_login import login_user,logout_user,login_required,current_user
from nowstagram.qiniusdk import qiniu_upload_file

@app.route('/')
def index():
    #首页
    images = Image.query.order_by(db.desc(Image.id)).limit(10).all()
    return render_template('index.html', images=images)

# 首页ajax 的json 数据
@app.route('/index/images/<int:page>/<int:per_page>/')
def index_images(page, per_page):
    paginate = Image.query.order_by(db.desc(Image.id)).paginate(page=page, per_page=per_page, error_out=False)
    map = {'has_next': paginate.has_next}
    images = []
    for image in paginate.items:
        comments = []
        for i in range(0, min(2, len(image.comments))):
            comment = image.comments[i]
            comments.append({'username':comment.user.username,
                             'user_id':comment.user_id,
                             'content':comment.content})
        imgvo = {'id': image.id,
                 'url': image.url,
                 'comment_count': len(image.comments),
                 'user_id': image.user_id,
                 'head_url':image.user.head_url,
                 'created_date':str(image.created_date),
                 'comments':comments}
        images.append(imgvo)

    map['images'] = images
    return json.dumps(map)


@app.route('/image/<int:image_id>/')
def image(image_id):
    image=Image.query.get(image_id)
    if image==None:
        return redirect('/')
    return render_template('pageDetail.html',image=image)

@app.route('/profile/<int:user_id>/')
@login_required
#个人详情页
def profile(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect('/')
    paginate=Image.query.filter_by(user_id=user_id).order_by(db.desc(Image.created_date)).paginate(page=1,per_page=3,error_out=False)
    return render_template('profile.html', user = user,images=paginate.items,has_next=paginate.has_next)

@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
#个人详情页ajax请求json
def user_images(user_id,page,per_page):
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    map={'has_next':paginate.has_next}
    images=[]
    for image in paginate.items:
        imgvo={'id':image.id,'url':image.url,'comment_count':len(image.comments)}
        images.append(imgvo)
    map['images']=images
    return json.dumps(map)

#登录注册页
@app.route('/regloginpage/')
def regloginpage():
    msg=''
    for m in get_flashed_messages(with_categories=False, category_filter=['reglogin']):
        #catetgory_filter 过滤相关消息
        msg = msg + m
    return render_template('login.html',msg=msg,next=request.values.get('next'))

#携带flash信息跳转到某个页面
def redirect_with_msg(target, msg, category):
    if msg != None:
        flash(msg, category=category)
    return redirect(target)

@app.route('/login/',methods={'post','get'})
def login():
    #注册账号
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    if username == '' or password == '':
        return redirect_with_msg('/regloginpage', '用户名和密码不能为空', 'reglogin')

    user=User.query.filter_by(username=username).first()
    if user==None:
        return redirect_with_msg('/regloginpage', '用户名不存在', 'reglogin')

    m=hashlib.md5()
    m.update((password + user.salt).encode("gbk"))
    if m.hexdigest()!=user.password:
        return redirect_with_msg('/regloginpage', '密码错误', 'reglogin')

    login_user(user)

    next = request.values.get('next')
    if next != None and next.startswith('/') > 0:
        return redirect(next)

    return redirect('/')

@app.route('/reg/',methods={'post','get'})
def reg():
    #注册账号
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    if username == '' or password == '':
        return redirect_with_msg('/regloginpage', '用户名和密码不能为空', 'reglogin')

    user= User.query.filter_by(username=username).first()
    if user != None:
        return redirect_with_msg('/regloginpage', '用户名已存在', 'reglogin')
    #更多判断

    salt = '.'.join(random.sample('0123456789abcde', 5))
    m = hashlib.md5()
    m.update((password + salt).encode("gbk"))
    password = m.hexdigest()
    user = User(username, password, salt)
    db.session.add(user)
    db.session.commit()
    login_user(user)

    next = request.values.get('next')
    if next != None and next.startswith('/') > 0:
        return redirect(next)

    return redirect('/')

@app.route('/logout/')
def logout():
    #退出登录
    logout_user()
    return redirect('/')

def save_to_local(file, file_name):
    save_dir = app.config['UPLOAD_DIR']
    file.save(os.path.join(save_dir, file_name))
    return '/image/' + file_name

def save_to_qiniu(file, file_name):
    return qiniu_upload_file(file, file_name)

@app.route('/upload/', methods={"post"})
@login_required
def upload():
    file = request.files['file']
    file_ext = ''
    if file.filename.find('.') > 0:
        file_ext = file.filename.rsplit('.', 1)[1].strip().lower()
    if file_ext in app.config['ALLOWED_EXT']:
        file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
        url = qiniu_upload_file(file, file_name)
        #url = save_to_local(file, file_name)
        if url != None:
            print(url)
            print(current_user.id)
            db.session.add(Image(url, current_user.id))
            db.session.commit()

    return redirect('/profile/%d' % current_user.id)

@app.route('/image/<image_name>')
def view_image(image_name):
    return send_from_directory(app.config['UPLOAD_DIR'], image_name)

@app.route('/addcomment/', methods={'post'})
@login_required
def add_comment():
    image_id = int(request.values['image_id'])
    content = request.values['content']
    comment = Comment(content, image_id, current_user.id)
    db.session.add(comment)
    db.session.commit()
    return json.dumps({"code":0, "id":comment.id,
                       "content":comment.content,
                       "username":comment.user.username,
                       "user_id":comment.user_id})


