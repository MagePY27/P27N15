from django.urls import path
from system import views
from system.views_user import UserManageView, USerListView, UserUpdateView, UserCreateView


app_name = 'system'

urlpatterns = [
    path('', views.IndexView.as_view(), name='login'),
    path('user_manage/', UserManageView.as_view(), name='system-user-manage'),
    path('user/list/', USerListView.as_view(), name='user-list'),
    path('user/update/', UserUpdateView.as_view(), name='user-update'),
    path('user/create/', UserCreateView.as_view(), name='user-create'),

]