from django.conf.urls import url

from message_board.views import MessageBoardAdminView, MessageBoardStudentView, MessageBoardTeacherView

urlpatterns = [
    # url(r'^student_settings/$', StudentUserSettingsView.as_view(), name='student-settings'),
    url(r'^admin/$', MessageBoardAdminView.as_view(), name='message_board-admin'),
    url(r'^teacher/$', MessageBoardTeacherView.as_view(), name='message_board-teacher'),
    url(r'^student/$', MessageBoardStudentView.as_view(), name='message_board-student'),
]
