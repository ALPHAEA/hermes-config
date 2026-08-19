# weather-style

version: "1.0.0"
author: jm-jsjkxyjs01-zkx-505

天气 + 黄历穿衣推荐。结合当天天气和五行，推荐穿衣颜色和款式。

## 用法

```bash
python ~/.claude/skills/weather-style.py                   # 当地
python ~/.claude/skills/weather-style.py 北京               # 指定城市
python ~/.claude/skills/weather-style.py 上海 --detail      # 显示五行生克
python ~/.claude/skills/weather-style.py 深圳 --date 2026-06-01  # 指定日期
```

## 输出内容

- **天气** — 温度、体感温度、湿度、风速
- **黄历** — 天干地支、本日五行、宜忌
- **颜色推荐** — 主推色 / 辅助色 / 避免色
- **款式推荐** — 根据温度推荐的衣物品类
- **材质推荐** — 适合当日温度的布料材质
- **配饰建议** — 围巾、伞、墨镜等
- **搭配建议** — 结合五行的穿搭小贴士

## 选项

| 选项 | 说明 |
|------|------|
| `--detail` | 显示五行生克详细关系 |
| `--date YYYY-MM-DD` | 查询指定日期（默认今天） |
| `--help` | 查看帮助 |

## 原理

- 天气数据来源: [wttr.in](https://wttr.in)（免费，无需 API Key）
- 日柱天干地支: 基于公历日期的数学计算
- 颜色对应: 五行 → 标准配色方案
- 款式对应: 体感温度区间 → 衣物类型
