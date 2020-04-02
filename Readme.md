#### URL
```python
# urls
path('hello/<int:year>/<int:month>/', HelloView.as_view(), name='hello'),

# views
class HelloView(APIView):
    def get(self, request, **kwargs):
        year = kwargs.get('year')
        month = kwargs.get('month')

        return Response({'year': year, 'month': month})

    def post(self,  requst):
        print("method:", requst.method)
        print("body:",  requst.body)
        print("post:",  requst.POST)
        print("dict:",  QueryDict(requst.body).dict())

        return Response('post')
```

#### day2
- 分页
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

