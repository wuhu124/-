# 化学实验数据处理系统

面向化学实验数据处理的静态网页工具，包含 5 个实验、两套界面。所有
计算均在学生的浏览器中完成，不需要后端服务器，也不会上传输入数据。

## 本地生成

需要 Python 3，无第三方依赖：

```powershell
python build.py
python build_v2.py
python package.py
```

生成结果位于 `build/`。用本地静态服务器打开 `build/index.html`，或解压
生成的网页压缩包查看。`build/` 和压缩包为生成产物，不提交到源码仓库。
`package.py` 还会生成 `实验计算_源码与可部署网页.zip`，其中包含源码和
可直接上传的完整网站，适合交给他人部署。

## GitHub Pages

本仓库通过 GitHub Actions 自动部署 Pages：

1. 在仓库 **Settings → Pages** 中把发布来源设为 **GitHub Actions**。
2. 向 `main` 推送提交，或在 **Actions** 中手动运行
   “Deploy chemistry tools to GitHub Pages”。
3. 工作流会运行三个生成脚本、验证页面链接并部署首页和版本 A/B。
4. 部署成功后，从 **Settings → Pages** 或 Actions 部署任务中取得 HTTPS
   网站地址。学生可直接打开首页或具体实验链接。

线上发布操作说明也由 `package.py` 生成到 `build/部署说明.txt`。