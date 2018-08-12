from django.contrib import admin
from repository.models import *

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(UserFans)
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Artical)
admin.site.register(ArticleDetail)
admin.site.register(Article2Tag)
admin.site.register(Comment)
admin.site.register(UpDown)
admin.site.register(Trouble)

