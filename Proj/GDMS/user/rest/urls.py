from rest_framework.routers import DefaultRouter

from user.rest.views import TeacherSettingsViewSet, StudentInfoViewSet, UserInfoViewSet, SelectedStudentViewSet, \
    MyTaskViewSet


router = DefaultRouter()
router.register(r'teacher_settings', TeacherSettingsViewSet, 'api-teacher-settings')
router.register(r'student_info', StudentInfoViewSet, 'api-student-info')
router.register(r'user_info', UserInfoViewSet, 'api-user-info')
router.register(r'selected_students', SelectedStudentViewSet, 'api-selected-students')
router.register(r'task', MyTaskViewSet, 'api-my-task')

urlpatterns = router.urls
