# url+视图函数
from django.core import paginator
from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from .models import *

blog = Blueprint('blog', __name__)
admin = Blueprint('admin', __name__)


@blog.route('/')
def home():
    return 'HOME'

##################################################################################
##后台
##################################################################################
#后台登录
@admin.route('/login/',methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        # 接收客户端数据
        username = request.form.get('username')
        password = request.form.get('userpwd')
        # 判断？是否成功
        if username == 'song' and password == '123':
            res = redirect(url_for('admin.admin_index'))
            # 获取cookie:通过key,获取value
            res.set_cookie('user',username)


            # 获取session，
            # session['user'] = username
            # session['username'] = username
            print(username)
            print(res)
            return res
        return '登录失败！'
    return render_template('admin/login.html')

#退出登录，注销cookie
@admin.route('/logout/')
def admin_logout():
    res = redirect(url_for('admin.admin_login'))
    #获取cookie，并删除key:pop,删除当前。clear清空所有
    res.delete_cookie('username')

    # 获取session，并删除session
    # session.pop('user')
    return res



# 管理首页
@admin.route('/admin/')
def admin_index():
    # 获取cookie
    # # 获取当前登录用户
    count =len(Article.query.all())
    username = request.cookies.get('user','')

    # 获取session
    # username = session.get('user','')
    print(username)
    if username == '':
        res  = redirect(url_for('admin.admin_login'))
        return res
    data = {
        'count':count,
        'username':username,
    }
    print(1111)
    print(count)
    print(username)
    return render_template('admin/index.html',**data)   #Flask 多个传参 **data  单个参数data=data


# 文章管理
@admin.route('/article/',methods=['GET','POST'])
def admin_article():
    #获取当前登录用户
    username = request.cookies.get('user','')
    print(1111111)
    print(username)
    if username == '':
        abort(403)
        res = redirect(url_for('admin.admin_login'))
        return res

    return redirect(url_for('admin.admin_article_page',page=1))
#后台文章分页表：
@admin.route('/article/<int:page>/')
def admin_article_page(page):
    per_page = 4        #初始化，每页显示2条数据
    if not page: # 如果前端没有传参，默认就是第一页page = 1，
        page = 1
    articles = Article.query.all()
    articles = articles[(page-1)*per_page:page*per_page]
    my_pageinate = Article.query.order_by('id').paginate(page=page,per_page=per_page)
    username = request.cookies.get('user','')
    data = {
        'articles': articles,
        'my_pageinate':my_pageinate,
        'username':username,
    }
    # print(articles[0].my_article.name,type(articles[0]))   #通过外键，找到对象中的字段名称 name
    return render_template('admin/article.html',**data)



# 增加文章链接
@admin.route('/addarticle/',methods = ['POST','GET'])
def admin_addarticle():
    # return render_template('admin/add-article.html')
    #获取属性表中所有字段
    articletypes = Articletype.query.all()
    username = request.cookies.get('user','')
    if username == '':
        return redirect(url_for('admin.admin_login'))
    if request.method =='POST':
        # 获取前端数据
        title = request.form.get('title')
        text = request.form.get('content')
        keyword = request.form.get('keywords')
        describe =request.form.get('describe')
        typename = request.form.get('category')
        label = request.form.get('tags')
        img = request.form.get('titlepic')
        data = request.form.get('data')

        # 创建对象Article
        a = Article()
        a.title = title
        a.text = text
        a.keyword =keyword
        a.describe = describe
        a.articletypeid = typename
        a.label = label
        a.img = img
        a.data = data
        db.session.add(a)
        db.session.commit()
        res = redirect(url_for('admin.admin_addarticle'))
        return res
    data ={
        'articletypes':articletypes,
        'username':username,
    }
    return render_template('admin/add-article.html',**data)


# 栏目管理
@admin.route('/category/',methods = ['GET','POST'])
def admin_category():
    articletypes = Articletype.query.all()
    username = request.cookies.get('user','')
    if username == '':
        res = redirect('admin.admin_login')
        return res
    if request.method == 'POST':
        name = request.form.get('name')
        alias =request.form.get('alias')
        fid = request.form.get('fid')
        keywords = request.form.get('keywords')
        describe = request.form.get('describe')
        print(name)
        #创建对象：Articletype
        articletype = Articletype()
        articletype.name = name
        articletype.alias = alias
        articletype.parentnode =fid
        articletype.keyword = keywords
        articletype.describe = describe
        db.session.add(articletype)
        db.session.commit()
        res = redirect(url_for('admin.admin_category'))
        return res
    data = {
       'articletypes':articletypes,
        'username':username
    }
    return render_template('admin/category.html',**data)


# 公告管理
@admin.route('/notice/',methods = ['GET','POST'])
def admin_notice():
    #获取数据库的信息

    return redirect(url_for('admin.admin_notice_page',page=1))

#公告分页
@admin.route('/notice/<int:page>/')
def admin_notice_page(page):
    per_page = 3
    if  not page:
        page = 1
    articles = Article.query.all()
    articles = articles[(page-1)*per_page:page*per_page]
    my_paginate = Article.query.order_by('id').paginate(page=page,per_page=per_page)
    username = request.cookies.get('user', '')
    if username == '':
        res = redirect('admin.admin_login')
        return res
    data = {
        'articles': articles,
        'username': username,
        'my_paginate':my_paginate
    }
    return render_template('admin/notice.html',**data)


# 增加公告
@admin.route('/addnotice/',methods = ['GET',"POST"])
def admin_addnotice():
    articles = Article.query.all()
    username = request.cookies.get('user','')
    if  username == '':
        res = redirect(url_for('admin.admin_login'))
        return res
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        keywords = request.form.get('keywords')
        describe = request.form.get('describe')
        #创建对象Article
        a = Article()
        a.title = title
        a.text = content
        a.keyword = keywords
        a.describe =describe
        db.session.add(a)
        db.session.commit()
        res = redirect(url_for('admin.admin_addnotice'))
        return res
    data = {
        'username':username,
        'articles':articles,
    }
    return render_template('admin/add-notice.html',**data)

# 评论管理
@admin.route('/comment/')
def admin_comment():
    return render_template('admin/comment.html')

# 用户管理
@admin.route('/manageuser/')
def admin_manageuser():
    return render_template('admin/manage-user.html')

# 管理登录日志
@admin.route('/loginlog/')
def admin_loginlog():
    return render_template('admin/loginlog.html')

# 基本设置
@admin.route('/setting/')
def admin_setting():
    return render_template('admin/setting.html')

# 阅读设置
@admin.route('/readset/')
def admin_readset():
    return render_template('admin/readset.html')

# 友情链接
@admin.route('/flink/')
def admin_flink():
    return render_template('admin/flink.html')

# 增加友情链接
@admin.route('/addflink/')
def admin_addflink():
    return render_template('admin/add-flink.html')


##################################################################################
##前台
##################################################################################
#首页
@blog.route('/index/')
def index():
    articles = Article.query.all()
    articletypes = Article.query.all()
    data = {
        'articles':articles,
        'articletypes':articletypes,
    }
    return render_template('blog/index.html',**data)
# # 网站首页
# @blog.route('/index/')
# def index():
#     return redirect(url_for('blog.index_page',page =1))

# # 首页分页：
# @blog.route('/index/<int:page>')
# def index_page(page):
#     per_page = 3
#     if not page:
#         page = 1
#     articles = Article.query.all()
#     articletypes = Articletype.query.all()
#     #获取得到所有数据，套用分页公式
#     articles = articles[(page-1)*per_page:page:per_page]
#     #分页完成，排序order_by(),获取页数page  每页数量per_page
#     my_paginate = Article.query.order_by('id').paginate(page = page,per_page = per_page)
#     data ={
#         'articles':articles,
#         'articletypes':articletypes,
#         'my_paginate':my_paginate,
#     }
#     return render_template('blog/index.html',**data)




# 首页分页：

#文章分类表
@blog.route('/articletype/<int:articletypeid>/')
def Article_type(articletypeid):
    articletypes = Articletype.query.all()  #获取类型表所有数据
    articles = Articletype.query.get(articletypeid).articles   #获取类型表关联的文章
    return render_template('blog/index.html',articletypes=articletypes,articles=articles)



# 我的相册
@blog.route('/share/')
def share():
    return render_template('blog/share.html')

# 我的日记
@blog.route('/list/')
def list():
    return render_template('blog/list.html')

# 关于我
@blog.route('/about/')
def about():
    articletypes = Articletype.query.all()  #获取类型表所有数据
    return render_template('blog/about.html',articletypes=articletypes)

# 留言
@blog.route('/gbook/')
def gbook():
    return render_template('blog/gbook.html')

# 内容页
@blog.route('/info/')
def info():
    return render_template('blog/info.html')

# 内容页
@blog.route('/infopic/')
def infopic():
    return render_template('blog/infopic.html')

# 添加文章数据
# @blog.route('/addarticle/')
# def add_article():
#     #添加数据，创建对象
#     a = Article()
#     a.title  = '生命终结的末端，苦短情长'
#     a.text = '天朝羽打开一扇窗，我不曾把你想得平常。看季节一一过往。'
#     a.img = 'App/static/blog/images/7.jpg'
#     try:
#         db.session.add(a)
#         db.session.commit()
#     except:
#         db.session.rollback()
#         db.session.flush()
#         return 'fail'
#     return 'success'

