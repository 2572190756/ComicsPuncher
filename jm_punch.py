import logging

from jmcomic import JmOption


class JmPuncher:
    """禁漫天堂自动签到类（基于 jmcomic，自动获取当前可用域名）"""

    def __init__(self, username, password, proxy=None):
        self.username = username
        self.password = password
        self.proxy = proxy

    def run(self):
        try:
            config = {
                "auth": {
                    "username": self.username,
                    "password": self.password,
                }
            }
            if self.proxy:
                config["client"] = {
                    "postman": {
                        "meta_data": {
                            "proxies": {
                                "http": self.proxy,
                                "https": self.proxy,
                            }
                        }
                    }
                }

            option = JmOption.construct(config)
            client = option.build_jm_client()
            logging.info("正在尝试登录禁漫（用户: %s）...", self.username)

            resp = client.login(self.username, self.password)
            user_data = resp.res_data
            logging.info("禁漫登录活跃成功！")
            logging.info("用户名: %s", user_data.get("username"))
            logging.info("金币余额: %s", user_data.get("coin"))
        except Exception as e:
            logging.error("禁漫运行异常: %s", e)
