from rest_framework.routers import DefaultRouter

from todo_mvc.rest.views import TaskViewSet


router = DefaultRouter()
router.register(r'task', TaskViewSet, 'api-task')
urlpatterns = router.urls