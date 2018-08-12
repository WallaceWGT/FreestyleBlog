"--wallace--"
from django import forms
from django.forms import fields
from .baseForm import BaseForm
from django.core.exceptions import ValidationError,NON_FIELD_ERRORS


class SignForm(forms.Form):
    r_pwd = '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$'
    username = fields.CharField(max_length=21, required=True)
    # password = fields.RegexField(r_pwd, max_length=32, min_length=8,
    #                              error_messages={
    #                                  'required': '密码不能为空',
    #                                  'invaile': '密码必须包含数字，字母，特殊字符',
    #                                  'min_length': '密码最小长度为8',
    #                                  'max_length': '密码最大长度为32'
    #                              })
    password = fields.CharField()
    confirm_password = fields.CharField(max_length=32)
    email = fields.EmailField(required=True)

    def clean(self):
        pwd1 = self.cleaned_data['password']
        pwd2 = self.cleaned_data['confirm_password']
        if pwd1 == pwd2:
            pass
        else:
            raise ValidationError('两次密码不一致')


class LoginForm(BaseForm, forms.Form):
    username = fields.CharField()
    password = fields.CharField()
    check_code = fields.CharField()

    def clean_check_code(self):
        print("------------")
        if self.request.session.get('check_code').upper()!= self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误', code='invalid')
        return self.cleaned_data