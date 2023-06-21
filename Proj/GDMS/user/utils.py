from .helpers import get_role


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    :param token:
    :param user:
    :param request:
    :return:
    """
    return {
        'token': token,
        'id': user.id,
        'role': get_role(user)
    }
