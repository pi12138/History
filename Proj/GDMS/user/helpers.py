def get_role(auth_user):
    """
    获取用户角色(角色字符串, 角色对象)
    :param auth_user: 系统用户
    :return:
    """
    if hasattr(auth_user, 'teacher'):
        return ("teacher", auth_user.teacher)
    elif hasattr(auth_user, 'student'):
        return ("student", auth_user.student)
    elif hasattr(auth_user, 'administrator'):
        return ("administrator", auth_user.administrator)
    elif auth_user.is_superuser:
        return ("superuser", auth_user)
    else:
        return ("", None)
