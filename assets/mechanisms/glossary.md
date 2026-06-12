# 高频混淆术语词典（Glossary）· v0.3.0

> **核心原则**：术语精度是论证有效性的前提。错用术语 = 论证一开始就在错误的概念上滑行。
>
> 这是 v0.2.1 dry-run 复盘后的硬约束——之前我用"裸辞"指代"接 offer 后离职"，污染了整份决策。本词典是主持人的自动勘误规则。

---

## 1. 词典结构

```yaml
- term: <错用词>
  correct: <正确词>
  rule: <如何区分>
  domain: <出现场景>
```

主持人在 R1/R2/R3 每条发言后扫一遍，命中错用 → 自动改写并在 `verdict.warnings[]` 中记录"术语勘误：'X' → 'Y'，理由：...".

---

## 2. 职业 / 跳槽场景

| 错用 | 正确 | 区分规则 |
|------|------|---------|
| **裸辞** | 主动离职 / 待业离职 | 裸辞 = **没找到下家就先辞**；接 offer 后离职属于正常跳槽，**禁止用裸辞**指代 |
| **期权** | 期权（option） / 限制性股票（RSU）/ 限制性股票单位（PSU）| 三者税务/风险/价值差异巨大；用户说"期权"时主持人必须问清楚是哪种 |
| **cliff（悬崖期）** | cliff（首次归属期）| cliff 1 年 = 入职满 1 年才开始解锁，**不是**满 1 年才能买；要区分 vesting cliff vs exercise window |
| **vesting** | 归属（解锁日历）| 与 cliff 不同：cliff 是首次解锁门槛，vesting 是后续解锁节奏 |
| **scope** | 职责范围（团队规模 + 汇报对象 + 负责模块 + 决策权重）| 不能简化为"做什么"；必须含 4 元素 |
| **base** / **薪资** | base salary / 总包（TC = base + bonus + equity 年化）| 早期创业公司给的"50w 包"通常是 TC，base 可能仅 30w；不区分会严重误判 |
| **股权稀释** | 后续融资稀释 | 用户提供的"5%股权"在 A/B/C/D 轮后可能变 1.5%；vesting 期间稀释由公司而非员工承担 |
| **窗口期** | 行权窗口 (exercise window) / 赛道窗口 / 离职后行权期 (post-termination exercise window, PTEW) | 三种"窗口"经常被混用——发言中出现"窗口期"必须自标注是哪一种 |
| **try lead** | 临时管理人（无 title 提升）| 不等于晋升 manager，且常无加薪 |

---

## 3. PRD / 产品场景

| 错用 | 正确 | 区分规则 |
|------|------|---------|
| **MVP** | Minimum Viable Product / Minimum Lovable Product (MLP) | MVP 是验证假设最小集；MLP 是"用户愿意每天用的最小版本"——别混 |
| **PMF** | Product-Market Fit | 不是用户增长率高 = PMF；标准是有机留存 + 用户主动推荐 + 付费意愿 |
| **北极星指标** | North Star Metric (NSM) | 单一最高优先级指标；不能说"我们有 3 个北极星"——那叫 KPI 组合 |
| **funnel** | 漏斗（user journey 中的转化路径）| 不等于"流程图"——funnel 必须有量化转化率 |
| **Aha moment** | 用户首次感知核心价值的瞬间 | 不是"留存提升点"——是用户主观体验拐点 |

---

## 4. 财务 / 投资场景

| 错用 | 正确 | 区分规则 |
|------|------|---------|
| **ROI** | Return on Investment | 必须给出**时间框**（年化 / 总期 / 月化）+ 风险调整后还是名义 |
| **预期收益** | Expected Value (EV) | EV = Σ(概率 × 收益) - 成本；不带概率分布的"预期收益"是空话 |
| **回本周期** | Payback period（不考虑时间价值）vs Discounted payback（考虑）| 创业 / 投资场景必须区分 |
| **估值** | 投后估值 (post-money) / 投前估值 (pre-money) | 早期 SAFE / 可转债场景下"估值"含义模糊，必须明示 |
| **沉没成本** | sunk cost | 不能作为"是否继续"的论据（决策只看 forward-looking incremental cost/benefit）|
| **机会成本** | opportunity cost | 选 A 必须算"放弃 B 的最优结果"——否则是单选项决策不是 trade-off |

---

## 5. 决策 / 概率场景

| 错用 | 正确 | 区分规则 |
|------|------|---------|
| **概率高** | "我估计 70%" / "base rate 30%" / "条件概率 P(A\|B) = X" | "概率高/低"未量化无法证伪——主持人自动追问"具体百分比" |
| **风险** | 概率分布 × 损失幅度 / Knightian 不确定性（无概率可估）| 两类风险处理方式完全不同 |
| **黑天鹅** | 极端低概率高影响事件（Taleb 定义）| 不是"我没想到的事"——必须满足"事后可解释 + 事前不可预测"|
| **第一性原理** | 从公理 / 不可约简事实推导（Aristotle / Musk）| 不是"问 5 个为什么"——那是 Toyota 5-why；区分概念边界 |
| **base rate** | 同类事件的历史发生比例 | 必须给数据源；"我感觉成功率 30%" ≠ base rate |

---

## 6. 自动勘误流程

```
def auto_correct(utterance):
    for entry in glossary:
        if entry.term appears in utterance:
            if used_in_correct_context(utterance, entry.rule):
                continue
            else:
                rewrite utterance with entry.correct
                log to verdict.warnings[]: "术语勘误：'{term}' → '{correct}'，理由：{rule}"
    return utterance
```

**主持人裁决卡底部专门一节**：

```markdown
## 术语勘误日志

| # | 原文 | 勘误为 | 理由 |
|---|------|-------|------|
| 1 | "裸辞过去" | "接 offer 后主动离职" | 裸辞 = 未找下家先辞，接 offer 后离职不属于裸辞 |
| 2 | "期权 5%" | "期权 [待补充] 股 / strike $X / 当前估值 $Y" | 单说百分比无法计算 EV |
```

如果勘误数 ≥ 3，裁决卡顶部加 ⚠️ "本辩论存在术语精度问题，请仔细核对结论中的关键概念"

---

## 7. 词典扩展规则

每次跑 skill 时若发现**新错用术语**：

1. 主持人在 verdict.warnings 中记录
2. 用户可命令 `--add-glossary "term=X, correct=Y, rule=Z"` 追加到本文件
3. v0.x 升级时主持人将累计的高频错用合入正式词典

---

## 8. 自检 3 问（每次裁决前）

- [ ] 全部发言已过自动勘误扫查？
- [ ] 勘误日志已纳入裁决卡底部？
- [ ] 勘误数 ≥ 3 时是否已挂顶部警告？

**任一项违反 → 视为 v0.3.0 术语精度硬约束失败。**
