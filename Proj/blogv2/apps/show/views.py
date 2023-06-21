from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.article.models import Article
from django.conf import settings
import json
# Create your views here.

def hello(request):
    return render(request, 'hello.html')

def article(request, pk):
    return render(request, 'article.html', {'pk': pk})

def index(request):
    return render(request, 'index.html')

def search(request):
    kw = request.POST.get('keyword', "")
    return render(request, 'search.html', {'keyword': kw})

def archive(request):
    return render(request, 'archive.html')

def message_board(request):
    return render(request, 'message_board.html')

def user_statistics(request):
    return render(request, 'user_statistics.html')
    
def favicon(request):
    filepath = "{}/static/image/favicon.png".format(settings.BASE_DIR)
    filename = 'favicon.ico'
    with open(filepath, 'rb') as f:
        data = f.read()

    response = HttpResponse(data)
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)

    return response