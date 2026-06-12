# 立场变迁的视觉化模板（v0.2.1 新增）

> 配套 `mind-change-table.md`——同样数据，**三层渲染**保底到增强。
> **核心硬约束**：图形化仅在 verdict 阶段使用；**坏数据必须仍然难看**（不允许图形美化立场冰冻 / 引证密度低等失败信号）。

---

## 三层渲染原则

| 层 | 形式 | 渲染保证 | 何时输出 |
|----|------|---------|---------|
| L1 文本 | Markdown 表格 | 100% 任何环境 | **必输** |
| L2 Sparkline | Unicode block 字符 | 100% 任何环境 | **必输** |
| L3 SVG | 内联 `<svg>` 折线图 | Qoder/VSCode/浏览器 | 推荐输出（可选关闭） |

**文本层永远不能省略**——即使 SVG 渲染成功，文本表格也必须在 SVG 上方保留。
理由：文本是真实数据载体，图是辅助；若 SVG 渲染失败，用户仍能消化结论。

---

## L2 · Unicode Sparkline 算法

### 字符集

5 级阶梯（自下而上）：`▁ ▂ ▃ ▄ ▅ ▆ ▇ █`

实际使用的 8 级映射（含中性点）：

```
立场值 → 字符
-1.0 ~ -0.75  → ▁
-0.75 ~ -0.5  → ▂
-0.5 ~ -0.25  → ▃
-0.25 ~ 0     → ▄
0 ~ 0.25      → ▅
0.25 ~ 0.5    → ▆
0.5 ~ 0.75    → ▇
0.75 ~ 1.0    → █
```

> 中位线 0.0 = `▄` / `▅` 交界（按符号选下/上）

### 输出格式（嵌入立场变迁表）

```markdown
| 角色 | R1 | R2 | R3 | Sparkline | 净变化 |
|------|----|----|----|-----------|----|
| <img src="../assets/avatars/01-data-driven.png" width="24" /> 数据派 | +0.7 | +0.3 | +0.3 | `▇▆▆` | -0.4 ⬇️ |
| <img src="../assets/avatars/02-user-empathy.png" width="24" /> 用户派 | -0.3 | -0.3 | -0.5 | `▃▃▂` | -0.2 ⬇️ |
| <img src="../assets/avatars/03-devils-advocate.png" width="24" /> 怀疑派 | -0.7 | -0.5 | -0.3 | `▂▃▃` | +0.4 ⬆️ |
| <img src="../assets/avatars/06-investor.png" width="24" /> 投资人 | 0.0 | +0.3 | +0.5 | `▄▆▇` | +0.5 ⬆️ |
```

### 净变化方向标识

- `⬆️` 净 +0.3 以上（正向移动）
- `⬇️` 净 -0.3 以上（负向移动）
- `→` 绝对值 < 0.1（**立场冰冻警示**——此符号本身就是坏信号视觉化）
- `↕️` 多次反复变动 |R2-R1| + |R3-R2| > |R3-R1| + 0.4

### 整体趋势行

```
**整体 sparkline**：`▄▅▅` 平均 +0.04 → +0.14 → +0.14（轻度向支持移动 +0.10）
```

---

## L3 · SVG 折线图模板

### 单角色横向 Sparkline SVG（可嵌入表格行）

```svg
<svg width="80" height="24" viewBox="0 0 80 24" xmlns="http://www.w3.org/2000/svg">
  <!-- 基线 0.0 -->
  <line x1="0" y1="12" x2="80" y2="12" stroke="#CCC" stroke-width="0.5" stroke-dasharray="2,2"/>
  <!-- 立场轨迹（R1 R2 R3 三点）-->
  <polyline points="10,4 40,12 70,12" fill="none" stroke="#3A6FB0" stroke-width="2"/>
  <!-- 节点 -->
  <circle cx="10" cy="4" r="2.5" fill="#3A6FB0"/>
  <circle cx="40" cy="12" r="2.5" fill="#3A6FB0"/>
  <circle cx="70" cy="12" r="2.5" fill="#3A6FB0"/>
</svg>
```

**坐标映射**：
- X 轴：R1 = x10, R2 = x40, R3 = x70（4 轮则 10/30/50/70）
- Y 轴：+1.0 = y0（顶）, 0 = y12（中）, -1.0 = y24（底）
- 即 `y = 12 - (立场值 × 12)`

### 多角色叠加折线图（裁决卡末位完整图）

```svg
<svg width="600" height="240" viewBox="0 0 600 240" xmlns="http://www.w3.org/2000/svg">
  <!-- 背景 + 网格 -->
  <rect width="600" height="240" fill="#FAFAFA"/>
  <line x1="80" y1="120" x2="560" y2="120" stroke="#999" stroke-width="1"/>
  <line x1="80" y1="20" x2="560" y2="20" stroke="#DDD" stroke-dasharray="3,3"/>
  <line x1="80" y1="220" x2="560" y2="220" stroke="#DDD" stroke-dasharray="3,3"/>

  <!-- Y 轴标签 -->
  <text x="70" y="24" text-anchor="end" font-size="10" fill="#666">+1.0</text>
  <text x="70" y="124" text-anchor="end" font-size="10" fill="#666">0.0</text>
  <text x="70" y="224" text-anchor="end" font-size="10" fill="#666">-1.0</text>

  <!-- X 轴标签 R1/R2/R3 -->
  <text x="160" y="235" text-anchor="middle" font-size="11" fill="#333">R1</text>
  <text x="320" y="235" text-anchor="middle" font-size="11" fill="#333">R2</text>
  <text x="480" y="235" text-anchor="middle" font-size="11" fill="#333">R3</text>

  <!-- 角色轨迹（每条用角色专属色）-->
  <!-- 数据派 (蓝) +0.7 → +0.3 → +0.3 -->
  <polyline points="160,50 320,84 480,84" fill="none" stroke="#3A6FB0" stroke-width="2"/>
  <!-- 用户派 (黄) -0.3 → -0.3 → -0.5 -->
  <polyline points="160,144 320,144 480,160" fill="none" stroke="#D4A03B" stroke-width="2"/>
  <!-- 怀疑派 (红) -0.7 → -0.5 → -0.3 -->
  <polyline points="160,190 320,170 480,144" fill="none" stroke="#C04848" stroke-width="2"/>
  <!-- 投资人 (绿) 0 → +0.3 → +0.5 -->
  <polyline points="160,120 320,84 480,60" fill="none" stroke="#2E6E5C" stroke-width="2"/>

  <!-- 节点圆点（按角色色）-->
  <!-- 此处省略：每个角色 3 个 circle 节点 -->

  <!-- 图例 -->
  <g transform="translate(80, 5)">
    <rect width="10" height="10" fill="#3A6FB0"/>
    <text x="14" y="9" font-size="10">数据派</text>
    <rect x="70" width="10" height="10" fill="#D4A03B"/>
    <text x="84" y="9" font-size="10">用户派</text>
    <rect x="140" width="10" height="10" fill="#C04848"/>
    <text x="154" y="9" font-size="10">怀疑派</text>
    <rect x="210" width="10" height="10" fill="#2E6E5C"/>
    <text x="224" y="9" font-size="10">投资人</text>
  </g>
</svg>
```

### 角色专属色（对齐头像背景色）

```
01 data-driven       → #3A6FB0 (蓝)
02 user-empathy      → #D4A03B (黄)
03 devils-advocate   → #C04848 (红)
04 executor          → #7A8B5C (橄榄)
05 strategist        → #3A4A7A (深紫)
06 investor          → #2E6E5C (翡翠)
07 first-principles  → #5B3F8C (深紫红)
09 red-team          → #2A2A2A (黑)
10 bayesian          → #3A8A8A (青)
11 steelman          → #6B7280 (钢灰)
```

---

## 坏数据反美化规则

为防止图形美化失败信号，强制以下规则：

### 立场冰冻警示

若 |净变化| < 0.1：
- L2 Sparkline 字符必须为 `→` 或 `▄▄▄`（视觉上"无变化")
- L3 SVG 该角色折线**强制描红边**（`stroke="#C04848"`）+ 折线**虚线化**（`stroke-dasharray="4,4"`）
- 表格"净变化"列加 `⚠️ 立场冰冻` 后缀

### 引证密度警示

若引证密度 < 60%：
- L3 SVG 整图**顶部加红色警告条**（`<rect width="100%" height="8" fill="#C04848"/>`）
- 警告条上叠白字"⚠️ 引证密度 <60%, 结论不应作为重要决策依据"

### 立场反复警示

若同角色在 R1→R2 和 R2→R3 出现反向变化（|R2-R1| + |R3-R2| > |R3-R1| + 0.4）：
- L2 Sparkline 加 `↕️` 后缀
- L3 SVG 该折线添加**橙色警告点**在反复峰处

---

## 输出顺序（裁决卡内）

```markdown
## 立场变迁

### L1 数据表（永远输出）
[完整表格 + 关键转折点]

### L2 Sparkline（永远输出）
[每行 ▇▆▆ 一目了然]

### L3 视觉图（推荐输出，deep mode 必出）
<svg>...</svg>

### 整体趋势 + 危险信号告警
- 整体平均净变化绝对值: 0.32 ✅ 高质量辩论
- 立场冰冻角色: 0
- 引证密度: 87% ✅
```

---

## 实现指引

主持人输出立场变迁部分时按此顺序生成：

1. 计算每角色每轮立场值（按 mind-change-table.md 算法）
2. 推出 sparkline 字符（按上述 8 级映射）
3. 拼出 L1 表格（含头像 inline + sparkline 列 + 净变化方向 emoji）
4. 计算危险信号（冰冻 / 反复 / 引证低）
5. 决定是否输出 L3 SVG（deep mode = 必出 / standard = 可选 / fast = 不出）
6. 拼接 svg 字符串（按角色专属色 + 警示规则）
7. 整体趋势行 + 危险信号告警

确保 L1+L2 永远输出——L3 是增强，不是依赖。
