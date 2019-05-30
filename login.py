import requests
from lxml import etree

"""
使用Session，获取登录后的Cookies，
进行登录后页面信息的爬取
"""

USERNAME = "username"
PASSWORD = "password"

class Login():
    def __init__(self):
        """
        初始化，设置Headers，一些后续需要访问的URL
        """
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'github.com',
            'Referer': 'https://github.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }
        # 登录页面URL
        self.login_url = "https://github.com/login"
        # 请求登录URL
        self.post_url = "https://github.com/session"
        self.profile_url = "https://github.com/settings/profile"
        # 初始化Session对象，维持会话，管理Cookie
        self.session = requests.Session()

    def token(self):
        """
        获取登录需要的TOKEN
        """
        # 使用Session对象访问登录页面，记录Cookies
        response = self.session.get(self.login_url, headers=self.headers)
        # 解析响应，获取token
        html = etree.HTML(response.text) # XPath解析对象
        token = html.xpath("//div//input[2]/@value")[0]
        return token

    def login(self):
        """
        请求session页面，进行登录,之后获取需要的信息
        """
        data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token(),
            'login': USERNAME,
            'password' : PASSWORD, 
            'webauthn-support': 'supported'
        }
        response = self.session.post(self.post_url, headers=self.headers, data=data)
        if response.status_code == 200:
            self.dynamics()
        
        response = self.session.get(self.profile_url, headers=self.headers)
        if response.status_code == 200:
            self.profile(response.text)

    def dynamics(self):
        """
        解析主页动态信息
        """
        print("Dynamics")

    def profile(self, response):
        """
        解析个人信息页信息
        """
        html = etree.HTML(response)
        name = html.xpath('//input[@id="user_profile_name"]/@value')[0]
        print(name)

if __name__ == "__main__":
    login = Login()
    login.login()