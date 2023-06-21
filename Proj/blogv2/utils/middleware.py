# 做一些统计操作
from apps.user_statistics.helper import statistical_traffic
import requests


class StatisticalTrafficMiddleware:
    """
    统计访问量
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        return self.get_response(request)
        
    def process_view(self, request, view_func, view_args, view_kwargs):
                
        ip = request.META.get("REMOTE_ADDR", "")
        path = request.path

        statistical_traffic(ip, path)
        return None

    def get_addr(self, ip):
        # 调用第三方接口获取ip的地理位置信息
        url = "http://ip.360.cn/IPQuery/ipquery?ip={}".format(ip)
        response = requests.get(url)

        return response.json()['data']
