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


def load_accounts():
    """兼容两种 ACCOUNTS 格式：
    1) 旧项目的 JSON: [{"type":"bika","username":"u","password":"p"}, ...]
    2) 新项目的格式: u1,p1|u2,p2 （两个平台共用）
    """
    raw = os.environ.get("ACCOUNTS", "").strip()
    if not raw:
        raise SystemExit("未配置 ACCOUNTS 环境变量，请检查仓库 Secret")

    if raw.startswith("["):
        accounts = []
        for item in json.loads(raw):
            accounts.append(
                (
                    str(item.get("type", "both")).lower(),
                    str(item.get("username", "")),
                    str(item.get("password", "")),
                )
            )
        return accounts

    accounts = []
    for part in raw.split("|"):
        part = part.strip()
        if not part or "," not in part:
            continue
        username, password = part.split(",", 1)
        accounts.append(("both", username.strip(), password.strip()))
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
