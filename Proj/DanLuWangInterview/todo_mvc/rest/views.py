from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from todo_mvc.models import Task

from todo_mvc.rest.serializers import TaskSerializer

import datetime


class TaskViewSet(viewsets.ViewSet):
    """
    任务视图集
    """
    def list(self, requets):
        query_set = Task.objects.filter(is_deleted=False)
        ser = TaskSerializer(instance=query_set, many=True)
        return Response(ser.data)

    def create(self, request):
        data = request.data
        data['create_time'] = datetime.datetime.now()

        tasks = Task.objects.filter(title=data['title'], is_deleted=True)
        if tasks.exists():
            data['is_deleted'] = False
            ser = TaskSerializer(instance=tasks[0], data=data)
        else:
            ser = TaskSerializer(data=data)

        if not ser.is_valid():
            return Response({'error': ser.errors, 'msg': '数据不合法'}, status=400)

        ser.save()
        return Response(ser.data)

    def partial_update(self, request, pk=None):
        if pk is None:
            return Response({'msg': '未传入pk参数'}, status=400)

        data = request.data
        tasks = Task.objects.filter(pk=pk, is_deleted=False)
        if not tasks.exists():
            return Response({'msg': "该任务不存在"}, status=400)

        ser = TaskSerializer(instance=tasks[0], data=data)
        if not ser.is_valid():
            return Response({'msg': '数据不合法', 'error': ser.errors}, status=400)

        ser.save()
        return Response(ser.data)

    def destroy(self, request, pk=None):
        if pk is None:
            return Response({'msg': '未传入pk参数'}, status=400)

        tasks = Task.objects.filter(pk=pk, is_deleted=False)
        if not tasks.exists():
            return Response({'msg': '该任务不存在'}, status=400)

        task = tasks[0]
        task.is_deleted = True
        task.save()

        return Response({'msg': '删除成功', 'data': 'ok'}, status=200)

    @action(methods=['post'], detail=False)
    def clear_completed(self, request):
        """
        清除已完成的task
        """
        data = request.data
        pk_list = data.get('pk_list', None)
        if pk_list is None:
            return Response({'msg': '未传入pk_list参数'}, status=400)

        tasks = Task.objects.filter(pk__in=pk_list, is_deleted=False)
        if not tasks.exists():
            return Response({'msg': '任务不存在'}, status=400)

        tasks.update(is_deleted=True)

        return Response({'msg': '删除成功', 'data': 'ok'}, status=200)
