# ComicsPuncher 漫画平台自动签到助手

基于 **GitHub Actions** 的自动签到工具，每天自动为 **哔咔漫画（PicaComic）** 和 **禁漫天堂（JMComic）** 打卡活跃。

- ✅ 无需自己的电脑或服务器，完全在 GitHub 云服务器上运行，关机也照常执行
- ✅ 账号密码存放在 GitHub Secrets 中，不会写进代码
- ✅ 每天自动运行一次，也支持手动触发
- ✅ 禁漫接口域名由 `jmcomic` 自动更新，不用担心域名变动

> 本项目基于 [RahabHub/ComicsPuncher](https://github.com/RahabHub/ComicsPuncher) 改造，适配了 GitHub Actions 运行方式。

---

## 工作原理

`.github/workflows/punch.yml` 定义了一个定时任务：

```yaml
on:
  schedule:
    - cron: '0 0 * * *'      # UTC 时间 00:00 = 北京时间 08:00
  workflow_dispatch:         # 支持在 Actions 页面手动触发
```

运行环境为 `ubuntu-latest`，每天**北京时间 08:00** 自动执行一次；也可随时手动运行。

> 注：GitHub 免费版运行器在高峰期可能把定时任务延迟数小时，属正常现象，不影响每天签到一次。

---

## 使用步骤

### 1. Fork 本仓库

点击右上角 **Fork**，把项目复制到你自己的 GitHub 账号下。

### 2. 配置账号密钥（Secret）

进入你 fork 的仓库：`Settings → Secrets and variables → Actions → New repository secret`

新建一个名为 **`ACCOUNTS`** 的 Secret，Value 填写以下 JSON：

```json
[
  {"type":"bika","username":"你的哔咔账号","password":"你的哔咔密码"},
  {"type":"jinman","username":"你的禁漫账号","password":"你的禁漫密码"}
]
```

> ⚠️ **键名 `type`、`username`、`password` 是固定的，必须原样保留，一个字都不能改！** 只需要替换引号里的账号和密码值。
> - `type` 只能是 `bika`（哔咔）或 `jinman`（禁漫）
> - 只用英文双引号 `"`、英文逗号 `,`
> - 不需要的平台可以删掉对应那一行
> - 哔咔通常用**邮箱**登录；禁漫用用户名

### 3.（可选）配置代理

如果某平台在你的网络环境下连不上，可以再加一个 Secret：

- Name：`HTTPS_PROXY`
- Value：代理地址，如 `http://127.0.0.1:7890` 或 `http://user:pass@host:port`

不需要代理就不用建这个 Secret，留空即可。

### 4. 启用 Actions 并测试

打开仓库的 **Actions** 标签页，若提示则点击启用工作流（"I understand my workflows, go ahead and enable them"）。

然后手动测试一次：

**Actions → Comic Punch → Run workflow → 选择分支 `main` → Run workflow**

等运行结束，点进日志查看签到结果。看到类似下面的输出就说明成功：

```
哔咔登录成功
哔咔签到成功！结果: ok
禁漫登录活跃成功！
金币余额: 6320
```

测试成功后，之后每天就会自动签到，无需手动操作。

---

## 常见问题（FAQ）

**Q: 日志显示 `email is not allowed to be empty` / `用戶名和密碼字段不能留空！`**

A: 说明账号没读出来。检查 `ACCOUNTS` 里的键名是否写成了 `username` / `password`（不要写成 `user`/`pwd`/你的用户名等）。本项目的日志会打印脱敏诊断信息，可直接看键名是否正确。

**Q: 哔咔登录失败 `{'code': 400, ...}`**

A: 检查账号密码是否正确（哔咔一般用邮箱），或签名算法是否需要更新。

**Q: 禁漫提示域名无法连接**

A: `jmcomic` 会自动获取最新 API 域名；若仍失败，通常是网络环境问题，可尝试配置 `HTTPS_PROXY`。

**Q: 定时任务不跑了**

A: GitHub 对个人仓库长期无活动（约 60 天）会自动暂停定时任务，偶尔手动跑一次或提交一次改动即可保活。

---

## 本地运行（可选）

如果想在自己电脑上跑：

```bash
pip install -r requirements.txt
```

然后设置环境变量 `ACCOUNTS`（JSON，格式同上），再执行：

```bash
python main.py
```

---

## 依赖

- Python 3.10+（GitHub Actions 使用 3.13）
- `requests`
- `jmcomic`

## 免责声明

本工具仅用于个人账号的每日签到打卡，请遵守各平台的相关规定。账号密码仅通过 GitHub Secrets 传递，不会明文出现在代码中。
