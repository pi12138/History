from rest_framework.routers import DefaultRouter

from blog.rest.views import ArticleViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'article', ArticleViewSet, 'api-article')
router.register(r'comment', CommentViewSet, 'api-comment')
urlpatterns = router.urls
