#encoding:utf-8

from flask import g
from wtforms import Form,StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo
from apps.forms import BaseForm
from utils import cache
from wtforms import ValidationError

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'),InputRequired(message='请输入邮箱！')])
    password = StringField(validators=[Length(6,20,message='请输入正确格式的密码')])
    remember = IntegerField()

class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,20,message='请输入正确格式的旧密码')])
    newpwd = StringField(validators=[Length(6,20,message='请输入正确格式的新密码')])
    newpwd2 = StringField(validators=[EqualTo("newpwd",message='确认密码和新密码保持一致')])

class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确格式的邮箱")])
    captcha = StringField(validators=[Length(min=6,max=6,message='请输入正确长度的验证码！')])

    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_cache = cache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误')

    def validate_email(self,field):
        email = self.email
        user = g.cms_user
        if user.email == email:
            raise ValidationError('原邮箱和修改邮箱一致！')