#encoding:utf-8

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from flask_bbs import create_app
from exts import db
from apps.cms import models as cms_modles
from apps.front import models as front_modles


CMSRole = cms_modles.CMSRole
CMSPermission = cms_modles.CMSPersmission

app = create_app()
CMSUser = cms_modles.CMSUser
manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)

FrontUser = front_modles.FrontUser

@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功')

@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_to_role(email,name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('用户添加到角色成功！')
        else:
            print('没有这个角色：%s'%role)
    else:
        print('没有这个邮箱：%s'%email)

@manager.command
def create_role():
    #1访问者 只能修改个人信息 其余的都不能进行修改
    visitor = CMSRole(name='访问者',desc='只能访问，不能修改')
    visitor.permissions = CMSPermission.VISITOR
    #2运营人员可以修改个人信息 可以管理帖子和评论
    operator = CMSRole(name='运营',desc='管理帖子和评论管理前台用户')
    operator.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.CMSUSER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER
    #3管理员 拥有绝大部分的权限 不能同级管理
    admin = CMSRole(name='管理员',desc='拥有本系统所有权限')
    admin.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.CMSUSER|CMSPermission.COMMENTER|CMSPermission.BOARDER|CMSPermission.FRONTUSER
    #4开发者
    developer = CMSRole(name='开发者',desc='开发人员专用')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor,operator,admin,developer])
    db.session.commit()

@manager.option('-t','--telephone',dest='telephone')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
def create_front_user(telephone,username,password):
    user = FrontUser(telephone=telephone,username=username,password=password)
    db.session.add(user)
    db.session.commit()



@manager.command
def test_permission():
    user = CMSUser.query.first()
    if user.has_permission(CMSPermission.VISITOR):
        print('这个用户有访问者的权限')
    else:
        print('这个用户没有访问者权限')

if __name__ == '__main__':
    manager.run()