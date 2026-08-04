# Memory
## Agent 记忆
     1|当前使用的模型是 DeepSeek V4 Flash，不支持 vision_analyze 视觉分析（返回 unknown variant `image_url` 错误）。需要从图片提取文字时，可用 EasyOCR（已安装在 hermes venv 中，但首次加载 PyTorch 很慢约30-60s），或委托 subagent 来处理耗时的 OCR 任务。fpdf2 已安装可用于生成含中文字体的 PDF，字体路径：/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc。
     2|§
     3|当用户发送扫描的 PDF 或截图时需要 OCR 提取中文文字时：先用 pymupdf 检查页面是否有文字（page.get_text()），如果是扫描件则用 EasyOCR（已安装在 hermes venv 中），首次加载慢约30s是因为 PyTorch 加载。PDF 生成用 fpdf2 + wqy-zenhei.ttc 字体。当前使用的 DeepSeek V4 Flash 模型不支持 vision_analyze 视觉分析（返回 unknown variant `image_url` 错误）。
     4|§
     5|Obsidian vault 路径：~/Documents/Obsidian Vault，通过坚果云 WebDAV 同步（账号 yizhiqiangvip@163.com）。同步脚本在 ~/Documents/Obsidian Vault/.obsidian/sync-nutstore.py，用法：python sync-nutstore.py sync（双向）、down（下载）、up（上传）。
     6|§
     7|OBSIDIAN_VAULT_PATH 在 ~/.bashrc 中设置，指向 ~/Documents/Obsidian Vault。
     8|§
     9|Agent Mail (agently-cli) 已安装配置。用户邮箱：alphae@agent.qq.com，别名 Alpha.E。CLI 版本 1.0.6，已加载 agently-mail skill。可用的命令：+list, +search, +read, +send（需两阶段确认）, +reply, +forward, +trash, attachment +download。限频：每天最多发50封，每小时200请求，每分钟10请求。token 有效期约1小时，过期后会走 device code 重新授权（流程：agently-cli auth login → 给用户授权链接 → 用户浏览器授权）。
    10|§
    11|Obsidian 笔记规范（NOTE 目录）：
    12|- 分类维度：按技术/主题分目录（Java/, Network/, SmartHome/, IDE/ 等），可自动新增或拆分二级目录
    13|- 文件名：【source】title.md，从 frontmatter 取值。title 中 /→-，:→：，?→？，*→·，"→'，<→《，>→》 ，|→-
    14|- frontmatter 模板：title / source / source_url / author / created / tags / assets
    15|- assets 字段: "[[_assets/8位MD5哈希]]" 指向附件目录，可点击跳转
    16|- _assets 附件：目录用 8 位 MD5 哈希（对笔记原名取 MD5 前8位），文件用 Unix 时间戳秒级命名
    17|- 同步：sync-nutstore.py sync（双向）或 up（仅上传）。远程旧文件需手动 curl DELETE 清理。
## 用户画像
     1|用户偏好使用中文交流
     2|§
     3|用户名叫 Alpha，工作涉及产品、设计、写代码。语言风格要求简单直接。需求要先做计划，确认后再动手。
