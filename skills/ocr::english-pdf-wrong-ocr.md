---
name: english-pdf-wrong-ocr
description: 专属英语扫描PDF试卷OCR、拆题、英语错题归类、语法/词汇/完形/阅读错因分析、整理英语错题本、发送到飞书
version: 2.0.0
author: AI助手
tags: [英语, PDF, OCR, 错题整理, 飞书, fpdf2, Tesseract]
trigger:
  keywords: [英语PDF, 英语试卷, 英语错题, 整理英语错题, 英语扫描卷]
  deps: [文档解析, OCR识别, PDF生成]
---

# 英语-扫描PDF错题整理

## 前提条件
- Tesseract 5.3+ 已安装（`tesseract --version` 检查）
- 英语语言包：`tesseract --list-langs` 应有 `eng`
- Python 包：`pymupdf`（fitz）、`Pillow`、`fpdf2`、`requests`
- 飞书凭证：环境变量 `FEISHU_APP_ID` + `FEISHU_APP_SECRET`
- OCR通用脚本：`/home/agentuser/ocr_full.py`

## 第1步：OCR识别

**唯一推荐方案：Tesseract 本地 OCR**
- 经过3轮方案试错验证：OCR.space效果差→EasyOCR/PaddleOCR内存不足→Tesseract本地效果佳无限制
- 命令：`python3 /home/agentuser/ocr_full.py "<pdf_path>" "<output_dir>" "eng"`
- 输出：`<output_dir>/full_ocr.txt`

### 参数建议
- DPI: 144（fitz.Matrix(2,2)）— 清晰且内存友好
- PSM: 6（Assume uniform block）— 最适合试卷
- 语言: `eng`
- OCR每页约1-2秒，22页约30-60秒

### 不推荐方案
- ❌ OCR.space 免费API — 20次/小时限速，质量差（用户反馈"效果不好"）
- ❌ EasyOCR/PaddleOCR — PyTorch内存不足OOM（仅2GB RAM）
- ❌ Gemini/Google Vision — 用户不一定有API Key

## 第2步：阅读OCR结果

全文阅读 `full_ocr.txt`，识别题型结构，提取：
- 核心词汇和短语
- 语法考点（冠词/时态/比较级/被动语态等）
- 完形填空答案和解析
- 阅读理解要点和答案
- 句型转换规律
- 词形变化规律
- 写作题目和要求

## 第3步：生成错题整理 PDF（fpdf2）

### 核心坑点
fpdf2 的 Helvetica 仅支持 **Latin-1** 字符集。以下内容会导致报错：
- ⛔ 音标符号（ə、ɪ、θ、ʊ、æ 等）
- ⛔ 箭头 →、长破折号 —、尖引号 "" 等
- ⛔ 中文/日文/韩文字符
- ✅ 只写纯 ASCII 文本

### 推荐PDF结构（10章节，每章1页）
1. Key Vocabulary — 核心词汇与搭配
2. Pronunciation — 发音辨析（不同音素归类）
3. Grammar: Articles & Pronouns
4. Grammar: Comparison
5. Grammar: Tense & Aspect
6. Cloze Passages — 完形填空摘要+关键词
7. Reading Comprehension — 阅读要点+难句
8. Sentence Transformation — 句型转换技巧
9. Word Formation — 词形变化规律
10. Writing Guide — 写作思路+句式模板

### 代码模板
```python
from fpdf import FPDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=20)
def section(title, items):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, title, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 10)
    for item in items:
        if item.startswith("##"):
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 7, item.replace("##","").strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            pdf.set_font("Helvetica", "", 10)
        else:
            pdf.cell(0, 5.5, item.strip(), new_x="LMARGIN", new_y="NEXT")
    pdf.output("/home/agentuser/output.pdf")
```

## 第4步：发送到飞书

使用 `/home/agentuser/send_feishu_file.py` 脚本发送PDF：
1. 获取 tenant_access_token（FEISHU_APP_ID + FEISHU_APP_SECRET）
2. POST 到飞书 `/open-apis/im/v1/files` 上传文件
3. POST 到飞书 `/open-apis/im/v1/messages` 发送消息

**注意：** `receive_id_type` 必须用 `chat_id`（用 `open_id` 会报 `open_id cross app` 错误）
**OCR.space 已弃用：** 之前第一份英语 PDF 用 OCR.space 整理后用户反馈"效果不好"，改用 Tesseract 后才满意。永远不要用 OCR.space。

## 总结：这个工作流解决的核心问题
1. 扫描PDF没有可选文字 → Tesseract本地OCR
2. 72页大试卷需要批量处理 → 自动化脚本逐页OCR
3. OCR.space效果差 → 转Tesseract本地方案
4. 飞书文件发送 → 直接REST API（send_message MEDIA不支持飞书）
5. fpdf2的Helvetica不支持Unicode → 只写纯ASCII

## 用法示例
```
OCR这份英语扫描PDF，整理全部错题
把这份英语卷子整理成错题本，标注易错单词
用Tesseract重新做OCR，比OCR.space准确多了
效果不好，用本地OCR重新处理
```
