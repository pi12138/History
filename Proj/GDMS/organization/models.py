from django.db import models
# Create your models here.


class Faculty(models.Model):
    """
    学院模型
    """
    name = models.CharField(max_length=30, verbose_name="学院名", unique=True)
    number = models.CharField(max_length=30, verbose_name="学院编号", unique=True)
    monitor = models.CharField(max_length=30, verbose_name="院长")

    def __str__(self):
        return self.name


class Profession(models.Model):
    """
    专业模型
    """
    name = models.CharField(max_length=30, verbose_name="专业名称", unique=True)
    number = models.CharField(max_length=30, verbose_name="专业编号", unique=True)
    faculty = models.ForeignKey(to='Faculty', verbose_name="所属学院", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Direction(models.Model):
    """
    方向模型
    """
    name = models.CharField(max_length=30, verbose_name="方向名称", unique=True)
    number = models.CharField(max_length=30, verbose_name="方向编号", unique=True)
    profession = models.ForeignKey(to='Profession', verbose_name="所属专业", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Klass(models.Model):
    """
    班级模型
    """
    name = models.CharField(max_length=30, verbose_name="班级名称", unique=True)
    number = models.CharField(max_length=30, verbose_name="班级编号", unique=True)
    # faculty = models.ForeignKey(to='Faculty', verbose_name="所属学院", on_delete=models.CASCADE)
    direction = models.ForeignKey(to='Direction', verbose_name="所学方向", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Office(models.Model):
    """
    教研室模型
    """
    name = models.CharField(max_length=30, verbose_name="教研室名称", unique=True)
    number = models.CharField(max_length=30, verbose_name="教研室编号", unique=True)
    faculty = models.ForeignKey(to='Faculty', verbose_name="所属学院", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Location(models.Model):
    """
    地点模型
    """
    location_number = models.CharField(verbose_name='地点代号', max_length=100, unique=True)
    location_desc = models.TextField(verbose_name="地点详细信息描述", blank=True, null=True)


