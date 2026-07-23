# Hermes Agent 配置快照

> 生成时间: 2026-07-24 06:00
> 包含: 模型配置、工具集、Skills、Memory、Cron 任务

---

## 一、模型配置

### 主模型 (deepseek)
- **API:** https://api.deepseek.com/v1 (chat_completions)
- **默认模型:** deepseek-v4-flash (DeepSeek V4 Flash)
- **备用模型:** deepseek-v4-pro (DeepSeek V4 Pro)

### 备用 Provider (minimax_coding)
- **API:** https://api.minimaxi.com/anthropic (anthropic_messages)
- **默认模型:** MiniMax-M2.7-highspeed
- **可用模型:** MiniMax-M2.7, M2.7-highspeed, M2.5, M2.5-highspeed, M2.1, M2.1-highspeed, M2

---

## 二、Agent 配置

| 参数 | 值 |
|------|-----|
| 最大工具轮数 | 60 |
| 超时 | 1800s (30min) |
| 推理力度 | medium |
| 默认个性 | kawaii |
| 流式响应 | 开启 |
| 上下文压缩 | 开启 (阈值0.5, 目标0.2) |

### 可用个性 (Personalities)
`catgirl`, `concise`, `creative`, `helpful`, `hype`, `kawaii` (当前), `noir`, `philosopher`, `pirate`, `shakespeare`, `surfer`, `teacher`, `technical`, `uwu`

---

## 三、工具集

### 各平台可用工具集
| 平台 | 工具集 |
|------|--------|
| CLI | hermes-cli |
| Discord | hermes-discord |
| Home Assistant | hermes-homeassistant |
| QQ Bot | hermes-qqbot |
| Signal | hermes-signal |
| Slack | hermes-slack |
| Telegram | hermes-telegram |
| WhatsApp | hermes-whatsapp |
| Yuanbao | hermes-yuanbao |

### 终端环境
- **后端:** local (本地)
- **Python:** 3.11.15 (venv: ~/.hermes/hermes-agent/venv/)
- **镜像:** nikolaik/python-nodejs:python3.11-nodejs20
- **资源:** 1 CPU / 5GB RAM / 50GB 磁盘
- **持久容器:** 是

---

## 四、所有已安装 Skills (81 个 SKILL.md)

### superpowers/ (14 个技能)
| 技能 | 说明 |
|------|------|
| `brainstorming` | 创意设计前探索需求，一问一答细化设计 |
| `dispatching-parallel-agents` | 并行派发代理处理独立任务 |
| `executing-plans` | 在新会话中分批执行计划 |
| `finishing-a-development-branch` | 4 种选项完成开发：合并/PR/保留/丢弃 |
| `requesting-code-review` | 提交代码评审 |
| `receiving-code-review` | 接收代码评审，技术验证优先 |
| `subagent-driven-development` | 子代理驱动开发 |
| `systematic-debugging` | 4 阶段系统化调试 |
| `test-driven-development` | 红-绿-重构 TDD |
| `using-git-worktrees` | 创建隔离的 git 工作树 |
| `using-superpowers` | 技能使用指南，先查技能再响应 |
| `verification-before-completion` | 声明完成前必须运行验证命令 |
| `writing-plans` | 编写实施计划 |
| `writing-skills` | TDD 式编写技能文档 |

### software-development/ (6 个技能)
- `plan` (Plan mode — 先写计划再动手)
- `requesting-code-review` (Hermes 适配版)
- `subagent-driven-development` (Hermes 适配版)
- `systematic-debugging` (Hermes 适配版)
- `test-driven-development` (Hermes 适配版)
- `writing-plans` (Hermes 适配版)

### autonomous-ai-agents/ (4 个)
- `claude-code`, `codex`, `hermes-agent`, `opencode`

### creative/ (11 个)
- `architecture-diagram`, `ascii-art`, `ascii-video`, `baoyu-infographic`, `creative-ideation`, `excalidraw`, `manim-video`, `p5js`, `pixel-art`, `popular-web-designs`, `songwriting-and-ai-music`

### mlops/ (13 个)
| 子分类 | 技能 |
|--------|------|
| general | `huggingface-hub` |
| evaluation | `lm-evaluation-harness`, `weights-and-biases` |
| inference | `llama-cpp`, `obliteratus`, `outlines`, `vllm` |
| models | `audiocraft`, `segment-anything` |
| research | `dspy` |
| training | `axolotl`, `trl-fine-tuning`, `unsloth` |
| vector-databases | (目录存在) |

### research/ (10 个)
- `arxiv`, `bing-news-search`, `blogwatcher`, `cron-news-report`, `llm-weekly-digest`, `llm-wiki`, `news-gathering-via-browser`, `polymarket`, `research-paper-writing`, `zhihu-article-fetch`

### productivity/ (7 个)
- `google-workspace`, `linear`, `maps`, `nano-pdf`, `notion`, `ocr-and-documents`, `powerpoint`

### github/ (6 个)
- `codebase-inspection`, `github-auth`, `github-code-review`, `github-issues`, `github-pr-workflow`, `github-repo-management`

### media/ (4 个)
- `gif-search`, `heartmula`, `songsee`, `youtube-content`

### apple/ (4 个)
- `apple-notes`, `apple-reminders`, `findmy`, `imessage`

### note-taking/ (3 个)
- `obsidian`, `obsidian-webdav-jianguoyun`, `url-to-obsidian-note`

### gaming/ (2 个)
- `minecraft-modpack-server`, `pokemon-player`

### ocr/ (2 个)
- `english-pdf-wrong-ocr`, `math-pdf-wrong-ocr`

### 单技能分类 (8 个)
- `data-science`: `jupyter-live-kernel`
- `devops`: `webhook-subscriptions`
- `dogfood`: `dogfood` (QA 测试)
- `email`: `himalaya`
- `mcp`: `native-mcp`
- `red-teaming`: `godmode`
- `smart-home`: `openhue`
- `social-media`: `xurl`
- `yuanbao`: `yuanbao`

### 其他 (含 DESCRIPTION.md 但无 SKILL.md 的分类)
- `agently-mail` (通过 agently-cli 操作邮件)
- `diagramming` (无 SKILL 文件)
- `domain` (无 SKILL 文件)
- `feeds` (无 SKILL 文件)
- `gifs` (无 SKILL 文件)
- `inference-sh` (无 SKILL 文件)

---

## 五、Memory 摘要

### Agent 记忆
- 当前模型: DeepSeek V4 Flash，不支持 vision_analyze
- OCR: EasyOCR 已安装但慢，英文用 Tesseract
- PDF 生成: fpdf2 + wqy-zenhei.ttc
- Obsidian vault: ~/Documents/Obsidian Vault，坚果云 WebDAV 同步
- Agent Mail (agently-cli): 已安装配置，邮箱 alphae@agent.qq.com
- 系统: Linux 容器, ~1.2GB RAM
- Skills: 81 SKILL.md (28 分类), 含 linked files 共 365 文件
- Config: 392 行，最后修改 2026-07-23

### 用户画像 (Alpha)
- 偏好中文交流
- 工作涉及产品、设计、写代码
- 语言风格简单直接
- 需求先做计划，确认后再动手
- 使用飞书作为主要平台

---

## 六、Cron 定时任务

当前有 3 个活动 cron 任务:
1. **上海松江每日天气** (`3e33eb3dff29`)
   - 调度: `0 6 * * *` (每天 6:00)
   - 已执行 89 次，状态: ok
   - 交付: 飞书

2. **每日AI科技早报** (`8f7ff97d834a`)
   - 调度: `0 8 * * *` (每天 8:00)
   - 已执行 90 次，状态: ok
   - 交付: 飞书

3. **daily-hermes-config-sync** (`615d91e235a8`)
   - 调度: `0 6 * * *` (每天 6:00)
   - 首次运行中
   - 交付: 飞书 (origin)

---

## 七、平台接入

当前已连接平台: **飞书 (Feishu)**

历史会话来源: 飞书 DM (ou_ccf563aa483729e009213dd28733bf73)
