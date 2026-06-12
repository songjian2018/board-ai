# 金句卡片样式模板（v0.2.1 新增）

> **使用约束**：金句卡片**仅在 verdict 阶段的金句精选区使用**——R1/R2/R3 辩论过程禁用。
> **反剧场化保护**：金句来源仍按 `highlight-extraction.md` 4 标准客观提取；卡片只是视觉容器，不影响内容硬约束。

---

## 卡片样式（4 种类型，按金句类型选）

### 1. 碰撞类（Collision）— 红色边

```markdown
<table>
<tr>
<td width="60" valign="top"><img src="../assets/avatars/03-devils-advocate.png" width="48"/></td>
<td>
<strong style="color:#C04848">⚔️ [碰撞]</strong><br/>
<strong>「执行派算的 8 周是顺风版本，但用户派的访谈数据显示需求理解还要 3 周，真实交付不会早于 11 周。」</strong><br/>
<small>— 数据派 · R2</small>
</td>
</tr>
</table>
```

### 2. 转折类（Pivot）— 黄色边

```markdown
<table>
<tr>
<td width="60" valign="top"><img src="../assets/avatars/05-strategist.png" width="48"/></td>
<td>
<strong style="color:#D4A03B">🔄 [转折]</strong><br/>
<strong>「我原本判断 ROI 优先级最高，但红队提到的政策不可控因素让我把『是否可推迟 6 个月』调到了同等优先级。」</strong><br/>
<small>— 战略派 · R3</small>
</td>
</tr>
</table>
```

### 3. 盲区类（Blind Spot）— 紫色边

```markdown
<table>
<tr>
<td width="60" valign="top"><img src="../assets/avatars/02-user-empathy.png" width="48"/></td>
<td>
<strong style="color:#5B3F8C">💡 [盲区]</strong><br/>
<strong>「大家都在算研发成本，但没人算用户侧的迁移成本——这个项目对老用户是免费升级还是被迫迁移，决定了 3 个月留存差 20% 还是 50%。」</strong><br/>
<small>— 用户派 · R1</small>
</td>
</tr>
</table>
```

### 4. 凝练类（Crystallization）— 绿色边

```markdown
<table>
<tr>
<td width="60" valign="top"><img src="../assets/avatars/06-investor.png" width="48"/></td>
<td>
<strong style="color:#2E6E5C">💎 [凝练]</strong><br/>
<strong>「这是一个 70% 概率赚 1 倍 / 30% 概率亏 50% 的赌注，仓位决定它对你是机会还是陷阱。」</strong><br/>
<small>— 投资人 · R3</small>
</td>
</tr>
</table>
```

---

## 4 类标识符号（与文本 fallback 对齐）

| 类型 | 符号 | 颜色 | 含义 |
|------|------|------|------|
| 碰撞 Collision | ⚔️ | #C04848 红 | 直接冲突的锐化句 |
| 转折 Pivot | 🔄 | #D4A03B 黄 | 立场移动的触发句 |
| 盲区 Blind Spot | 💡 | #5B3F8C 紫 | 揭示新维度的句 |
| 凝练 Crystallization | 💎 | #2E6E5C 绿 | 最少字数核心张力 |

---

## 整区布局（金句精选区在 verdict 卡内位置）

```markdown
## 金句精选区（共 X 条）

[卡片 1：碰撞类]

[卡片 2：盲区类]

[卡片 3：转折类]

[卡片 4：凝练类]

> 所有金句由主持人按 4 客观标准提取（详见 `assets/mechanisms/highlight-extraction.md`）。无符合标准时本场不输出金句区。
```

---

## 降级渲染

### Markdown 不渲染 HTML 表格时的 fallback

```markdown
> ⚔️ **[碰撞]** 📊 **数据派 · R2**
>
> 「执行派算的 8 周是顺风版本，但用户派的访谈数据显示需求理解还要 3 周，真实交付不会早于 11 周。」
```

### 完全纯文本时的 fallback

```
[碰撞] 数据派 · R2
"执行派算的 8 周是顺风版本，但用户派的访谈数据显示需求理解还要 3 周，真实交付不会早于 11 周。"
```

---

## 反剧场化校核

- [ ] 金句是否都从原文截取（非主持人加工/润色）？
- [ ] 每条都通过 4 标准 + 一票否决（有具体论据非纯修辞）？
- [ ] 总数控制在 3-7 条（少则不输出本区，多则裁剪）？
- [ ] 卡片视觉强化但**未改变内容**？

任一项违反 → 视为 v0.2 反剧场化硬约束失败。

---

## 共识矩阵的紧凑头像版（可选增强）

把"支持角色 / 反对角色"列从角色名列表换成头像列表：

```markdown
| # | 论点 | 支持 | 反对 | 加权置信度 |
|---|------|------|------|-----------|
| 1 | xxx | <img src="../assets/avatars/01-data-driven.png" width="20"/><img src="../assets/avatars/04-executor.png" width="20"/><img src="../assets/avatars/06-investor.png" width="20"/> | <img src="../assets/avatars/03-devils-advocate.png" width="20"/> | 65% |
```

适用：角色 ≥ 5 时，头像列表比文字更易扫描。
不适用：终端用户使用纯文本环境时——必须保留文本 fallback 列。
