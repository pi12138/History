from django.shortcuts import render
from django.views.generic import View

from .helpers import handle_excel_info
from organization.models import Faculty, Profession, Direction, Klass, Office, Location
# Create your views here.


class ImportData(View):
    """
    导入信息
    """
    def get(self, request):
        return render(request, 'import_data.html')

    def post(self, request):
        file = request.FILES.get('file', None)
        type = request.POST.get('type', 0)
        type = int(type)
        info = '导入成功'

        if not file:
            info = "请传入文件"

        type_dict = {
            0: self.faculty_info,
            1: self.profession_info,
            2: self.direction_info,
            3: self.klass_info,
            4: self.office_info,
        }
        try:
            file_data = file.read()
            data_list = handle_excel_info(file_data)
            for data in data_list:
                type_dict[type](data)

        except Exception as e:
            info = "文件内容存在异常"
            print('error info: {}'.format(e))

        context = {
            'info': info,
            'type': type
        }

        return render(request, 'import_data.html', context)

    @staticmethod
    def faculty_info(data):
        Faculty.objects.create(name=data[0], number=data[1], monitor=data[2])

    @staticmethod
    def profession_info(data):
        Profession.objects.create(name=data[0], number=data[1],
                                  faculty=Faculty.objects.get(number=data[2])
                                  )

    @staticmethod
    def direction_info(data):
        Direction.objects.create(name=data[0], number=data[1],
                                 profession=Profession.objects.get(number=data[2])
                                 )

    @staticmethod
    def klass_info(data):
        Klass.objects.create(name=data[0], number=data[1],
                             direction=Direction.objects.get(number=data[2])
                             )

    @staticmethod
    def office_info(data):
        Office.objects.create(name=data[0], number=data[1],
                              faculty=Faculty.objects.get(number=data[2])
                              )


class ImportLocationInfo(View):
    """
    导入答辩地点信息
    """

    def get(self, request):
        return render(request, 'import_location_data.html')

    def post(self, request):
        file = request.FILES.get('file')

        context = {
            'info': '',
            'error_info': ''
        }
        error_info = list()

        if not file:
            context['info'] = '请传入文件'
            return render(request, 'import_location_data.html', context)

        try:
            file_data = file.read()
            data_list = handle_excel_info(file_data)
            for data in data_list[1:]:
                Location.objects.create(location_number=data[0], location_desc=data[1])
        except Exception as e:
            error_info.append(e)

        return render(request, 'import_location_data.html', context)
