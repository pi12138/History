from django.conf.urls import url

from announcement.views import AnnouncementView, AnnouncementStudentView, AnnouncementTeacherView


urlpatterns = [
    # url(r'^student_settings/$', StudentUserSettingsView.as_view(), name='student-settings'),
    url(r'^admin/$', AnnouncementView.as_view(), name='announcement-admin'),
    url(r'^teacher/$', AnnouncementTeacherView.as_view(), name='announcement-teacher'),
    url(r'^student/$', AnnouncementStudentView.as_view(), name='announcement-student'),
]
