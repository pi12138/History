from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from user.helpers import get_role


class TestViewSet(ViewSet):
    """

    """
    def list(self, request):
        role = get_role(request.user)

        return Response({"role": role[0]})
