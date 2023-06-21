from .models import UserIP, UserInterviewInfo
# from .serializers import UserIPSerializer, UserInterviewInfoSerializer

def statistical_traffic(ip, path):
    """
    统计访问
    """
    user = UserIP.objects.filter(ip=ip)

    if user.exists():
        # 更新UserIP表
        user_obj = user[0]
        user_obj.count += 1
    else:
        # 更新UserIP表
        user_obj = UserIP()
        user_obj.ip = ip
        user_obj.ip_addr = user_obj.get_addr()
        user_obj.count = 1
        
    user_obj.save()
    
    # 更新UserInterviewInfo表
    UserInterviewInfo.objects.create(ip=user_obj, interview_url=path)
    