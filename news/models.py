import os

from django.contrib.auth import get_user_model
from django.db import models
from colorfield.fields import ColorField
from django.urls import reverse
from main.validators import validate_news_content_image_begin_name_with_a_letter


def get_news_cover_path(instance: 'NewsCover', filename: str):
    return os.path.join('news', instance.news.date.strftime('%Y%m%d'), 'cover.jpg')


def get_news_content_image_path(instance: 'NewsContentImage', filename: str):
    return os.path.join('news', instance.news.date.strftime('%Y%m%d'), filename)


class News(models.Model):
    HTML = 'html'
    MARKDOWN = 'md'

    RENDERS = [
        (HTML, 'html'),
        (MARKDOWN, 'markdown')
    ]

    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    url = models.CharField(max_length=60, blank=True, default=None, null=True, unique=True)
    cover = models.ImageField(max_length=120, blank=True, default='', upload_to=get_news_cover_path,)
    description = models.TextField()
    text = models.TextField()
    render_in = models.CharField(max_length=8, choices=RENDERS, null=False, blank=False, default=HTML)
    hidden = models.BooleanField(default=True)

    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=False)

    class Meta:
        verbose_name_plural = 'News'
        ordering = ('-pk',)

    def __str__(self):
        return self.title

    def get_url(self):
        if self.url:
            kwargs = {
                'url': self.url
            }
            return reverse('news:news-url', kwargs=kwargs)
        return reverse('news:news', kwargs={'pk': self.pk})


class NewsCover(models.Model):
    img = models.ImageField(max_length=120, blank=True, default='', upload_to=get_news_cover_path)
    content = models.CharField(max_length=60, null=True, blank=True, default=None)
    color = ColorField(default='#0997ef')
    news = models.OneToOneField(News, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.content if self.content else 'Empty content'


class NewsContentImage(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False,
                            validators=(validate_news_content_image_begin_name_with_a_letter,))
    img = models.ImageField(max_length=120, blank=True, default='', upload_to=get_news_content_image_path)
    news = models.ForeignKey(News, on_delete=models.SET_NULL, null=True, blank=False)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.name} ({self.img.name})'
