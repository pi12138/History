from django.shortcuts import render
from django.views import View
# Create your views here.

from user.mixins import LoginRequiredMixin


class MessageBoardStudentView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'message_board_student.html')


class MessageBoardTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'message_board_teacher.html')


class MessageBoardAdminView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'message_board_admin.html')
