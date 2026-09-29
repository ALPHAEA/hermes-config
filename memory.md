# Memory

## Agent 记忆
扫描PDF/截图OCR：先 pymupdf page.get_text() 查文字层，扫描件用 EasyOCR（已装 hermes venv，首次加载 PyTorch 约30-60s，耗时可委托 subagent）。PDF 生成用 fpdf2 + 字体 /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc。DeepSeek V4 Flash 不支持 vision_analyze（unknown variant `image_url`）。
§
Obsidian vault 路径：~/Documents/Obsidian Vault，通过坚果云 WebDAV 同步（账号 yizhiqiangvip@163.com）。同步脚本在 ~/Documents/Obsidian Vault/.obsidian/sync-nutstore.py，用法：python sync-nutstore.py sync（双向）、down（下载）、up（上传）。
§
OBSIDIAN_VAULT_PATH 在 ~/.bashrc 中设置，指向 ~/Documents/Obsidian Vault。
§
Agent Mail (agently-cli) 已安装配置。用户邮箱：alphae@agent.qq.com，别名 Alpha.E。CLI 版本 1.0.6，已加载 agently-mail skill。可用的命令：+list, +search, +read, +send（需两阶段确认）, +reply, +forward, +trash, attachment +download。限频：每天最多发50封，每小时200请求，每分钟10请求。token 有效期约1小时，过期后会走 device code 重新授权（流程：agently-cli auth login → 给用户授权链接 → 用户浏览器授权）。
§
- _assets 附件：必须放在 vault 顶层 _assets/ 目录下（切勿放入 NOTE/<子目录>/_assets/），目录名用 8 位 MD5（对笔记原名取 MD5 前8位），文件用 Unix 时间戳秒级命名。笔记内用 [[_assets/<md5>/<file>]] 引用（从 vault 根解析，子目录笔记也能指向顶层）
§
用户对每日早报（cron job 8f7ff97d834a，每天8:00）的格式要求：新闻每条必须带来源+时间+具体数字，表格呈现榜单，国产模型标🇨🇳，结尾2-3条核心结论，一屏可读。曾因输出10段重复废话被用户批评，严禁重复内容。早报包含两板块：AI行业新闻(Google News抓取) + 全球大模型对比(LMArena实时榜单)。
§
头条文章抓取：桌面页 requests 只得空JS壳，须用移动端API https://m.toutiao.com/i{article_id}/info/（iPhone UA），JSON data 含 title/content(HTML)/publish_time(unix秒)；图片域名 p*-sign.toutiaoimg.com 无防盗链（带 Referer 直接下载）。HTML图片→本地文件映射必须按出现顺序替换，禁止URL模糊匹配（头条图共享 tos-cn-i-<appid> 前缀，模糊匹配会把所有图映射到第一张）。
§
腾讯云开发者社区文章（cloud.tencent.com/developer/article/N）：curl+UA 直接拿到完整静态 HTML，正文在 <div class="rno-markdown new-version">，用 BeautifulSoup 转 Markdown 即可，无需浏览器。注意页面尾部的 qcloudimg 二维码/备案图不是正文图，须排除；发布日期在 HTML 中形如 2026-06-30 10:22:30（或 createTime unix 秒）。url-to-obsidian-note skill 是手写技能，curator 补丁会被拒绝，站点配方记在这里。
§
飞书文档(feishu.cn/wiki)抓取：限流页"页面访问人数过多"→点Refresh等30s重试。正文虚拟滚动：容器.bear-web-x-container，采集data-block-id+docx-*-block类（heading/text/bullet/code/image），scrollTop步进400px每步220ms，记rect.top+scrollTop作位置，收Map按pos排序拼MD。图片是blob: URL需登录态：curl下载返回code:5 Login Required，CSP拦截外部POST；唯一导出法=滚到图可见处canvas.drawImage→toDataURL('image/jpeg',0.7)（宽900约40-60KB/张）存window变量，分批经browser_console取回base64落盘。console单次30s超时须分段；浏览器会话可能中途重置，数据尽快取回。url-to-obsidian-note是手写技能curator补丁会被拒，配方记这里。

## 用户画像
用户偏好使用中文交流
§
用户名叫 Alpha，工作涉及产品、设计、写代码。语言风格要求简单直接。需求要先做计划，确认后再动手。
