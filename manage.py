from nowstagram import app, db
from sqlalchemy import  or_,and_
import random,os,uuid,json
from flask_script import Manager
from  nowstagram.models import User,Image,Comment
from nowstagram.qiniusdk import upload_localfile
# Terminal :python manage.py init_database
manager = Manager(app)

@manager.command
#python manage.py init_database_king
def init_database_king():
    urls=get_upload_url()
    print(urls)
    db.drop_all()
    db.create_all()
    with open('.\herolist.json', 'r', encoding='utf-8') as ff:
        jsonFile = json.load(ff)
    #print(jsonFile)
    n=0
    for i in range(0,len(jsonFile)):
        #英雄编号
        eName = jsonFile[i]['ename']
        # 英雄名字
        cName = jsonFile[i]['cname']
        title = jsonFile[i]['title']
        skinName = jsonFile[i]['skin_name']
        skinName = skinName.split("|")
        # 皮肤数量
        skin_numbers = len(skinName)

        print( str(eName)+cName+title+str(skin_numbers))

        db.session.add(User(cName, 'herorobort'))#账号密码
        for j in range(1, skin_numbers + 1):
            pictureUrl = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/' + str(eName) + '/' + str(eName) + '-bigskin-' + str(j) + '.jpg'
            db.session.add(Image(pictureUrl, i + 1))
            n=n+1
            db.session.add(Comment(skinName[j-1], n, i + 1))
    db.session.commit()




def get_image_url():
    #生成随机头像
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'

@manager.command
def run_test():
    #init_database()
    db.drop_all()
    db.create_all()
    tests = unittest.TestLoader().discover('./')
    unittest.TextTestRunner().run(tests)

@manager.command
    #python manage.py upload_local_to_qiniu
def upload_local_to_qiniu():
    path = os.getcwd() + "\King\\"
    print(path)
    for root, dirs, files in os.walk(path):
        for source_file in files:
            #print(source_file)
            file_ext = ''
            if source_file.find('.') > 0:
                file_ext =source_file.rsplit('.', 1)[1].strip().lower()

            source_file=path+source_file
            print(source_file)
            save_file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
            print(save_file_name)
            url = upload_localfile(source_file,save_file_name)
            print(url)

def get_upload_url():
    urls=[]
    path = os.getcwd() + "\King\\"
    print(path)
    for root, dirs, files in os.walk(path):
        for source_file in files:
            #print(source_file)
            file_ext = ''
            if source_file.find('.') > 0:
                file_ext = source_file.rsplit('.', 1)[1].strip().lower()

            source_file = path + source_file
            #print(source_file)
            save_file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
            #print(save_file_name)
            url = upload_localfile(source_file, save_file_name)
            #print(url)
            urls.append(url)
    return urls

@manager.command
#python manage.py init_database
def init_database():
    urls=get_upload_url()
    un=0
    db.drop_all()
    db.create_all()
    for i in range(0, 3):
        db.session.add(User('user' + str(i + 1), 'a' + str(i + 1)))
        for j in range(0, 3):
            if un<len(urls):
                db.session.add(Image(get_image_url(), i + 1))
                un=un+1
                for k in range(0, 5):
                    db.session.add(Comment('hello' + str(k), 1 + 3 * i + j, i + 1))

    db.session.commit()


@manager.command
#python manage.py init_database
def init_database():
    urls=get_upload_url()
    un=0
    db.drop_all()
    db.create_all()
    for i in range(0, 3):
        db.session.add(User('user' + str(i + 1), 'a' + str(i + 1)))
        for j in range(0, 3):
            if un<len(urls):
                db.session.add(Image(get_image_url(), i + 1))
                un=un+1
                for k in range(0, 5):
                    db.session.add(Comment('hello' + str(k), 1 + 3 * i + j, i + 1))

    db.session.commit()

#     for i in range(1,16):
#         user=User.query.get(i)
#         user.username='[new]'+user.username
#     db.session.commit()
#     for i in range(20,30):
#         #User.query.filter_by(id=i).update({'username':'[new2]'+str(i)})
#         User.query.filter_by(id=i + 1).update({'username': '[new2]' + str(i)})
#     db.session.commit()
# #两种删除
#     for j in range(20,30):
#         comment=Comment.query.get(j)
#         db.session.delete(comment)
#         #print(1,comment)
#     db.session.commit()
#
#     for j in range(40,50):
#         Comment.query.filter_by(id =j).delete()
#     db.session.commit()

    #查询全部
    # print(1,User.query.all())
    # #查主键
    # print(2,User.query.get(3))
    # #first第一个
    # print(3,User.query.filter_by(id=5).first())
    # #order_by 排序 desc 倒序 offset 偏移量 limit 数量
    # print(4,User.query.order_by(User.id.desc()).offset(1).limit(2).all())
    # #以什么结尾（开始）
    # print(5,User.query.filter(User.username.endswith('0')).limit(3).all())
    # #多条件_and _or (需要导入)
    # print(6,User.query.filter(or_(User.id==88,User.id==99)).all())
    # print(7, User.query.filter(and_(User.id > 88, User.id < 99)).all())
    # #分页 第i页 每页 j条
    # print(8,User.query.paginate(page=2,per_page=10).items)
    # print(9, User.query.order_by(User.id.desc()).paginate(page=1, per_page=10).items)

    # print(10, User.query.get(3).images.all())
    # #backref
    # print(11, Image.query.get(1).user)
    # print(12,Image.query().get(1).comments.all())

if __name__ == '__main__':
    manager.run()
