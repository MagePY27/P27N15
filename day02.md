### day2
#####  tamplates
>  基于 AdminLte 2模板
-  模板的继承关系
    -  base-static.html  （静态资源）
        -  base-layer.html  (layer弹出)
        -  head-footer.html
            -  base-left.html  （左部菜单）
                - index.html

#####  用户表
> 扩展django的User model扩展类AbstractUser
```python
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    name = models.CharField(max_length=20, default="", verbose_name="姓名")
    gender = models.IntegerField(choices=((0, "男"), (1, "女")), default=0, verbose_name="性别")
    email = models.EmailField(max_length=50, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    name = models.CharField(max_length=20, default="", verbose_name="姓名")
    gender = models.IntegerField(choices=((0, "男"), (1, "女")), default=0, verbose_name="性别")
    email = models.EmailField(max_length=50, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name




```

##### 用户页面
> 分页&搜索&下载
> 基于bootstrap-table
![image](https://github.com/MagePY27/P27N15/blob/master/img/user-table.png)

- 前端
```javascript
        var oDataTable = null;

        $(function () {
            oDataTable = initTable();

            function initTable() {
                var oTable = $('#mytab').bootstrapTable({
                    {#全部参数#}
                    //请求后台的URL（*）或者外部json文件，json内容若为json数组[{"id": 0,"name": "Item 0","price": "$0"},{"id": 1,"name": "Item 1","price": "$1"}]，
                    //且键的名字必须与下方columns的field值一样，同时sidePagination需要设置为client或者直接注释掉，这样前台才能读取到数据，且分页正常。
                    //当json文件内容为json对象时：{"total": 2,"rows": [{"id": 0,"name": "Item 0","price": "$0"},{"id": 1,"name": "Item 1","price": "$1"}]}，
                    //分页要写为server，但是server如果没有处理的话,会在第一页显示所有的数据，分页插件不会起作用
                    {#url: "{% static 'guchen_obj.json' %}",     #}

                    url: "/system/user/list/",     //从后台获取数据时，可以是json数组，也可以是json对象
                    dataType: "json",
                    method: 'get',                      //请求方式（*）
                    toolbar: '#toolbar',                //工具按钮用哪个容器
                    striped: true,                      //是否显示行间隔色
                    cache: true,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                    pagination: true,                   //是否显示分页（*）
                    sortable: true,                     //是否启用排序
                    sortOrder: "asc",                   //排序方式
                    {#queryParams: oTableInit.queryParams,//传递参数（*）#}
                    sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）,数据为json数组时写client，json对象时（有total和rows时）这里要为server方式，写client列表无数据
                    pageNumber: 1,                       //初始化加载第一页，默认第一页
                    pageSize: 2,                       //每页的记录行数（*）
                    pageList: [1, 2, 5, 100],        //可供选择的每页的行数（*）
                    search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以意义不大
                    strictSearch: true,
                    showColumns: true,                  //是否显示所有的列
                    showRefresh: true,                  //是否显示刷新按钮
                    minimumCountColumns: 2,             //最少允许的列数
                    clickToSelect: true,                //是否启用点击选中行
                    {#height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度#}
                    uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
                    showToggle: false,                    //是否显示详细视图和列表视图的切换按钮
                    cardView: false,                    //是否显示详细视图
                    detailView: false,                   //是否显示父子表
                    idField: 'id',          //指定主键
                    singleSelect: true,                //开启单选,想要获取被选中的行数据必须要有该参数
                    showExport: true,   //导出功能
                    exportDataType: ['selected'],
                    {#exportTypes: ['json',  'pdf'], //导出类型#}
                    exportOptions: {//导出设置
                        fileName: 'Table_User',//下载文件名称
                    },


                    //得到查询的参数，会在url后面拼接，如：?rows=5&page=2&sortOrder=asc&search_kw=&_=1564105760651
                    queryParams: function (params) {
                        //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
                        var query_params = {
                            rows: params.limit,                         //页面大小
                            page: (params.offset / params.limit) + 1,   //页码
                            sort: params.sort,      //排序列名
                            sortOrder: params.order, //排位命令（desc，asc）

                            //查询框中的参数传递给后台
                            search_kw: $('#search-keyword').val(), // 请求时向服务端传递的参数
                        };
                        return query_params;
                    },

                    columns: [
                        {
                            checkbox: true  //第一列显示复选框
                        },

                        {
                            field: 'id',  //返回数据rows数组中的每个字典的键名与此处的field值要保持一致
                            title: 'id',
                            sortable: true
                        },
                        {
                            field: 'name',
                            title: '姓名',
                            sortable: true
                        },
                        {
                            field: 'email',
                            title: '邮箱',
                            sortable: true
                        },
                        {
                            field: 'gender',
                            title: '性别',
                            sortable: true,
                            formatter: function (value, row, index) {
                                if (value === 0) {
                                    return '<span class="label label-success">' + '男' + '</span>';
                                }
                                return '<span class="label label-warning">' + '女' + '</span>';
                            }
                        },
                        {
                            field: 'operate',
                            title: '操作',
                            width: 120,
                            align: 'center',
                            valign: 'middle',
                            formatter: actionFormatter,
                        },
                    ],

                    onLoadSuccess: function (data) {
                        {#获取行数据的状态#}
                        console.log('渲染数据完成后，打印所有数据')
                        console.log(data);
                        {#获取所有列表数据#}
                        var data = $("#mytab").bootstrapTable("getData");
                        console.log('已获取全部数据%s', data);
                    }

                });
                return oTable;
            }
        });

        //操作栏的格式化,value代表当前单元格中的值，row代表当前行数据，index表示当前行的下标
        function actionFormatter(value, row, index) {
            var index = index
            {#console.error(index)#}
            var id = JSON.stringify(row.id);
            {#console.error(id)#}
            var ret = "";
            ret += "<a href='javascript:;' class='btn btn-xs green' onclick=\"doUpdate(" + id + ")\" title='编辑'><span class='glyphicon glyphicon-pencil'>Edit</span></a>";
            ret += "<a href='javascript:;' class='btn btn-xs btn-danger' onclick=\"doDelete(" + id + ")\" title='删除'><span class='glyphicon glyphicon-trash'>Del</span></a>";
            return ret;

        }

        // 搜索查询按钮触发事件
        $(function () {
            $("#search-button").click(function () {
                $('#mytab').bootstrapTable(('refresh')); // 很重要的一步，刷新url！
                $('#search-keyword').val()
            })
        })

        //重置搜索条件
        function clean() {
            //先清空
            $('#search-keyword').val('');
            //清空后查询条件为空了，再次刷新页面，就是全部数据了
            $('#mytab').bootstrapTable(('refresh')); // 很重要的一步，刷新url！
        }

```
- views
```python
        search_kw = request.GET.get('search_kw', None)
        # print('search:', search_kw)
        # 获取分页参数用于查询对应页面数据，page为第几页，num为每页数据条数,right_boundary为数据切片的右侧边界
        page = request.GET.get('page')
        num = request.GET.get('rows')
        right_boundary = int(page) * int(num)
        # print(page, num, int(page) * int(num))
        # 如果搜索关键字不为空，则根据此关键字模糊查询
        if search_kw:
            query = UserProfile.objects.filter(Q(name__contains=search_kw) | Q(email__contains=search_kw))[int(num) * (int(page) - 1):right_boundary]
            # 获取查询结果的总条数
            total = UserProfile.objects.filter(Q(name__contains=search_kw) | Q(email__contains=search_kw)).count()
            # print('11查询结果总数为:', total)
        else:
            # 根据前台传来的分页信息，页码（page）和每页条数（rows）,计算分页后的查询对象片段，例如前台传来第2页的参数，
            # rows=10，page=2，则服务端需要给前台返回[10:20]的数据片段，切片是左闭右开，所以最大只会取到下标为10到19，共10个数据
            query = UserProfile.objects.all()[int(num) * (int(page) - 1):right_boundary]
            total = UserProfile.objects.all().count()
            # print('22查询结果总数为:', total)
        ser = UserSerializer(query, many=True)
        row = ser.data
        return Response({'total': total, 'rows': row})
```

#### 增删改
> layer & forms
- 用户页面JS
```javascript

 $("#btnCreate").click(function () {
            var div = layer.open({
                type: 2,
                title: '新增',
                shadeClose: false,
                maxmin: true,
                area: ['50%', '50%'],
                content: '/system/user/create/',
                end: function () {
                    //关闭时做的事情
                    {#oDataTable.ajax.reload();#}
                    oDataTable.bootstrapTable('refresh')
                }
            });
        });

        function doUpdate(id) {
            var div = layer.open({
                type: 2,
                title: '编辑',
                shadeClose: false,
                maxmin: true,
                area: ['50%', '50%'],
                content: ["{% url 'system:user-update' %}" + '?id=' + id, 'no'],
                end: function () {
                    {#oDataTable.ajax.reload();#}
                    oDataTable.bootstrapTable('refresh')
                }
            });
        }

        function doDelete(id) {
            layer.alert('确定删除吗？', {
                title: '提示'
                , icon: 3 //0:感叹号 1：对号 2：差号 3：问号 4：小锁 5：哭脸 6：笑脸
                , time: 0 //不自动关闭
                , btn: ['YES', 'NO']
                , yes: function (index) {
                    layer.close(index);
                    $.ajax({
                        type: "POST",
                        url: "{% url 'system:user-delete' %}",
                        data: {"id": id, csrfmiddlewaretoken: '{{ csrf_token }}'},  //防止post数据时报 csrf_token 403
                        cache: false,
                        success: function (msg) {
                            if (msg.result) {
                                layer.alert('删除成功', {icon: 1});
                                {#oDataTable.ajax.reload();#}
                                oDataTable.bootstrapTable('refresh')
                            } else {
                                //alert(msg.message);
                                layer.alert('删除失败', {icon: 2});
                            }
                            return;
                        }
                    });
                }
            });
        }

        function doChangepasswd(id) {
            layer.open({
                type: 2,
                title: '修改密码',
                shadeClose: false,
                maxmin: true,
                area: ['50%', '50%'],
                content: ["{% url 'system:user-update-password' %}" + '?id=' + id, 'no'],
                end: function () {
                    oDataTable.bootstrapTable('refresh')
                }
            });
        }

```
- forms验证
```python
import re
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": "密码不能为空",
            "min_length": "密码长度最少6位数",
        }
    )

    confirm_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": "确认密码不能为空",
            "min_length": "密码长度最少6位数",
        }
    )

    class Meta:
        model = User
        fields = [
            'name', 'username', 'password', 'email', 'gender'
        ]

        error_messages = {
            "name": {"required": "姓名不能为空"},
            "username": {"required": "用户名不能为空"},
            "email": {"required": "邮箱不能为空"},
        }

    def clean(self):
        cleaned_data = super(UserCreateForm, self).clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if User.objects.filter(username=username).count():
            raise forms.ValidationError('用户名：{}已存在'.format(username))

        if password != confirm_password:
            raise forms.ValidationError("两次密码输入不一致")

        if User.objects.filter(email=email).count():
            raise forms.ValidationError('邮箱：{}已存在'.format(email))


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'gender']


class PasswordChangeForm(forms.Form):
    password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": u"密码不能为空"
        })

    confirm_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": u"确认密码不能为空"
        })

    def clean(self):
        cleaned_data = super(PasswordChangeForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("两次密码输入不一致")

```
##### 增
![image](https://github.com/MagePY27/P27N15/blob/master/img/user-add.png)
- views
```python
class USerCreateView(APIView):

    def get(self,  request):
        return render(request, 'user_create.html')

    def post(self, request):
        user_create_form = UserCreateForm(request.POST)
        if user_create_form.is_valid():
            new_user = user_create_form.save(commit=False)
            new_user.password = make_password(user_create_form.cleaned_data['password'])
            new_user.save()
            ret = {'status': 'success'}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(user_create_form.errors)
            user_create_form_errors = re.findall(pattern, errors)
            print(errors)
            ret = {
                'status': 'fail',
                'user_create_form_errors': user_create_form_errors[0]
            }

        return Response(ret)
```
##### 改
![image](https://github.com/MagePY27/P27N15/blob/master/img/user-update.png)
![image](https://github.com/MagePY27/P27N15/blob/master/img/password.png)
- views
```python
class UserUpdateView(APIView):
    def get(self, request):
        user = get_object_or_404(User, pk=int(request.GET['id']))
        return render(request, 'user_update.html', locals())

    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            user = get_object_or_404(User, pk=int(request.POST['id']))
        else:
            user = get_object_or_404(User, pk=int(request.user.id))
        user_update_form = UserUpdateForm(request.POST, instance=user)
        if user_update_form.is_valid():
            user_update_form.save()
            ret = {"status": "success"}
        else:
            ret = {"status": "fail", "message": user_update_form.errors}
        return Response(ret)


class PasswordChangeView(APIView):

    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            user = get_object_or_404(User, pk=int(request.GET.get('id')))
            ret['user'] = user
        return render(request, 'user_passwod.html', ret)

    def post(self, request):
        from apps.system.forms import PasswordChangeForm
        if 'id' in request.POST and request.POST['id']:
            user = get_object_or_404(User, pk=int(request.POST['id']))
            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                new_password = request.POST['password']
                user.set_password(new_password)
                user.save()
                ret = {'status': 'success'}
            else:
                pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
                errors = str(form.errors)
                password_change_form_errors = re.findall(pattern, errors)
                ret = {
                    'status': 'fail',
                    'password_change_form_errors': password_change_form_errors[0]
                }
        return Response(ret)
```

##### 删除
![image](https://github.com/MagePY27/P27N15/blob/master/img/user-del.png)

- views
```python
class UserDeleteView(APIView):
    """
    删除数据
    """

    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            User.objects.filter(pk=request.POST['id']).delete()
            ret['result'] = True
        return Response(ret)
```
