# 头像资源使用公约（Avatars Usage Contract）

> **核心硬约束**：头像**仅在裁决卡（Verdict）阶段使用**——R1/R2/R3 辩论过程禁用。
> 这是为了维持反剧场化基调——过程克制 / 结论可视化强化。

---

## 头像清单

| role_id | 文件 | 主色（背景）| 视觉锚点 |
|---------|------|----------|---------|
| data-driven | `01-data-driven.png` | 浅蓝 #A8C5E8 | 眼镜 + 柱状图 |
| user-empathy | `02-user-empathy.png` | 暖黄 #F5D17C | 暖笑 + 心形/对话气泡 |
| devils-advocate | `03-devils-advocate.png` | 暗红 #C04848 | 锐眼 + 放大镜+问号 |
| executor | `04-executor.png` | 橄榄绿 #7A8B5C | 安全帽 + 扳手 |
| strategist | `05-strategist.png` | 深紫 #3A4A7A | 沉思 + 棋子/罗盘 |
| investor | `06-investor.png` | 翡翠绿 #2E6E5C | 西装 + 趋势箭头 |
| first-principles | `07-first-principles.png` | 深紫 #5B3F8C | 科学家 + 原子符号 |
| red-team | `09-red-team.png` | 黑灰 #2A2A2A 红描边 | 兜帽 + 狙击十字 |
| bayesian-updater | `10-bayesian-updater.png` | 青色 #3A8A8A | 数学家 + 钟形曲线 |
| steelman | `11-steelman.png` | 钢灰 #6B7280 | 骑士 + 钢盾 |

---

## 使用规则

### ✅ 允许场景（仅这 4 处）

1. **立场变迁表的角色行首** —— 头像作为视觉锚点，让用户在 5-7 角色中快速定位轨迹
2. **金句精选区每条金句的署名位** —— 头像 + 角色名 + 轮次
3. **共识矩阵的支持/反对角色列** —— 用头像列表替代纯文字角色名（节省横向宽度）
4. **裁决卡顶部的"董事会名单"** —— 召集名单首次亮相

### ❌ 禁止场景

1. ❌ R1/R2/R3 任何一轮辩论发言中禁用头像（保持过程克制）
2. ❌ 不允许在头像旁加任何修饰词（"专家""博士""资深"等）
3. ❌ 不允许用头像替代正文论据——头像是定位锚点不是论据
4. ❌ 不允许在 PITFALLS / mechanisms 等内部文档中插入头像

---

## Markdown 引用语法

### 标准 inline 引用（推荐）

```markdown
<img src="../assets/avatars/01-data-driven.png" width="32" height="32" align="middle" /> **数据派**
```

### 紧凑表格行（立场变迁表用）

```markdown
| 角色 | R1 | R2 | R3 | 净变化 |
|------|----|----|----|----|
| <img src="../assets/avatars/01-data-driven.png" width="24" /> 数据派 | +0.7 | +0.3 | +0.3 | -0.4 |
```

### 金句卡片样式（金句精选区）

```markdown
> <img src="../assets/avatars/01-data-driven.png" width="48" align="left" />
>
> **「执行派算的 8 周是顺风版本，但用户派的访谈数据显示需求理解还要 3 周。」**
>
> *— 数据派, R2 [类型: 碰撞]*
```

---

## 尺寸规范

| 用途 | 像素尺寸 | width 属性 |
|------|---------|-----------|
| 内联文本对齐 | 24×24 | `width="24"` |
| 表格行首 | 32×32 | `width="32"` |
| 金句卡片 | 48×48 | `width="48"` |
| 董事会名单封面 | 64×64 | `width="64"` |

> 源文件统一 256×256，浏览器/markdown 渲染器自动缩放。

---

## 渲染降级路径

由于 markdown 渲染环境差异（Qoder chat / VS Code preview / GitHub / 纯 terminal / 邮件客户端 / Notion），按以下顺序降级：

1. **完整渲染**（自包含 HTML / Qoder chat / 现代浏览器从同 skill 目录打开）：`<img>` 标签 + 路径 → 显示头像
2. **HTML 不渲染**（部分 terminal markdown）：fallback 到 emoji 字符
3. **完全纯文本**：fallback 到角色名 + role_id 字母前缀

主持人输出裁决卡时**同时输出三层**：

```markdown
<!-- 头像层 -->
<img src="..." width="32" /> **数据派**
<!-- emoji fallback：📊 数据派 -->
<!-- text fallback：[data] 数据派 -->
```

实际只显示第一层；后两层作为 HTML 注释保留以防渲染失败。

---

## ⚠️ 跨目录加载陷阱（v0.2.2 关键工程约束）

**问题**：Chrome/Safari/Firefox 默认禁止 `file://` 协议**跨目录加载本地资源**。
若 verdict 被导出到 skill 目录之外（用户桌面 / 邮件附件 / Notion 粘贴 / `outputs/` 工作目录），相对路径 `../assets/avatars/01.png` 全部断裂——浏览器视为跨源请求并静默拒绝。

**导出时三档处理（按目标环境选）：**

| 目标环境 | 引用方式 | 是否需要内联 |
|---------|---------|------------|
| **A · skill 目录内 markdown 预览**（开发期 / 自用） | 相对路径 `../assets/avatars/01.png` | ❌ 不需要 |
| **B · 跨目录 HTML / 邮件 / Notion / 用户桌面** | base64 data URI | ✅ **必须内联** |
| **C · 纯 terminal / 不支持 HTML 的 markdown** | emoji fallback `📊` | — 直接降级 L2 |

**判定算法**：主持人输出 verdict 前先看目标路径——

```
if 目标路径 startswith skill_root:
    用相对路径
elif 目标支持 HTML（.html / .md 现代渲染器）:
    强制 base64 内联（不要赌相对路径，赌不赢）
else:
    走 emoji fallback
```

**base64 内联标准片段**：

```html
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEU...." width="32" />
```

**生成命令**（macOS / Linux 通用）：

```bash
base64 -i assets/avatars/01-data-driven.png | tr -d '\n'
```

**或一键批量内联整个 HTML**：

```python
import base64, re, os
def to_data_uri(p):
    return "data:image/png;base64," + base64.b64encode(open(p,"rb").read()).decode()

html = open(input_html).read()
html = re.sub(
    r'src="(?:file://)?([^"]+\.png)"',
    lambda m: f'src="{to_data_uri(m.group(1))}"' if os.path.exists(m.group(1)) else m.group(0),
    html
)
open(output_html, "w").write(html)
```

**代价**：单文件体积膨胀 ~10× 头像总和（10 张 256×256 PNG ≈ 700KB → base64 后 ≈ 950KB；HTML 可能到 2-3MB）。
**收益**：单文件可移植到任何环境，永不断图。
**裁决**：高不可逆决策的 verdict 必须自包含——单文件的 2.6MB 远好于发出去对方看不到头像。

---

## Emoji Fallback 映射表

```
01 数据派         → 📊
02 用户派         → 💛
03 怀疑派         → 🔍
04 执行派         → 🔧
05 战略派         → ♟️
06 投资人         → 💼
07 第一性原理派    → ⚛️
09 红队           → 🎯
10 Bayesian       → 📈
11 Steelman       → 🛡️
```

---

## 反剧场化校核（每次输出前自检）

- [ ] 头像是否仅在 verdict 阶段使用？过程发言中无头像？
- [ ] 头像旁是否未加任何"专业头衔"装饰词？
- [ ] 头像是否作为定位锚点而非论据来源？
- [ ] 立场冰冻 / 引证密度低 / 红队折扣大等坏数据是否仍然显著（未被头像装饰美化）？
- [ ] **目标导出环境已判定（A/B/C 三档）？跨目录场景已 base64 内联？**（v0.2.2）
- [ ] **emoji + text fallback 已作为 HTML 注释保留？**（防 HTML 渲染失败）

任一项违反 → 视为 v0.2 反剧场化或 v0.2.2 工程约束硬约束失败。
