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
from .forms import LoginForm,ResetpwdForm,ResetEmailForm
from .models import CMSUser,CMSPersmission
from .decorators import login_required,permission_required
import config
from exts import db,mail
from flask_mail import Message
from utils import restful,cache
import string,random
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

@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error('请输入邮箱')
    source = list(string.ascii_letters)
    source.extend(map(lambda x:str(x),range(0,10)))
    captcha =  "".join(random.sample(source,6))
    message = Message('bbs 邮箱验证码',recipients=[email],body='您的验证码是：%s' %captcha)
    try:
        mail.send(message)
    except:
        return restful.server_error()
    cache.set(email,captcha)
    return restful.success()


@bp.route('/mail/')
def send_email():
    message = Message('发送邮件测试',recipients=['qqq499634750@163.com'],body='测试')
    mail.send(message)
    return '成功'
#定义login get请求和post请求  继承 views的methoview


@bp.route('/posts/')
@login_required
@permission_required(CMSPersmission.POSTER)
def posts():
    return render_template('cms/cms_posts.html')
@bp.route('/comments/')
@login_required
@permission_required(CMSPersmission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')
@bp.route('/boards/')
@login_required
@permission_required(CMSPersmission.BOARDER)
def boards():
    return render_template('cms/cms_boards.html')
@bp.route('/fusers/')
@login_required
@permission_required(CMSPersmission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')
@bp.route('/cusers/')
@login_required
@permission_required(CMSPersmission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')
@bp.route('/croles/')
@login_required
@permission_required(CMSPersmission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')


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
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            print(email)
            g.cms_user.email = email
            # db.session.add()
            db.session.commit()
            return restful.success()
        else:
            print('1111')
            return restful.params_error(form.get_error())


bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
#将loginview绑定到login

bp.add_url_rule('/resetpwd/',view_func=ResetpwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=ResetEmailView.as_view('resetemail'))