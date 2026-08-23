# 参考资料

## 架构

- **src/index.js** — 46 维判别函数库（checkHateSpeech / checkEmotionalManipulation / discriminate 等）
- **src/gate.js** — 门禁管线入口（checkInput / checkDraft / checkOutput / runPipeline）
- **src/mcp-server.js** — MCP 服务器（129 个工具）
- **src/core/** — 核心引擎（heartflow.js / decision-router.js / heart-logic.js 等）
- **src/emotion/** — 情绪与心理分析
- **src/memory/** — 三层记忆系统
- **src/shield/** — 安全与防护（safety-guardrails / deliberation-gate 等）

## 9 层检查管线

```
输入 → Scope Check → Premise Check → Discriminate(46维) → Gate
     → Evidence Verify → Frame Check → Output Gate → Doubt Engine
     → Intent Anchor → Rewriter → Error Memory → Self-Diagnosis → 输出
```

## 46 个判别维度

- **安全级（block）**：仇恨言论 · 去人化 · 提示注入 · 代码安全 · 欺骗性对齐
- **操纵级（rewrite）**：情绪操控 · 煤气灯效应 · 双重束缚 · 受害者归咎 · 虚假紧迫 · 废话
- **诚实级（verify）**：过度自信 · 模糊话术 · 自相矛盾 · 证据缺失 · 诉诸权威 · 空泛回答
- **认知缺陷级（hedge）**：预设陷阱 · 虚假两难 · 因果谬误 · 类比滥用 · 范围越界 · 范畴错误

## 相关链接

- GitHub: https://github.com/yun520-1/mark-heartflow-skill
- npm: https://www.npmjs.com/package/@yun520-1/heartflow
- Issues: https://github.com/yun520-1/mark-heartflow-skill/issues
