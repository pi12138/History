import xlrd


def handle_excel_info(filename):
    data = xlrd.open_workbook(file_contents=filename)
    table = data.sheets()[0]

    data_list = list()
    for i in range(0, table.nrows):
        values = [handle_data(j) for j in table.row_values(i)]
        data_list.append(values)

    return data_list


def handle_data(data):
    return str(data).replace(' ', '').split('.')[0]
