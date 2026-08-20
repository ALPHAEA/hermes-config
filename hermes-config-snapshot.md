# Hermes Agent 配置快照

> 生成时间: 2026-08-20 06:01:22
> 包含: 模型配置、工具集、Skills、Memory、Cron 任务

---

## 一、模型配置

---

## 二、Agent 配置

| 参数 | 值 |
|------|-----|
| 最大工具轮数 | N/A |
| 超时 | 1800s |
| 推理力度 | medium |
| 默认个性 | kawaii |
| 流式响应 | 关闭 |
| 上下文压缩 | 关闭 |
| 持久容器 | 否 |

---

## 三、所有已安装 Skills

- **总技能数:** 122
- **分类数:** 37

### agently-mail (1)
- agently-mail

### apple (4)
- apple-notes, apple-reminders, findmy, imessage

### autonomous-ai-agents (4)
- claude-code, codex, hermes-agent, opencode

### computer-use (1)
- computer-use

### creative (18)
- architecture-diagram, ascii-art, ascii-video, baoyu-infographic, claude-design, comfyui, creative-ideation, design-md, excalidraw, humanizer, manim-video, p5js, pixel-art, popular-web-designs, pretext, sketch, songwriting-and-ai-music, touchdesigner-mcp

### data-science (1)
- jupyter-live-kernel

### devops (2)
- hermes-config-github-sync, webhook-subscriptions

### dogfood (1)
- dogfood

### email (1)
- himalaya

### find-skill-skillhub (1)
- find-skill-skillhub

### gaming (2)
- minecraft-modpack-server, pokemon-player

### github (6)
- codebase-inspection, github-auth, github-code-review, github-issues, github-pr-workflow, github-repo-management

### hermes-desktop-plugins (1)
- hermes-desktop-plugins

### humanizer-zh-pro (1)
- humanizer-zh-pro

### mcp (1)
- native-mcp

### media (4)
- gif-search, heartmula, songsee, youtube-content

### mlops (1)
- huggingface-hub

### mlops_evaluation (2)
- lm-evaluation-harness, weights-and-biases

### mlops_inference (4)
- llama-cpp, obliteratus, outlines, vllm

### mlops_models (2)
- audiocraft, segment-anything

### mlops_research (1)
- dspy

### mlops_training (3)
- axolotl, trl-fine-tuning, unsloth

### note-taking (4)
- note-restructure, obsidian, obsidian-webdav-jianguoyun, url-to-obsidian-note

### ocr (2)
- english-pdf-wrong-ocr, math-pdf-wrong-ocr

### productivity (10)
- airtable, google-workspace, linear, maps, nano-pdf, notion, ocr-and-documents, petdex, powerpoint, teams-meeting-pipeline

### red-teaming (1)
- godmode

### research (10)
- arxiv, bing-news-search, blogwatcher, cron-news-report, llm-weekly-digest, llm-wiki, news-gathering-via-browser, polymarket, research-paper-writing, zhihu-article-fetch

### self-improving-agent-pro-plus-new (1)
- self-improving-agent-pro-plus-new

### smart-home (1)
- openhue

### social-media (1)
- xurl

### software-development (11)
- hermes-agent-skill-authoring, node-inspect-debugger, plan, python-debugpy, requesting-code-review, simplify-code, spike, subagent-driven-development, systematic-debugging, test-driven-development, writing-plans

### superpowers (14)
- brainstorming, dispatching-parallel-agents, executing-plans, finishing-a-development-branch, receiving-code-review, requesting-code-review, subagent-driven-development, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers, verification-before-completion, writing-plans, writing-skills

### superpowers-skill (1)
- superpowers-skill

### ui-ux-pro-max (1)
- ui-ux-pro-max

### weather-style (1)
- weather-style

### web-composite-search (1)
- web-composite-search

### yuanbao (1)
- yuanbao

---

## 四、Cron 定时任务

1. **上海松江每日天气**
   - 调度: `{'kind': 'cron', 'expr': '0 6 * * *', 'display': '0 6 * * *'}`
   - 状态: ok
2. **每日AI科技早报**
   - 调度: `{'kind': 'cron', 'expr': '0 8 * * *', 'display': '0 8 * * *'}`
   - 状态: ok
3. **daily-hermes-config-sync**
   - 调度: `{'kind': 'cron', 'expr': '0 6 * * *', 'display': '0 6 * * *'}`
   - 状态: ok
---

## 五、系统信息

- **Config 文件:** 369 行
- **Skills 总数:** 122 个 (37 分类)
- **Cron 任务数:** 3 个
- **同步日期:** 2026-08-21
