from nowstagram import app, db
from sqlalchemy import  or_,and_
import random
from flask_script import Manager
from  nowstagram.models import User,Image,Comment
# Terminal :python manage.py init_database
manager = Manager(app)


def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'


@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(0, 100):
        db.session.add(User('user' + str(i + 1), 'a' + str(i + 1)))
        for j in range(0, 7):
            db.session.add(Image(get_image_url(), i + 1))
            for k in range(0, 3):
                db.session.add(Comment('hello' + str(k), 1 + 7 * i + j, i + 1))

    db.session.commit()

    for i in range(1,16):
        user=User.query.get(i)
        user.username='[new]'+user.username
    db.session.commit()
    for i in range(20,30):
        #User.query.filter_by(id=i).update({'username':'[new2]'+str(i)})
        User.query.filter_by(id=i + 1).update({'username': '[new2]' + str(i)})
    db.session.commit()
#两种删除
    for j in range(20,30):
        comment=Comment.query.get(j)
        db.session.delete(comment)
        #print(1,comment)
    db.session.commit()

    for j in range(40,50):
        Comment.query.filter_by(id =j).delete()
    db.session.commit()

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
