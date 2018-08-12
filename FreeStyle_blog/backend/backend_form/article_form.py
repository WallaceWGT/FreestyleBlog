"--wallace--"

from django.forms import forms
from django.forms import fields
from django.forms import widgets

from repository.models import *
choice = tuple(Artical.type_choices)
class CreateArticleForm(forms.Form):
    title = fields.CharField(min_length=1,max_length=32,
                             widget=widgets.TextInput(attrs={'class':'form-control','name':'title'}))
    summary = fields.CharField(widget=widgets.Textarea(attrs={'class':'form-control','rows':'4','name':'summary'}))
    articledetail_content = fields.CharField(widget=widgets.Textarea(
        attrs={'id':'content','name':'articledetail_content',}
    ),required=False)
    article_type_id = fields.CharField(
        widget=widgets.RadioSelect(attrs={
            'name':'article_type_id',
        })
    )
    category_id = fields.IntegerField(
        widget=widgets.RadioSelect(attrs={
            'name':'category_id',
        })
    )
    tag_id = fields.IntegerField(
        widget=widgets.RadioSelect(attrs={
            'name':'tag_id',
        })
    )
    def __init__(self,*args,**kwargs):
        super(CreateArticleForm,self).__init__(*args,**kwargs)
        self.fields['article_type_id'].widget.choices = tuple(Artical.type_choices)
        self.fields['category_id'].widget.choices = Category.objects.all().values_list('nid','title')
        self.fields['tag_id'].widget.choices = Tag.objects.all().values_list('nid','title')