from django.shortcuts import render
from .models import articles
from django.urls import reverse

def article_list_view(request):
    articlesObj = articles.objects.all()
    args = {'articles': articlesObj}
    return render(request, 'articles.html', args)

def article_view(request, article_pk):
    article = articles.objects.get(pk=article_pk)
    args = {
        'article': article
    }
    return render(request, 'article.html', args)
