from django.db import models

# Create your models here.
class UserInfo(models.Model):
    '''
    用户信息表
    '''
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名',max_length=32,unique=True)
    password = models.CharField(verbose_name='密码',max_length=64)
    nickname = models.CharField(verbose_name='昵称',max_length=32)
    email = models.EmailField(verbose_name='邮箱',unique=True)
    avatar = models.ImageField(verbose_name='头像',upload_to='static/userImage',null=True,blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    fans = models.ManyToManyField(verbose_name='粉丝',
                                  to='UserInfo',
                                  through='UserFans',
                                  related_name='f',
                                  through_fields=('user','follower'))
    permissions = [
        (0, '普通'), (1, '管理'), (2, '最高'),
    ]
    premissions = models.IntegerField(choices=permissions,null=True,blank=True,default=0)
    class Meta:
        verbose_name="用户信息"
    def __str__(self):
        return self.username

class UserFans(models.Model):
    '''
    互粉关系表
    '''
    user = models.ForeignKey(verbose_name='博主',to='UserInfo',to_field='nid',
                             related_name='users',on_delete=models.CASCADE)
    follower = models.ForeignKey(verbose_name='粉丝',to='UserInfo',to_field='nid',
                                 related_name='follwers',on_delete=models.CASCADE)
    class Meta:
        verbose_name='互粉关系'
        unique_together = [
            ('user','follower'),
        ]
    def __str__(self):
        return self.user.username
class Blog(models.Model):
    '''
    博客信息
    '''
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题',max_length=64)
    site = models.CharField(verbose_name='个人博客前缀',max_length=32,unique=True)
    theme = models.CharField(verbose_name='博客主题',max_length=32)
    user = models.OneToOneField(to='UserInfo',to_field='nid',on_delete=models.CASCADE)

    class Meta:
        verbose_name = "博客信息"
    def __str__(self):
        return self.title

class Category(models.Model):
    '''
    博主博文分类表
    '''
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题',max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid',on_delete=models.CASCADE)

    class Meta:
        verbose_name = '博主博文分类'
    def __str__(self):
        return self.title

class Tag(models.Model):
    '''
    标签详情
    '''
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称',max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid',on_delete=models.CASCADE)

    class Meta:
        verbose_name='标签'
    def __str__(self):
        return self.title

class Artical(models.Model):
    '''
    文章详情
    '''
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题',max_length=32)
    summary = models.CharField(verbose_name='文章简介',max_length=255)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(verbose_name='赞',default=0)
    down_count = models.IntegerField(verbose_name='踩',default=0)
    create_time = models.DateTimeField(verbose_name="发表时间")
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid',on_delete=models.CASCADE)
    category = models.ForeignKey(verbose_name='文章类型',to='Category',to_field='nid',on_delete=models.SET('全部'))

    type_choices = [
        (1,'Python'),(2,'Linux'),(3,'OpenStack'),(4,'GoLang')
    ]
    article_type_id = models.IntegerField(choices=type_choices,default=None)
    tags = models.ManyToManyField(
        to='Tag',
        through='Article2Tag',
        through_fields=('article','tag'),
    )

    class Meta:
        verbose_name='文章详情'
    def __str__(self):
        return self.title

class ArticleDetail(models.Model):
    content = models.TextField(verbose_name='文章内容')
    artical = models.OneToOneField(verbose_name='所属文章',to='Artical',to_field='nid',on_delete=models.CASCADE)
    class Meta:
        verbose_name='文章内容详情'
    def __str__(self):
        return self.artical.title

class Article2Tag(models.Model):
    article = models.ForeignKey(verbose_name='文章',to='Artical',to_field='nid',on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name='标签',to='Tag',to_field='nid',on_delete=models.CASCADE)
    class Meta:
        verbose_name='文章标签信息'
        unique_together=[
            ('article','tag'),
        ]

class Comment(models.Model):
    '''
    评论表
    '''
    nid = models.BigAutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容',max_length=255)
    create_time = models.DateTimeField(verbose_name='评论时间',auto_now_add=True)

    reply = models.ForeignKey(verbose_name='评论回复',to='self',related_name='back',null=True,on_delete=models.CASCADE)
    article = models.ForeignKey(verbose_name='评论文章',to='Artical',to_field='nid',on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='评论者',to='UserInfo',to_field='nid',on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论表'

class UpDown(models.Model):
    '''
    顶或踩
    '''
    article = models.ForeignKey(verbose_name='文章',to='Artical',to_field='nid',on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='点赞者',to='UserInfo',to_field='nid',on_delete=models.CASCADE)
    up = models.BooleanField(verbose_name='是否赞')
    class Meta:
        verbose_name='点赞表'
        unique_together=[
            ('article','user'),
        ]

class Trouble(models.Model):
    title = models.CharField(verbose_name='报障标题', max_length=32)
    detail = models.CharField(verbose_name='报障详情', max_length=255)

    image = models.ImageField(verbose_name='报障图片', upload_to='static/disabilitiesImage', null=True,blank=True)
    user = models.ForeignKey(verbose_name='报障用户', to='UserInfo', to_field='nid',
                             on_delete=models.CASCADE, related_name='ud')

    handler = models.ForeignKey(verbose_name='处理用户', to='UserInfo', to_field='nid',
                                on_delete=models.CASCADE, related_name='hd', null=True,blank=True)
    status = [
        (0, '待处理'), (1, '处理中'), (2, '已处理'),
    ]
    handler_status = models.IntegerField(choices=status, default=0)
    cm_status = [
        (0, '很差'), (1, '一般'), (2, '很好')
    ]
    comment_status = models.IntegerField(choices=cm_status, default=1, null=True,blank=True)
    create_time = models.DateTimeField(verbose_name='提交时间', auto_now_add=True, null=False)
    dear_time = models.DateTimeField(verbose_name='处理时间',null=True,blank=True)
    dear_detail = models.TextField(null=True,blank=True)
    class Meta:
        verbose_name = '报障单'

    def __str__(self):
        return self.title

