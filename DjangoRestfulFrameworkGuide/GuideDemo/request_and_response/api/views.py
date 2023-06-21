from datetime import datetime

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response


class RequestViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwarg):
        data = {
            'is_request_isinstance': isinstance(request, Request),
            'query_params': request.query_params,
            'data': request.data,
            'method': request.method,
            'user': str(request.user)
        }

        return Response(data)

    def create(self, request, *args, **kwargs):
        data = {
            'is_request_isinstance': isinstance(request, Request),
            'query_params': request.query_params,
            'data': str(request.data),
            'method': request.method,
            'user': str(request.user),
            'type': str(type(request.data)),
        }
        print(request.data.get('name'))
        print(request.data.getlist('name'))
        return Response(data)


class ResponseViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        data = {
            'datetime': datetime.now()
        }
        response = Response(data)

        return response
