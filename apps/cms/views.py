#encoding:utf-8

from flask import (
    Blueprint,
    render_template,
    views,
    request,
    session,
    redirect,
    url_for,
    g,
    jsonify
)
from .forms import LoginForm,ResetpwdForm
from .models import CMSUser
from .decorators import login_required
import config
from exts import db,mail
from flask_mail import Message
from utils import restful
bp = Blueprint("cms",__name__,url_prefix='/cms')
#subdomain'cms' 子域名
#url_prefix  后缀

@bp.route('/')
@login_required
#装饰器 如果没有登陆 无法访问cms主页 并跳转到login页面
def index():
    return render_template('cms/cms_index.html')
@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))

@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')

@bp.route('/mail/')
def send_email():
    message = Message('发送邮件测试',recipients=['qqq499634750@163.com'],body='测试')
    mail.send(message)
    return '成功'
#定义login get请求和post请求  继承 views的methoview
class LoginView(views.MethodView):
    def get(self,message=None):
       return render_template('cms/cms_login.html',message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    #如果设置perment session过期时间为31天
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或用户名错误')

        else:
            # print(form.errors)
            # {'password': ['请输入正确格式的密码']} popitem 取字典中的第一个 然后列表中的第0个值
            message = form.get_error()
            return  self.get(message=message)

class ResetpwdView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetpwd.html')
    def post(self):
        # form = ResetpwdForm(request.form)
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # return jsonify({"code":200,"message":"修改成功"})
                return restful.success()
            else:
                return restful.params_error("旧密码错误")
                # return jsonify({"code":400,"message":"旧密码错误"})
        else:
            print('11111')
            message = form.get_error()
            return restful.params_error(message)


class ResetEmailView(views.MethodView):
    decorators = [login_required]
    def get(self):
       return render_template('cms/cms_resetemail.html')
    def post(self):
        pass


bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
#将loginview绑定到login

bp.add_url_rule('/resetpwd/',view_func=ResetpwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=ResetEmailView.as_view('resetemail'))