# loon-dns-plugin-builder

这个仓库用于 **自动生成一个 Loon 插件（.plugin）**：  
从 BlackMatrix7 的国内域名规则库拉取域名列表，并把这些域名的 DNS 解析 **强制指定为阿里 DNS 的 DoH**（`https://dns.alidns.com/dns-query`），最终输出为：

- `China_AliDoH.plugin`

你在 Loon 中订阅该插件后，命中列表内的域名将统一使用 **Ali DoH** 来解析，从而实现“国内域名走指定 DNS（DoH）”的效果。

---

## ✅ 这个仓库解决什么问题？

很多时候我们想要：

- 国内站点（域名）统一走国内/阿里 DNS（最好还是 DoH 加密）
- 但又不想手动维护一大堆 `[Host]` 规则
- 并且希望规则库能随着上游自动更新

本仓库实现方式是：

1. **每天自动抓取**上游域名列表（BlackMatrix7）
2. 自动生成一个 Loon 插件：在 `[Host]` 中把域名映射到 `server:https://dns.alidns.com/dns-query`
3. 自动提交回本仓库
4. Loon 订阅这个插件后即可使用

---

## 📦 仓库结构说明

- `generate.py`  
  生成脚本：拉取上游域名列表 → 解析域名 → 生成 `China_AliDoH.plugin`

- `.github/workflows/update.yml`  
  GitHub Actions 工作流：定时运行 `generate.py`，并把生成结果 commit 回仓库

- `China_AliDoH.plugin`  
  自动生成的 Loon 插件文件（你在 Loon 里订阅的就是它）

---

## ⏱ 自动更新机制

GitHub Actions 工作流包含两种触发方式：

- **定时触发（每天一次）**  
  `cron: 0 3 * * *` → 每天 UTC 03:00 自动运行  
  （北京时区约为当天 11:00；纽约冬令时约为前一日 22:00）

- **手动触发**  
  在 GitHub 仓库的 Actions 页面可以点击 “Run workflow” 立即运行

> 注意：  
> 如果上游列表当天没有变化，脚本生成的结果也不会变，因此可能不会产生新的 commit。  
> 但工作流仍然会按计划执行。

---

## 🔧 如何在 Loon 中使用

### 1）拿到插件 Raw 链接

打开仓库中的 `China_AliDoH.plugin` 文件，点击右上角 **Raw**，复制浏览器地址栏的链接。

### 然后在 Loon 中更新外部资源/插件即可生效。
