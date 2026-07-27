# Hermes Agent 配置快照

> 生成时间: 2026-07-28 06:15:49
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
| 持久容器 | 是 |
| 会话重置 | 每日 4:00 / 闲置 1440min |
| Delegation 模型 | 继承主模型 |

### 可用个性 (Personalities)
catgirl, concise, creative, helpful, hype, kawaii (当前), noir, philosopher, pirate, shakespeare, surfer, teacher, technical, uwu

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
- **Python:** ~/.hermes/hermes-agent/venv/
- **镜像:** nikolaik/python-nodejs:python3.11-nodejs20
- **资源:** 1 CPU / 5GB RAM / 50GB 磁盘
- **持久容器:** 是

### 辅助服务
- Vision: auto provider
- Web Extract: auto provider
- Session Search: auto provider, max 3 concurrency
- MCP: auto provider
- TTS: edge (en-US-AriaNeural) / 备选: elevenlabs, openai, xai, mistral, neutts
- STT: local (whisper base)

---

## 四、所有已安装 Skills (96 个 SKILL.md)

### superpowers/ (14 个)
- brainstorming, dispatching-parallel-agents, executing-plans, finishing-a-development-branch, receiving-code-review, requesting-code-review, subagent-driven-development, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers, verification-before-completion, writing-plans, writing-skills

### creative/ (11 个)
- architecture-diagram, ascii-art, ascii-video, baoyu-infographic, creative-ideation, excalidraw, manim-video, p5js, pixel-art, popular-web-designs, songwriting-and-ai-music

### research/ (10 个)
- arxiv, bing-news-search, blogwatcher, cron-news-report, llm-weekly-digest, llm-wiki, news-gathering-via-browser, polymarket, research-paper-writing, zhihu-article-fetch

### productivity/ (7 个)
- google-workspace, linear, maps, nano-pdf, notion, ocr-and-documents, powerpoint

### github/ (6 个)
- codebase-inspection, github-auth, github-code-review, github-issues, github-pr-workflow, github-repo-management

### software-development/ (6 个)
- plan, requesting-code-review, subagent-driven-development, systematic-debugging, test-driven-development, writing-plans

### apple/ (4 个)
- apple-notes, apple-reminders, findmy, imessage

### media/ (4 个)
- gif-search, heartmula, songsee, youtube-content

### note-taking/ (4 个)
- note-restructure, obsidian, obsidian-webdav-jianguoyun, url-to-obsidian-note

### autonomous-ai-agents/ (4 个)
- claude-code, codex, hermes-agent, opencode

### mlops/ 及子分类 (13 个)
- general: huggingface-hub
- evaluation: lm-evaluation-harness, weights-and-biases
- inference: llama-cpp, obliteratus, outlines, vllm
- models: audiocraft, segment-anything
- research: dspy
- training: axolotl, trl-fine-tuning, unsloth

### gaming/ (2 个)
- minecraft-modpack-server, pokemon-player

### ocr/ (2 个)
- english-pdf-wrong-ocr, math-pdf-wrong-ocr

### 单技能分类 (10 个)
- agently-mail, data-science: jupyter-live-kernel, devops: webhook-subscriptions, dogfood, email: himalaya, mcp: native-mcp, red-teaming: godmode, smart-home: openhue, social-media: xurl, yuanbao

---

## 五、Memory 摘要

### Agent 记忆
- 当前模型: DeepSeek V4 Flash，不支持 vision_analyze
- OCR: EasyOCR 已安装但慢，英文用 Tesseract
- PDF 生成: fpdf2 + wqy-zenhei.ttc
- Obsidian vault: ~/Documents/Obsidian Vault，坚果云 WebDAV 同步
- Agent Mail (agently-cli): 已安装配置，邮箱 alphae@agent.qq.com
- 系统: Linux 容器
- Skills: 96 SKILL.md (27 分类)
- Config: 393 行

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
   - 已执行 93 次，状态: ok
   - 交付: 飞书

2. **每日AI科技早报** (`8f7ff97d834a`)
   - 调度: `0 8 * * *` (每天 8:00)
   - 已执行 94 次，状态: ok
   - 交付: 飞书

3. **daily-hermes-config-sync** (`615d91e235a8`)
   - 调度: `0 6 * * *` (每天 6:00)
   - 已执行 4 次，状态: ok
   - 交付: 飞书

---

## 七、平台接入

当前已连接平台: **飞书 (Feishu)**
