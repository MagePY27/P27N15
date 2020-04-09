from django.urls import path, include
from .views import IndexView, UserView, USerListView, ListViewSet, USerCreateView, UserUpdateView, UserDeleteView, PasswordChangeView


app_name = 'system'

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('user/', UserView.as_view(), name='user'),
    path('user/list/', USerListView.as_view(), name='user-list'),
    path('user/list2/', ListViewSet.as_view(), name='user-list2'),
    path('user/create/', USerCreateView.as_view(), name='user-create'),
    path('user/update/', UserUpdateView.as_view(), name='user-update'),
    path('user/update/password/', PasswordChangeView.as_view(), name='user-update-password'),
    path('user/delete/', UserDeleteView.as_view(), name='user-delete'),
]