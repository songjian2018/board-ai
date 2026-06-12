# 引证策略（Citation Policy）· v0.3.0

> **核心原则**：每个带数字的论点必须可定位到外部可验证来源；无法定位的数字必须明示"待验证"，**不计入**加权置信度。
>
> 这是 v0.2.1 dry-run 复盘后的硬约束——之前的"a16z 报告""Carta 43% 期权归零""Glassdoor 22%"全是编造数字带"权威修饰词"，绕过了反水词检测。本策略堵这个口子。

---

## 1. 论点的三种状态

| 状态 | 标记 | 是否计入加权置信度 | 视觉处理 |
|------|------|------------------|---------|
| **已验证**（cited & verifiable）| `[source: ...]` 含可定位信息 | ✅ 全权重 | 默认 |
| **未验证**（unverified claim）| `[待验证：建议查 X]` | ❌ **不计入**，仅作为 hypothesis | 灰色斜体 |
| **常识/经验**（lived knowledge）| `[experience: ...]` | ⚠️ 0.5 权重 | 浅黄底色 |

**强制规则**：发言中出现的**所有数字**（百分比 / 倍数 / 金额 / 时长 / 计数）必须落入这三种状态之一。无标注数字 = 主持人自动改写为 `[待验证]` 并降权。

---

## 2. 可定位信息的 5 种合法形式

发言中的 `[source: ...]` 必须满足以下**至少一种**：

| # | 形式 | 示例 |
|---|------|------|
| A | 公开 URL | `[source: https://carta.com/blog/state-of-startups-2024/]` |
| B | DOI / arxiv ID | `[source: arxiv:2509.05396]` |
| C | 报告标题 + 年份 + 页码 | `[source: McKinsey "State of AI 2025", p.42]` |
| D | 数据集名 + 查询条件 | `[source: BLS QCEW 2024 Q4, NAICS 5415]` |
| E | 自有数据集 + 来源描述 | `[source: 用户提供的 X 公司 ESOP plan PDF, 第 3 页 vesting schedule]` |

**不合法形式**（一律降级为 `[待验证]`）：
- ❌ `[source: a16z 报告]`（无标题/年份/链接）
- ❌ `[source: Carta 数据]`（无具体数据集名 + 查询条件）
- ❌ `[source: Glassdoor 跨厂均值]`（无可查询路径）
- ❌ `[source: 行业普遍认为]`（无主体）

---

## 3. 主持人的引证扫查算法

裁决前，主持人对全部发言执行：

```
for each utterance in [R1, R2, R3]:
    for each number_token in utterance:
        if has_source_marker:
            verify_source_format()
            if not in 5_legal_forms:
                downgrade to [待验证]
                log to verdict.warnings[]
        else:
            auto_rewrite as [待验证]
            log to verdict.warnings[]
```

**再算两个指标**：

```
claim_with_citation_ratio = 带 [source/待验证/experience] 标注的数字数 / 全部数字数
verifiable_citation_ratio = 通过 5 法则验证的 [source] 数 / 全部数字数
```

| 指标 | 阈值 | 视觉警示 |
|------|------|---------|
| `claim_with_citation_ratio` | < 90% | 内联 ⚠️ 标记每条无标注数字 |
| **`verifiable_citation_ratio`** | **< 60%** | **裁决卡顶部红警告条："本辩论引证有效性不足，结论仅作 hypothesis 处理"** |
| `verifiable_citation_ratio` | 60-79% | 黄色边框告警 |
| `verifiable_citation_ratio` | ≥ 80% | 通过 |

---

## 4. 角色卡的引证义务（写入每张 role-pool 卡的 frontmatter）

每个角色 frontmatter 新增字段：

```yaml
citation_obligation: strict   # strict | moderate | exempt
```

- `strict`（数据派 / Bayesian / 投资人 / 红队）：每条带数字论点**必须**带 `[source]`，否则角色自动 self-flag `[待验证]`
- `moderate`（用户派 / 怀疑派 / Steelman）：可用 `[experience]` 标注主观观察，但不能用 `[source]` 包装无源数字
- `exempt`（执行派 / 战略派 / 第一性原理派）：处理逻辑推理时无需引证，但**所有具体数字仍受 strict 规则约束**

---

## 5. 用户提供数据的引证

用户在输入预处理阶段提供的数据（参见 `abstain-protocol.md`）享有特殊地位：

```yaml
[source: 用户输入·<字段名>]
```

例如：用户填写"现职 base 60万 / X 公司 offer base 80万"——
- 可用 `[source: 用户输入·薪资对照]`
- **不需要外部验证**——但裁决卡需在底部声明"以下结论基于用户自陈数据，未做独立核实"

---

## 6. 反例参考（v0.2.1 dry-run 真实失败案例）

| 原文（v0.2.1 dry-run）| 处理（v0.3）|
|---------------------|------------|
| "Carta 2024 早期创业 base rate 43% 期权最终归零" | → `[待验证：建议查 Carta State of Private Markets / Wealthfront 2024 期权流失数据]` 不计入加权 |
| "Glassdoor 跨厂均值 22% 试用期淘汰率" | → `[待验证]`，Glassdoor 不公开此聚合数据 |
| "MAI 1 年估值 5x" | → 改写为 `[待验证：建议查 PitchBook MAI Inc 融资轮次数据]` 或直接删除 |
| "a16z 报告 2026 vertical AI agent 加速" | → `[experience: 行业讨论度提升]` 0.5 权重；不能用 `[source]` |

---

## 7. 自检 5 问（每次裁决前）

- [ ] 全部数字是否落入"已验证 / 待验证 / 经验"三态之一？
- [ ] `[source]` 标注是否符合 5 种合法形式之一？
- [ ] 是否有"权威修饰词 + 无源数字"的伪科学化表达？
- [ ] `verifiable_citation_ratio` 已计算并显示在裁决卡？
- [ ] 用户自陈数据是否标注了 `[source: 用户输入·X]` + 底部免责声明？

**任一项违反 → 视为 v0.3.0 引证策略硬约束失败，裁决卡自动降级为 hypothesis 报告。**
