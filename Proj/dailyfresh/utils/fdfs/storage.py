from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings


class FastDFSStorage(Storage):
    """fast dfs文件存储类"""

    def __init__(self, client_conf=None, base_url=None):
        """初始化"""
        if client_conf is None:
            client_conf = settings.FDFS_CILENT_CONF
        if base_url is None:
            base_url = settings.FDFS_URL

        self.client_conf = client_conf
        self.base_url = base_url

    def _open(self, name, mode='rb'):
        """打开文件"""
        pass

    def _save(self, name, content):
        """
        保存文件
        :param name: 选择上传文件的文件名
        :param content: 包含上传文件内容的File对象
        :return: 上传文件后fast dfs 文件存储系统返回的文件ID
        """
        # 1. 创建 Fdfs_client对象
        # client = Fdfs_client('./utils/fdfs/client.conf')
        client = Fdfs_client(self.client_conf)

        # 2. 通过文件内容上传文件
        res = client.upload_by_buffer(content.read())

        # client.upload_by_buffer()方法返回内容
        # return dict
        # {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id,
        #     'Status': 'Upload successed.',
        #     'Local file name': '',
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # } if success else None

        # 3. 判断上传是否成功，若上传失败抛出异常
        if res.get('Status') != 'Upload successed.':
            raise Exception('文件上传到 fast dfs 失败！')

        # 4. 上传成功获取返回的ID，并作为函数的返回值
        filename = res.get('Remote file_id')

        return filename

    def exists(self, name):
        """
        Django用来判断文件名是否存在的方法,
        返回True表示文件名已经存在，则不可用；
        返回False表示文件名不存在，可以使用
        """
        return False

    def url(self, name):
        """
        返回name 可以访问所引用文件内容的URL
        """
        # return "http://192.168.0.100:8888/" + name
        return self.base_url + name
