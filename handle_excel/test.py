from pyecharts.charts import Bar, Line
import xlrd


def handle_time_list(time_list):
    """
    处理float格式的时间数据为 年/月/日 小时:分钟
    time_list: 时间列表
    return: 处理好的时间数据列表
    """
    new_time_list = [xlrd.xldate_as_datetime(i, 0).strftime(r'%Y/%m/%d %H:%M') for i in time_list]
    return new_time_list

data = xlrd.open_workbook('C:\\Users\\Administrator\\Desktop\\新建文件夹\\个人-月\\12.xlsx')
table = data.sheets()[0]

PM2_5 = table.col_values(0)
PM10 = table.col_values(1)
CO = table.col_values(2)
NO2 = table.col_values(3)
SO2 = table.col_values(4)
O3 = table.col_values(5)
wind = table.col_values(6)
pressure = table.col_values(7)
water = table.col_values(8)
temperature = table.col_values(9)
humidity = table.col_values(10)
time = table.col_values(11)


line = Line()
line.add_xaxis(handle_time_list(time[1:]))
line.add_yaxis('PM2.5', PM2_5[1:])
line.add_yaxis('PM10', PM10[1:])
line.add_yaxis('CO', CO[1:])
line.add_yaxis('NO2', NO2[1:])
line.add_yaxis('SO2', SO2[1:])
line.add_yaxis('O3', O3[1:])
line.add_yaxis('风速', wind[1:])
line.add_yaxis('压强', pressure[1:])
line.add_yaxis('降水量', water[1:])
line.add_yaxis('温度', temperature[1:])
line.add_yaxis('湿度', humidity[1:])
line.render('./person/12.html')
