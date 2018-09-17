# _*_ coding:utf-8 _*_
__author__ = 'victorfan'
__date__ = '2018/8/14 13:56'


from xadmin import views

from .models import EmailVerifyRecord, Banner
import xadmin


class BaseSetting(object):
    # 给默认的后台管理系统设置可以多选的页面主题
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    # site_title是左上角的logo，site_footer是页脚的标签
    site_title = "慕学后台管理系统"
    site_footer = "慕学在线网"
    # accordion可折叠
    menu_style = "accordion"

# 邮件记录检验的管理类
class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


# 标题的管理类
class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
