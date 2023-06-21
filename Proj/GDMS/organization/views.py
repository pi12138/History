from django.http import JsonResponse
# Create your views here.
from organization.models import Faculty, Profession, Direction, Klass, Office


def get_faculty(request):
    """获取所有学院信息"""
    query_set = Faculty.objects.all()
    facultys = []
    for i in query_set:
        faculty = {}
        faculty['id'] = i.id
        faculty['name'] = i.name
        facultys.append(faculty)

    return JsonResponse(facultys, safe=False)


def get_profession_from_faculty(request):
    ''' 根据学院id，获取学院的所有专业 '''
    faculty_id = request.GET.get('faculty_id')

    if not faculty_id:
        return JsonResponse("未传入学院参数！")

    query_set = Profession.objects.filter(faculty_id=faculty_id)
    professions = []
    for i in query_set:
        profession = {}
        profession['id'] = i.id
        profession['name'] = i.name
        professions.append(profession)
    
    return JsonResponse(professions, safe=False)


def get_direction_from_profession(request):
    ''' 根据专业id，获取所有方向 '''
    profession_id = request.GET.get("profession_id")
    if not profession_id:
        return JsonResponse("未传入专业参数！")

    query_set = Direction.objects.filter(profession_id=profession_id)
    directions = list()
    for i in query_set:
        direction = dict()
        direction['id'] = i.id
        direction['name'] = i.name
        directions.append(direction)

    return JsonResponse(directions, safe=False)


def get_klass_from_directions(request):
    ''' 根据方向id，获取所有班级 '''
    direction_id = request.GET.get('direction_id')
    if not direction_id:
        return JsonResponse("未传入方向参数!")
    
    query_set = Klass.objects.filter(direction_id=direction_id)
    klasses = []
    for i in query_set:
        klass = {}
        klass['id'] = i.id
        klass['name'] = i.name
        klasses.append(klass)

    return JsonResponse(klasses, safe=False)


def get_office_from_faculty(request):
    """
    根据学院id获取所有教研室
    :param request:
    :return:
    """
    faculty = request.GET.get('faculty')
    if not faculty:
        return JsonResponse("未传入学院参数")

    query_set = Office.objects.filter(faculty_id=faculty)
    offices = []
    for i in query_set:
        office = dict()
        office['id'] = i.id
        office['name'] = i.name
        offices.append(office)

    return JsonResponse(offices, safe=False)
