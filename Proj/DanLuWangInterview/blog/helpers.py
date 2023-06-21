import requests


def getAddrFromIP(ip):
    """
    根据传入ip获取ip的地理位置
    :param ip: ip
    :return: (code, msg) code为1时，msg为错误信息，code为0时msg为ip的地理位置
    """
    url = 'http://ip.taobao.com/outGetIpInfo'
    data = {
        'ip': ip,
        'accessKey': 'alibaba-inc'
    }

    signal = True
    number = 0

    while signal:
        try:
            res = requests.post(url=url, data=data)
            signal = False
        except requests.exceptions.ConnectionError as e:
            number += 1
            if number == 10:
                return 1, 'e: {}'.format(str(e))

    if res.status_code != 200:
        return 1, "status_code: {}".format(res.status_code)

    data = res.json().get('data')
    if not data:
        return 1, ""

    return 0, "{}-{}-{}-{}".format(data.get('country'), data.get('region'), data.get('city'), data.get('county'))


if __name__ == "__main__":
    print(getAddrFromIP('120.79.87.64'))
