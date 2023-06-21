from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.conf import settings
# Create your views here.

def load_static_file(request, path, file):
    filepath = '{}/media/media/{}/{}'.format(settings.BASE_DIR, path, file)
    filename = "{}".format(file)
    response = StreamingHttpResponse(file_iterator(filepath))
    response['Content-Type'] = "application/octet-stream"
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)

    return response


def file_iterator(file, chunk_size=512):
    with open(file, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break