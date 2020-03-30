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

#### ORM查询


#### blog


