from django.views.generic import View
from django.http import JsonResponse
# Create your views here.
from apps.myblog.models import Article
from apps.comment.models import Comment


# /comment/submit/
class CommentSubmitView(View):
    """提交评论"""
    def post(self, request):

        article_id = request.POST.get('article_id')
        emali = request.POST.get('email')
        content = request.POST.get('content')

        if not all([article_id, content]):
            return JsonResponse({'res': 1, 'errmsg': '文章ID或者内容为空'})

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '该文章不存在！'})

        try:
            comment = Comment()
            comment.email = emali
            comment.content = content
            comment.article = article
            comment.save()
        except Exception as e:
            return JsonResponse({'res': 3, 'errmsg': '保存信息出错！'})

        return JsonResponse({'res': 0, 'message': "添加成功"})

