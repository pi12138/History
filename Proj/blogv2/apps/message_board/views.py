from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MessageBoardModel
from .forms import MessageBoardModelForm
from .serializers import MessageBoardSerializer
# Create your views here.


class MessageBoardViewSet(ModelViewSet):
    queryset = MessageBoardModel.objects.all().order_by('-pub_date')
    serializer_class = MessageBoardSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    # @csrf_exempt
    # def create(self, request, *args, **kwargs):
    #     form_obj = MessageBoardModelForm(request.data)
    #     print(form_obj)
    #     if form_obj.is_valid():
    #         form_obj.save()
    #     else:
    #         return Response(form_obj.errors)
    #     return Response(form_obj.cleaned_data)