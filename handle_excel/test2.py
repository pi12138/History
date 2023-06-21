from pyecharts.charts import Bar, Line
import xlrd



def handle_time_list(time_list):
    """
    处理float格式的时间数据为 年/月/日 小时:分钟
    time_list: 时间列表
    return: 处理好的时间数据迭代器
    """
    new_time_list = [xlrd.xldate_as_datetime(i, 0).strftime(r'%Y/%m/%d %H:%M') for i in time_list]
    return new_time_list

data = xlrd.open_workbook('C:\\Users\\Administrator\\Desktop\\新建文件夹\\国——月\\12月.xlsx')
table = data.sheets()[0]

PM2_5 = table.col_values(0)
PM10 = table.col_values(1)
CO = table.col_values(2)
NO2 = table.col_values(3)
SO2 = table.col_values(4)
O3 = table.col_values(5)
time = table.col_values(6)


line = Line()
line.add_xaxis(handle_time_list(time[1:]))
line.add_yaxis('PM2.5', PM2_5[1:])
line.add_yaxis('PM10', PM10[1:])
line.add_yaxis('CO', CO[1:])
line.add_yaxis('NO2', NO2[1:])
line.add_yaxis('SO2', SO2[1:])
line.add_yaxis('O3', O3[1:])
line.render('./china/12.html')
# make_snapshot(snapshot, line.render(), 'test.png')