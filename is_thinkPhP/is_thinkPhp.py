# 检查页面源代码：有些网站在页面的元数据、注释或者其他地方留下了 ThinkPHP 的标记。
# 特定路径和文件：ThinkPHP 框架通常会有一些特定的文件和路径，比如 ThinkPHP 目录下的文件。
# 响应头信息：有时可以从响应头中找到特定的标志信息。
import requests


class Is_ThonkPHP(object):
    def __init__(self):
        self.context = "ThinkPHP"
    def is_thinkphp(self, url):
        try:
            response = requests.get(url)

            # 检查特定的路径和文件
            thinkphp_paths = [
                'ThinkPHP/', 'ThinkPHP.php', 'index.php?s=', 'index.php?s=/', 'index.php?s=/home/index'
            ]

            for path in thinkphp_paths:
                response = requests.get(url + path)
                if response.status_code == 200 and 'ThinkPHP' in response.text:
                    return True

            # 检查响应头信息
            if 'X-Powered-By' in response.headers:
                if 'ThinkPHP' in response.headers['X-Powered-By']:
                    return True

            # 检查页面源代码
            if 'ThinkPHP' in response.text:
                return True

            return False

        except requests.RequestException as e:
            print(f"请求过程中发生错误: {e}")
            return False
