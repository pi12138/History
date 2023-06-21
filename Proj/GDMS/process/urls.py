from django.conf.urls import url

from .views import TeacherProcess, AdminProcess, StudentProcess


urlpatterns = [
    # url(r'^student_settings/$', StudentUserSettingsView.as_view(), name='student-settings'),
    url(r'^teacher/$', TeacherProcess.as_view(), name='teacher'),
    url(r'^admin/$', AdminProcess.as_view(), name='admin'),
    url(r'^student/$', StudentProcess.as_view(), name='student')
]
