import os
import sys
import json
from io import BytesIO

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect, reverse

from repository.models import *
from utils.paging import CustomPager
from .form.blogForm import SignForm
from .form.blogForm import LoginForm

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from utils.check_code import create_validate_code
# Create your views here.

def mainBlog(request):

    url_data = request.GET.get('choice')
    if not request.GET.get("p"):
        current_page = 1
    else:
        current_page = int(request.GET.get('p'))
    article_obj = Artical.objects.all().order_by('up_count')
    print(article_obj)
    if url_data is None:
        article_list = Artical.objects.all()
    else:
        article_list = Artical.objects.filter(article_type_id=url_data)
    pager_obj = CustomPager(len(article_list),current_page,1,5)

    if request.session.get('user'):
        session_obj = request.session.get('user')
    else:
        session_obj = None
    return render(request, 'blogPage/mainBlog.html', {'article_list': article_list[pager_obj.start:pager_obj.end],
                                           'pager_obj':pager_obj,
                                           'session_obj':session_obj,
                                            'article_obj':article_obj})

def login(request):
    if request.method == 'GET':
        login_form = LoginForm(request)
        return render(request, 'blogPage/login.html', {'login_form':login_form, })
    elif request.method == 'POST':
        login_set={'status':100,'message':None,'errors':None}
        login_form = LoginForm(request,request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if login_form.is_valid():
            user_obj = UserInfo.objects.filter(username=username).first()
            if user_obj:
                if user_obj.password == password:
                    request.session['user']=username
                    request.session['is_login']='login'
                    return redirect('/mainBlog')
                else:
                    login_set['errors']='密码错误'
                    return render(request, 'blogPage/login.html', {'login_form':login_form,
                                                        'login_set':login_set})
            else:
                login_set['errors']='用户名不存在'
                return render(request, 'blogPage/login.html', {'login_form':login_form,
                                                    'login_set':login_set})
        else:
            return render(request, 'blogPage/login.html', {'login_form':login_form})

def logOut(request):
    request.session.clear()
    print(request.session)
    return redirect('/login.html')

def sessionAuth(func):
    def weaper(request,*args,**kwargs):
        s = request.session.get("is_login",False)
        if s == "login":
            return func(request,*args,**kwargs)
        else:
            return redirect('/login')
    return weaper

def giveLike(request):
    upSet={'status':1000,'message':None,'data':None}
    upUser = request.GET.get('sessionData')
    articleData = request.GET.get('articleData').split(' ')
    upUserId = UserInfo.objects.filter(username=upUser).first()
    article_id = int(articleData[0])

    if UpDown.objects.filter(user_id=upUserId.nid,article_id=article_id):
        upSet['message']='hasUp'
        print('++++++++++')
        print(Artical.objects.filter(nid=article_id).values('up_count'))
        upSet['data'] = Artical.objects.filter(nid=article_id).values('up_count').first().get('up_count')
    else:
        UpDown.objects.create(user_id=upUserId.nid,article_id=article_id,up=True)
        count = Artical.objects.filter(nid=article_id).values('up_count').first()
        up_count = count.get('up_count')+1
        Artical.objects.filter(nid=article_id).update(up_count=up_count)
        upSet['message']='upSuccess'
        upSet['data']=up_count

    return HttpResponse(json.dumps(upSet))

def sign(request):
    if request.method == 'POST':
        verify_data = {'status':100,'message':None}
        sign_obj = SignForm(request.POST)
        if sign_obj.is_valid():
            username = sign_obj.cleaned_data.get('username')
            email = sign_obj.cleaned_data.get('email')
            if UserInfo.objects.filter(username=username):
                verify_data['message'] = '用户名已存在'
                return render(request, 'blogPage/sign.html', {'sign_obj':sign_obj,
                                                   "verify_data":verify_data})
            if UserInfo.objects.filter(email=email):
                verify_data['message'] = '您的邮箱已注册'
                return render(request, 'blogPage/sign.html', {'sign_obj':sign_obj,
                                                   'verify_data':verify_data})

            userInfo_data = sign_obj.cleaned_data
            del userInfo_data['confirm_password']
            UserInfo.objects.create(**userInfo_data)
            return redirect('/login')
        else:
            return render(request, 'blogPage/sign.html', {'sign_obj':sign_obj})
    elif request.method == 'GET':
        sign_obj = SignForm()
        return render(request, 'blogPage/sign.html', {'sign_obj':sign_obj})

def checkCode(request):
    f = BytesIO()
    img,code = create_validate_code()
    request.session['check_code']=code
    img.save(f,'PNG')
    return HttpResponse(f.getvalue())

def personalHomePage(request,*args,**kwargs):
    blogName = kwargs.get('blogSite')
    blog_obj = Blog.objects.filter(site=blogName).first()
    all_artical_list = Artical.objects.filter(blog__site=blogName)
    pager_obj = CustomPager(len(all_artical_list), 1, 5)
    login_name = request.session.get('user')
    login_obj = UserInfo.objects.filter(username=login_name)[0]
    print('------',login_name)
    return render(request, 'blogPage/personalHomePage.html', {'blog_obj':blog_obj,
                                                              'all_artical_list':all_artical_list[pager_obj.start:pager_obj.end],
                                                              'pager_obj':pager_obj,
                                                              'login_obj':login_obj})

def personalClassPage(request,**kwargs):

    blogName = kwargs.get('blogSite')
    condition = kwargs.get('condition')
    val = int(kwargs.get('val'))
    if condition == 'tag':
        artical_obj = Artical.objects.filter(blog__site=blogName,tags__nid=val).all()
    elif condition == 'category':
        artical_obj = Artical.objects.filter(blog__site=blogName,category__nid=val).all()
    else:
        artical_obj = Artical.objects.filter(blog__site=blogName)
    blog_obj = Blog.objects.filter(site=blogName).first()


    pager_obj = CustomPager(len(artical_obj), 1, 5)
    return render(request, 'blogPage/personalHomePage.html', {'blog_obj': blog_obj,
                                                     'all_artical_list': artical_obj[
                                                                         pager_obj.start:pager_obj.end],
                                                     'pager_obj': pager_obj})

def oneArticle(request,**kwargs):
    blogName = kwargs.get('blogSite')
    article_id = int(kwargs.get('article_id'))
    try:
        val = int(kwargs.get('val'))
        condition = kwargs.get('condition')
    except Exception as e:
        condition = None
    if condition == 'tag':
        artical_obj = Artical.objects.filter(blog__site=blogName, tags__nid=val,nid=article_id).first()
        print(artical_obj)
    elif condition == 'category':
        artical_obj = Artical.objects.filter(blog__site=blogName, category__nid=val,nid=article_id).first()
    else:
        artical_obj = Artical.objects.filter(blog__site=blogName,nid=article_id).first()
    blog_obj = Blog.objects.filter(site=blogName).first()
    all_artical_list = Artical.objects.filter(blog__site=blogName)
    pager_obj = CustomPager(len(all_artical_list), 1, 5)
    login_name = request.session.get('user')
    login_obj = UserInfo.objects.filter(username=login_name)[0]

    return render(request, 'blogPage/oneArticle.html', {'blog_obj':blog_obj, 'artical_obj':artical_obj,
                                             'all_artical_list':all_artical_list[pager_obj.start:pager_obj.end],
                                             'pager_obj':pager_obj,
                                             'login_obj':login_obj
                                            })

def oneArticleUpDown(request,**kwargs):
    return HttpResponse('success')




