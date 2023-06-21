from django import template
from user.helpers import get_role

register = template.Library()


@register.filter
def get_username(val):
    role_str, role_obj = get_role(val)

    return role_obj.name 


@register.filter
def handler_none(val):
    """
    当模版中返回None时将其处理为空字符串
    如果不是该对象name
    """
    if val is None:
        return ""
    else:
        return val.name


@register.filter
def get_faculty(val):
    if hasattr(val, 'administrator'):
        return val.administrator.faculty_id
    elif hasattr(val, 'teacher'):
        return val.teacher.faculty_id
    elif hasattr(val, 'student'):
        return val.student.faculty_id
    else:
        return None
