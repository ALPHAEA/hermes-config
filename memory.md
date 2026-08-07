# Memory & User Profile

> 生成时间: 2026-08-07 12:35:30
> 来源: ~/.hermes/memories/MEMORY.md + USER.md

---

## Agent 记忆

当前使用的模型是 DeepSeek V4 Flash，不支持 vision_analyze 视觉分析（返回 unknown variant `image_url` 错误）。需要从图片提取文字时，可用 EasyOCR（已安装在 hermes venv 中，但首次加载 PyTorch 很慢约30-60s），或委托 subagent 来处理耗时的 OCR 任务。fpdf2 已安装可用于生成含中文字体的 PDF，字体路径：/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc。
§
当用户发送扫描的 PDF 或截图时需要 OCR 提取中文文字时：先用 pymupdf 检查页面是否有文字（page.get_text()），如果是扫描件则用 EasyOCR（已安装在 hermes venv 中），首次加载慢约30s是因为 PyTorch 加载。PDF 生成用 fpdf2 + wqy-zenhei.ttc 字体。当前使用的 DeepSeek V4 Flash 模型不支持 vision_analyze 视觉分析（返回 unknown variant `image_url` 错误）。
§
Obsidian vault 路径：~/Documents/Obsidian Vault，通过坚果云 WebDAV 同步（账号 yizhiqiangvip@163.com）。同步脚本在 ~/Documents/Obsidian Vault/.obsidian/sync-nutstore.py，用法：python sync-nutstore.py sync（双向）、down（下载）、up（上传）。
§
OBSIDIAN_VAULT_PATH 在 ~/.bashrc 中设置，指向 ~/Documents/Obsidian Vault。
§
Agent Mail (agently-cli) 已安装配置。用户邮箱：alphae@agent.qq.com，别名 Alpha.E。CLI 版本 1.0.6，已加载 agently-mail skill。可用的命令：+list, +search, +read, +send（需两阶段确认）, +reply, +forward, +trash, attachment +download。限频：每天最多发50封，每小时200请求，每分钟10请求。token 有效期约1小时，过期后会走 device code 重新授权（流程：agently-cli auth login → 给用户授权链接 → 用户浏览器授权）。
§
- _assets 附件：必须放在 vault 顶层 _assets/ 目录下（切勿放入 NOTE/<子目录>/_assets/），目录名用 8 位 MD5（对笔记原名取 MD5 前8位），文件用 Unix 时间戳秒级命名。笔记内用 [[_assets/<md5>/<file>]] 引用（从 vault 根解析，子目录笔记也能指向顶层）
§
模型 qwen3.6-flash（custom provider）**不支持多模态**：vision_analyze 工具对本地文件和外部URL都返回 404。需要视觉分析时只能靠底层Python像素分析，无法真正识别图片内容。如果用户需要多模态能力，应切换到 Claude Sonnet/GPT-4o/Qwen-VL 等支持视觉的模型。

---

## 用户画像

用户偏好使用中文交流
§
用户名叫 Alpha，工作涉及产品、设计、写代码。语言风格要求简单直接。需求要先做计划，确认后再动手。
