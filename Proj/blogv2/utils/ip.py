# 自测好像不太准确
import geoip2.database


def ip_to_addr(ip):
    reader = geoip2.database.Reader('../static/GeoLite2-City.mmdb')
    response = reader.city(ip)

    country = response.country.names['zh-CN']
    province = response.subdivisions.most_specific.names["zh-CN"]
    city = response.city.names['zh-CN']

    print("{} -- {} -- {}".format(country, province, city))


if __name__ == "__main__":
    ip_to_addr('120.79.87.64')