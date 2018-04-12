#encoding:utf-8

from flask import Blueprint

bp = Blueprint("cms",__name__,url_prefix='/cms')
#subdomain'cms' 子域名
#url_prefix  后缀

@bp.route('/')
def index():
    return "cms index"