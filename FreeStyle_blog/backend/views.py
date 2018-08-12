from django.shortcuts import render
from django.shortcuts import redirect
from repository.models import *
from django.db.models import Q
from django.shortcuts import HttpResponse
from datetime import datetime

from backend.backend_form import article_form
from backend.backend_form import trouble_form
from web.views import sessionAuth

@sessionAuth
def backendManagement(request,**kwargs):
    sessiondata = request.session.get('user')
    blogSite = Blog.objects.filter(user__username=sessiondata).values('site').first()['site']
    print(blogSite)
    try:
        category_conditions = kwargs['blogCategory']
        category_conditions_id = int(category_conditions.split('-')[1])
        print(category_conditions_id)
        if category_conditions.split('-')[0] == 'blog':
            article_category_list = Artical.objects.filter(blog__artical__article_type_id=category_conditions_id)
        elif category_conditions.split('-')[0]=='category':
            article_category_list = Artical.objects.filter(category__nid=category_conditions_id)
        else:
            article_category_list =[]
    except Exception as e:
        article_category_list=[]
    article_obj = Artical.objects.filter(blog__site=blogSite).first()
    article_category_obj = Category.objects.filter(blog__site=blogSite)
    login_name = request.session.get('user')
    login_obj = UserInfo.objects.filter(username=login_name)[0]

    return render(request,'blogManagement/layout.html',{'article_obj':article_obj,
                                                        'article_category_obj':article_category_obj,
                                                        'blogSite':blogSite,
                                                        'article_category_list':article_category_list,
                                                        'login_obj':login_obj})

@sessionAuth
def createArticle(request,**kwargs):
    if request.method == 'GET':
        blogSite = kwargs['blogSite']
        createForm = article_form.CreateArticleForm()
        return render(request,'blogManagement/createArticle.html',{'createForm':createForm,
                                                                   'blogSite':blogSite})
    elif request.method == 'POST':
        blogSite = kwargs['blogSite']
        createForm = article_form.CreateArticleForm(request.POST)
        if createForm.is_valid():
            title = createForm.cleaned_data['title']
            summary = createForm.cleaned_data['summary']
            content = createForm.cleaned_data['articledetail_content']
            article_type = int(createForm.cleaned_data['article_type_id'])
            category = int(createForm.cleaned_data['category_id'])
            tag = createForm.cleaned_data['tag_id']
            blog_id = Blog.objects.filter(site=blogSite).values('nid').first()['nid']
            Artical.objects.create(title=title,summary=summary,
                                                category_id=category,
                                                article_type_id=article_type,
                                                create_time=datetime.now(),
                                                blog_id=blog_id)
            article_id = Artical.objects.filter(title=title).values('nid').first()['nid']
            ArticleDetail.objects.filter(artical__blog__site=blogSite).create(content=content,artical_id=article_id)
            article_tag = Article2Tag(article_id=article_id,tag_id=tag)
            article_tag.save()
        return render(request, 'blogManagement/createArticle.html', {'createForm': createForm,
                                                                     'blogSite': blogSite})

@sessionAuth
def trouble(request,**kwargs):
    blogSite = kwargs['blogSite']
    handlerId = UserInfo.objects.filter(blog__site=blogSite).values('nid').first()['nid']
    print(handlerId)
    if blogSite == 'root':
        trouble_list=Trouble.objects.filter(Q(user__blog__site=blogSite) | Q(handler_status=0) | Q(handler=handlerId)).\
        only('title', 'handler_status', 'create_time', 'dear_time', 'handler', 'id').order_by('handler_status')
    else:
        trouble_list = Trouble.objects.filter(user__blog__site=blogSite).\
        only('title','handler_status','create_time','dear_time','handler','id')
    login_name = request.session.get('user')
    login_obj = UserInfo.objects.filter(username=login_name)[0]
    return render(request,'blogManagement/troubleList.html',{
        'trouble_list':trouble_list,
        'blogSite':blogSite,
        'login_obj': login_obj
    })

@sessionAuth
def createTrouble(request,**kwargs):
    blogSite = kwargs.get('blogSite')
    if request.method == 'GET':
        troubleFormObj = trouble_form.TroubleForm()
        return render(request,'blogManagement/troubleCreate.html',{
            'blogSite': blogSite,
            'troubleFormObj':troubleFormObj
        })
    elif request.method == 'POST':
        troubleFormObj = trouble_form.TroubleForm(request.POST)
        troubleDict = {}
        if troubleFormObj.is_valid():
            user_id = UserInfo.objects.filter(blog__site=blogSite).values('nid').first()['nid']
            troubleDict['user_id']=user_id
            troubleDict.update(troubleFormObj.cleaned_data)
            Trouble.objects.create(**troubleDict)
            print(troubleDict)
            return redirect('/backendManagement/%s/troubleList.html/' % blogSite)

        return render(request, 'blogManagement/troubleCreate.html', {
            'blogSite': blogSite,
            'troubleFormObj': troubleFormObj
        })

@sessionAuth
def editTrouble(request,**kwargs):
    blogSite = kwargs.get('blogSite')
    troubleId = kwargs.get('troubleId')
    troubleObj = Trouble.objects.filter(handler_status=0, id=troubleId).only('detail', 'image').first()
    if request.method == 'GET':
        troubleFormObj = trouble_form.TroubleForm({'title':troubleObj.title,'detail':troubleObj.detail,'image':troubleObj.image})
        return render(request, 'blogManagement/troubleEdit.html', {
            'blogSite': blogSite,
            'troubleFormObj': troubleFormObj,
            'troubleObj':troubleObj,
        })
    elif request.method == 'POST':
        troubleFormObj = trouble_form.TroubleForm(request.POST)
        if troubleFormObj.is_valid():
            troubleObj = Trouble.objects.filter(handler_status=0, id=troubleId).update(**troubleFormObj.cleaned_data)
            return redirect('backendManagement/%s/troubleList.html/' % (blogSite))

        return render(request, 'blogManagement/troubleEdit.html', {
            'blogSite': blogSite,
            'troubleFormObj': troubleFormObj,
            'troubleObj': troubleObj,
        })






    # elif request.method == 'POST':
    #     blogSite = kwargs.get('blogSite')
    #     troubleFormObj = trouble_form.TroubleForm(request.POST)
    #     troubleDict = {}
    #     if troubleFormObj.is_valid():
    #         user_id = UserInfo.objects.filter(blog__site=blogSite).values('nid').first()['nid']
    #         troubleDict['user_id'] = user_id
    #         troubleDict.update(troubleFormObj.cleaned_data)
    #         Trouble.objects.create(**troubleDict)
    #         print(troubleDict)
    #         return redirect('/backendManagement/%s/troubleList.html/' % blogSite)
    #
    #     return render(request, 'blogManagement/troubleCreate.html', {
    #         'blogSite': blogSite,
    #         'troubleFormObj': troubleFormObj
    #     })

@sessionAuth
def detailTrouble(request,**kwargs):
    blogSite = kwargs.get('blogSite')
    troubleId = kwargs.get('troubleId')

    trouble_obj = Trouble.objects.filter(id=troubleId).first()

    return render(request,'blogManagement/detailTrouble.html',{
        'blogSite':blogSite,
        'trouble_obj':trouble_obj,
    })

#root用户,不同的用户有不同的全新，普通用户不处理保障

def dearTrouble(request,**kwargs):
    blogSite = kwargs.get('blogSite')
    troubleId = kwargs.get('troubleId')
    handlerId = UserInfo.objects.filter(blog__site=blogSite).values('nid').first()['nid']
    if request.method == 'GET':
        v = Trouble.objects.filter(id=troubleId,handler_status=0).update(handler_id=handlerId,handler_status=1)
        troubleObj = Trouble.objects.filter(id=troubleId).only('title', 'detail').first()
        dearFormObj = trouble_form.DearTroubleForm()
        if v:
            return render(request, 'blogManagement/dearTrouble.html',{
                'blogSite':blogSite,
                'troubleObj':troubleObj,
                'dearFormObj':dearFormObj
            })
        elif Trouble.objects.filter(id=troubleId,handler_status=1,handler_id=handlerId):
            return render(request, 'blogManagement/dearTrouble.html', {
                'blogSite': blogSite,
                'troubleObj': troubleObj,
                'dearFormObj': dearFormObj
            })
        else:
            return HttpResponse('已经被接单')
    elif request.method == 'POST':
        dearFormObj=trouble_form.DearTroubleForm(request.POST)
        if dearFormObj.is_valid():
            Trouble.objects.filter(id=troubleId).update(handler_status=2,**dearFormObj.cleaned_data)
            return redirect('/backendManagement/%s/troubleList.html/' % blogSite)
        else:
            troubleObj = Trouble.objects.filter(id=troubleId).only('title','detail').first()
            return render(request, 'blogManagement/dearTrouble.html', {
                'blogSite': blogSite,
                'troubleObj': troubleObj,
                'dearFormObj': dearFormObj
            })

def troubleReport(request,**kwargs):
    user_list = UserInfo.objects.filter(Q(username='root')|Q(username='superUser'))
    data_dict = []

    for user in user_list:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute('''select count(id),date_format(dear_time,'%%Y-%%m') from repository_trouble where handler_id=%s GROUP BY date_format(dear_time,'%%Y-%%m')''',[user.nid,])
        row = cursor.fetchall()
        temp = {
            'name':user.username,
            'data':row
        }
        data_dict.append(temp)
    return render(request,'blogManagement/troubleReport.html')