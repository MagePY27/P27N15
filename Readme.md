### celery 基础
> 请查看
https://github.com/MagePY27/P27N15/blob/master/day02/celery.md




### day 3 drf
> 使用drf实现后端
> 参考增加了restful的 response, viewset 功能,方便前端调用
> viewset.ModelSet视图
- mixins.CreateModeMixin
- mixins.RetriveModeMixin
- mixins.UpdateModeMixin
- mixins.DestoryModeMixin
- mixins.ListModeMixin

- 效果
![image](https://github.com/MagePY27/P27N15/blob/master/img/day3-book.png)
![image](https://github.com/MagePY27/P27N15/blob/master/img/day3-publish-create.png)

#### 设置docs
- setting
```python
'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
```

- urls
```python
from rest_framework.documentation import include_docs_urls
urlpatterns = [
...
    # drf docs
    path('docs/', include_docs_urls(title='接口文档'))
]
```

#### 重写rest rest_framework 位于utils目录
- Response My_rest_response.py
- 分页 MyPageNumberPagination.py
- viewset My_rest_viewset.py  增加返回信息
- 异常 My_rest_exception.py   增加错误提示

#### 出版社 demo
- serializers
```python
class PublisherSerializer(serializers.ModelSerializer):
    name = serializers.CharField(label='名称', max_length=32, min_length=2, required=True, help_text='名称',
                                 validators=[
                                     UniqueValidator(
                                         queryset=Publisher.objects.all(),
                                         message="出版社名称已存在"
                                     )],
                                 error_messages={
                                     "max_length": "最大32个字符",
                                     "min_length": "最少2个字符",
                                     'required': '请输入出版社名称'
                                 })
    address = serializers.CharField(label='地址', max_length=32, min_length=2, required=True, help_text='地址',
                                    error_messages={
                                        "max_length": "最大32个字符",
                                        "min_length": "最少2个字符",
                                        "required": "地址不能为空"
                                    })
    city = serializers.CharField(label='城市', max_length=32, min_length=2, required=True, help_text='城市',
                                 error_messages={
                                     "max_length": "最大32个字符",
                                     "min_length": "最少2个字符",
                                     "required": "城市不能为空"
                                 })

    class Meta:
        model = Publisher
        fields = "__all__"
```

- views

```python
# 管理页
class PublishView(APIView):

    def get(self, request):
        city_list = Publisher.objects.values('city').distinct()
        return render(request, 'publisher.html', locals())


class PublishCrateView(APIView):

    def get(self, request):
        return render(request, 'publisher_create.html')


class PublishUpdateView(APIView):

    def get(self, request):
        if request.GET['id']:
            publisher = Publisher.objects.filter(id=request.GET['id']).first()

        return render(request, 'publisher_update.html', locals())


# class PublisherViewSet(viewsets.ModelViewSet):
class PublisherViewSet(MyViewBase):

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    # filter
    filter_fields = ['city']
    # search
    search_fields = ('name', 'address')
```


- urls
```python
from django.urls import path, include
from apps.books import views
from rest_framework.routers import DefaultRouter
# drf注册
router = DefaultRouter()
router.register(r'publisher_action', views.PublisherViewSet)
router.register(r'author_action', views.AuthorViewSet)
router.register(r'book_action', views.BookViewSet)

app_name = 'books'

urlpatterns = [
    # drf
    path('', include(router.urls), name='books-publisher_action'),
    # publisher
    path('publisher/', views.PublishView.as_view(), name='books-publisher'),
    path('publisher/create/', views.PublishCrateView.as_view(), name='books-publisher-create'),
    path('publisher/update/', views.PublishUpdateView.as_view(), name='books-publisher-update'),
    # author
    path('author/', views.AuthorView.as_view(), name='books-author'),
    path('author/create/', views.AuthorCrateView.as_view(), name='books-author-create'),
    path('author/update/', views.AuthorUpdateView.as_view(), name='books-author-update'),
    # books
    path('books/', views.BooksView.as_view(), name='books-books'),
]

```

- 前端调整
``` javascript
//bootstrap table 变更
// 增加指定返回数据
responseHandler: function (res) {
    //将服务端你的数据转换成bootstrap table 能接收的类型
    return {
        "total": res.count,//查询的总数量
        "rows": res.data   //数据
    };
},

// create/update function
// 修改返回信息判断
$("#btnSave").click(function () {
            var data = $("#addForm").serialize();
            $.ajax({
                type: $("#addForm").attr('method'),
                url: "/books/publisher_action/",
                data: data,
                cache: false,
                success: function (msg) {
                    if (msg.message == 'success') {
                        layer.alert('添加成功！', {icon: 1}, function (index) {
                            parent.layer.closeAll(); //关闭所有弹窗
                        });
                    } else {

                        var obj = msg.data;//定义一个object对象
                        var keys = [];//定义一个数组用来接受key
                        var values = [];//定义一个数组用来接受value
                        for (var key in obj) {
                            keys.push(key);
                            values.push(obj[key]);//取得value
                        }
                        {#alert("keys：" + keys + " errors：" + values);#}
                        layer.alert("keys：" + keys + " <br>errors：" + values , {icon: 5});
                    }
                    return;
                }
            });
        });
```

#### 待解决
> 多对多，一对多更新，是否要自定义create方法？
- serialize
```python
class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(label='书名', required=True, help_text='书名',
                                  error_messages={"required": "书名不能为空"
                                                  })
    # 显示外键
    publisher = serializers.CharField(source='publisher.name', read_only=True)
    # many to many
    # authors = AuthorSerializer(many=True, read_only=True)
    authors = serializers.StringRelatedField(many=True, read_only=True)
    # authors = AuthorDisplaySerializers(many=True, read_only=True)

    class Meta:
        model = Book
        # fields = ['id', 'title', 'publisher']
        fields = ['id', 'title', 'publisher', 'authors']
```
