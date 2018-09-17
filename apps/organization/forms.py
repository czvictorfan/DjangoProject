# _*_ coding:utf-8 _*_
__author__ = 'victorfan'
__date__ = '2018/9/6 9:53'
# 导入正则表达式的管理类
import re
from django import forms

from operation.models import UserAsk


# 用ModelForm直接生成UserForm（UserAsk）
class UserAskForm(forms.ModelForm):
    # my_filed = forms.CharField()，也可以直接生成新字段
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

# clean_是固定的格式，对fields里面的字段进行过滤是否合法
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        # 对正则表达式匹配
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invaild")
