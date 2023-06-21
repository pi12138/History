from django.shortcuts import render
from django.views.generic import View
# from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.
from apps.myblog.models import Article
from apps.comment.models import Comment


# 127.0.0.1:8000
class IndexView(View):
    """首页"""
    def get(self, request, index):

        if not index:
            index = 1

        articles = Article.objects.all().order_by('-update_time')
        comments = Comment.objects.all().order_by('-pub_date')

        paginator = Paginator(articles, 7)
        num_pages = int(paginator.num_pages)
        index = int(index)

        if index > num_pages:
            index = 1

        page = paginator.page(index)

        # 进行页码控制，页面上最多显示5个页码
        #     总页数小于5页，页面上显示所有页码
        #     如果当前页是前三页，显示1-5页
        #     如果当前页是后三页，显示后5页，
        #     其他情况，显示当前页的前两页，当前页，当前页的后两页
        if num_pages < 5:
            page_list = range(1, num_pages+1)
        elif index <= 3:
            page_list = range(1, 6)
        elif num_pages - 3 < index:
            page_list = range(num_pages-4, num_pages+1)
        else:
            page_list = range(index-2, index+3)

        context = {
            'articles': page,
            'page_list': page_list,
            'comments': comments[:5],
        }
        return render(request, 'myblog/index.html', context)


# /article/文章id
class ArticleShowView(View):
    """查看文章"""
    def get(self, request, article_id):

        if not article_id:
            return render(request, 'error.html', {'errmsg': '未传入文章ID!'})

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return render(request, 'error.html', {'errmsg': '该文章不存在！'})

        try:
            comment_list = Comment.objects.filter(article=article).order_by('-pub_date')
        except Exception as e:
            comment_list = []

        try:
            similar_articles_list = Article.objects.filter(Q(title__icontains=article.category) | Q(category__icontains=article.category)).exclude(id=article_id).order_by('-pub_date')
        except Exception as e:
            similar_articles_list = []

        context = {
            'article': article,
            'comment_list': comment_list,
            'similar_articles_list': similar_articles_list,
        }

        return render(request, 'myblog/article.html', context)


# /article/search/
class ArticleSearchView(View):
    """搜索文章"""
    def post(self, request):
        search = request.POST.get('search')

        if not search:
            return render(request, 'error.html', {'errmsg': '搜索内容为空！'})

        try:
            search_result = Article.objects.filter(Q(title__icontains=search) | Q(category__icontains=search)).order_by('-update_time')
        except Exception as e:
            return render(request, 'error.html', {'errmsg': e})

        comments = Comment.objects.all().order_by('-pub_date')

        context = {
            'search': search,
            'search_result': search_result,
            'comments': comments,
        }

        return render(request, 'myblog/search_result.html', context)


