# _*_ coding: utf-8 _*_

import xadmin
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)

class GlobalSettings(object):
  site_title="simple-admin 管理系统"
  site_footer="simple-xadmin"
  menu_style="accordion"
xadmin.site.register(views.CommAdminView,GlobalSettings)