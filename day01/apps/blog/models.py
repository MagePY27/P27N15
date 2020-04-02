from django.db import models


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField(verbose_name='标签')

    class Meta:
        verbose_name = "blog"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    class Meta:
        verbose_name = '作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255, verbose_name='标题')
    body_text = models.TextField()
    mod_date = models.DateTimeField(auto_now=True, verbose_name="修改日期")
    authors = models.ManyToManyField(Author)

    class Meta:
        verbose_name = '发帖'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.headline
