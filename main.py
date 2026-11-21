import json
import logging
import os

from jm_punch import JmPuncher
from pica_punch import PicaPuncher

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def normalize_proxy(value):
    value = (value or "").strip()
    if not value:
        return ""
    if "://" not in value:
        value = "http://" + value
    return value


USER_KEYS = ("username", "user", "email", "account", "name", "用户名", "账号", "邮箱")
PASSWORD_KEYS = ("password", "pwd", "pass", "pw", "密码")


def pick(item, keys):
    for key in keys:
        value = item.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def load_accounts():
    """兼容多种 ACCOUNTS 写法，并输出脱敏诊断信息。"""
    raw = os.environ.get("ACCOUNTS", "").strip()
    if not raw:
        raise SystemExit("未配置 ACCOUNTS 环境变量，请检查仓库 Secret")

    logging.info("ACCOUNTS 原始长度: %d，首字符: %s", len(raw), raw[:1])

    if raw.startswith("["):
        try:
            items = json.loads(raw)
        except Exception as e:
            raise SystemExit(f"ACCOUNTS 不是合法 JSON: {e}")

        accounts = []
        for index, item in enumerate(items, 1):
            if not isinstance(item, dict):
                logging.error("第 %d 项不是对象，已跳过: %s", index, type(item).__name__)
                continue
            username = pick(item, USER_KEYS)
            password = pick(item, PASSWORD_KEYS)
            logging.info(
                "账号项 %d 键名=%s | 类型=%s | 用户名非空=%s | 密码非空=%s",
                index,
                list(item.keys()),
                item.get("type", "both"),
                bool(username),
                bool(password),
            )
            accounts.append(
                (
                    str(item.get("type", "both")).lower(),
                    username,
                    password,
                )
            )
        return accounts

    normalized = raw.replace("，", ",").replace("｜", "|").replace("│", "|")
    accounts = []
    for part in normalized.split("|"):
        part = part.strip()
        if not part or "," not in part:
            continue
        username, password = part.split(",", 1)
        accounts.append(("both", username.strip(), password.strip()))
    logging.info("按管道格式解析出 %d 个账号", len(accounts))
    return accounts


if __name__ == "__main__":
    proxy = normalize_proxy(
        os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY") or ""
    )
    accounts = load_accounts()

    for index, (kind, username, password) in enumerate(accounts, 1):
        logging.info("===== 第 %d 个账号 (%s) =====", index, kind)

        if kind in ("bika", "pica", "both"):
            PicaPuncher(username, password, proxy).run()
        elif kind in ("jinman", "jm"):
            JmPuncher(username, password, proxy).run()
        else:
            logging.warning("未知账号类型 %s，已跳过", kind)
