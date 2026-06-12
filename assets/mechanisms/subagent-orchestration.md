# Subagent 编排协议（Subagent Orchestration）· v0.3.0 新增

> **核心原则**：v0.3.0 引入 **真 subagent 模式**——R1 独立陈述阶段使用 Qoder Task 工具并发 spawn 5 个独立 context 的 subagent，物理隔离 Identity Bias 与 Sycophancy。
>
> 本协议解释架构差异、何时使用、何时回退、并发参数与失败处理。

---

## 1. 架构对比

### v0.2.x 单 context 模式（保留为 standard mode）

```
主 LLM 单 context
┌──────────────────────────┐
│ SKILL.md                 │
│ 全部 5-7 张角色卡         │
│ R1: 数据派 prompt + 输出  │
│ R1: 用户派 prompt + 输出  │  ← 同一 LLM 顺序生成
│ R1: 怀疑派 prompt + 输出  │  ← 看得见兄弟角色卡，靠 prompt
│ R1: 投资人 prompt + 输出  │     约束"假装看不到他人意见"
│ R1: Steelman prompt + 输出│
└──────────────────────────┘

特点：
✅ 实现简单，0 工具依赖
✅ R1→R2→R3 流转无需 IPC
❌ Identity Bias / Sycophancy 在 prompt 层无法物理消除
❌ "盲发言"是表演性的（LLM 实际看得到所有角色卡）
```

### v0.3.0 独立 subagent 模式（新增 independent mode）

```
主 agent (主持人)
  │
  ├─[Task spawn, parallel]──→ Subagent A (数据派)
  │                            ├─ 独立 context window
  │                            ├─ 只见：议题 + 自己角色卡 + 输入数据
  │                            └─ 不见：B/C/D/E 的角色卡 + R1 草稿
  │
  ├─[Task spawn, parallel]──→ Subagent B (用户派)  [同上]
  ├─[Task spawn, parallel]──→ Subagent C (怀疑派)  [同上]
  ├─[Task spawn, parallel]──→ Subagent D (投资人)  [同上]
  └─[Task spawn, parallel]──→ Subagent E (Steelman) [同上]

  收集 5 份独立 R1 →
  主持人在主 context 中合并 → R2 交叉质询（单 context，因为需要看到全部 R1）
                          → R3 红队 + 裁决（单 context）

特点：
✅ 物理隔离 = 真盲评，从根本上消除 Identity Bias 第一轮污染
✅ Sycophancy 在 R1 完全不存在（subagent A 看不到 B 在说什么）
✅ 利用 Qoder Task 并发能力（最多 10 并发，5-7 角色绰绰有余）
⚠️ 工具依赖 Qoder Task 工具（脱离 Qoder 环境无法运行）
⚠️ R2/R3 仍单 context（subagent 不能再 spawn subagent，1 层嵌套限制）
```

---

## 2. 引用依据

Claude Code 官方文档 (`code.claude.com/docs/en/sub-agents`) 验证：

> "Subagents use the Task tool engine for parallel execution. They offer **Context isolation: Each task gets its own context window.** Up to **10 tasks run concurrently**."
>
> "Subagents cannot spawn other subagents. If your workflow requires nested delegation, use Skills or chain subagents from the main conversation."

Qoder 的 Task 工具继承同等能力。

`[source: code.claude.com/docs/en/sub-agents, retrieved 2026-06-10]`

---

## 3. Mode 选择策略

| Mode | 架构 | 适用场景 | 工具要求 |
|------|------|---------|---------|
| `fast` | 单 context · 3 角色 · 1 轮 + 极简红队 | 已知项 / 低不可逆性 / 5 分钟内决策 | 无 |
| `standard` | 单 context · 5 角色 · 3 轮 + 红队 | 通用决策 / 中等不可逆性 | 无 |
| `deep` | 单 context · 7 角色 · 3 轮 + 强化红队 | 高复杂度 / 高不可逆性 | 无 |
| **`independent`**（v0.3.0 新增）| **R1 真 subagent 并发**，R2/R3 单 context | **Identity Bias 高风险场景**：身份/政治/价值观决策 / 用户特别在意盲评质量 | **Qoder Task 工具** |

### 触发条件（自动判定）

主持人启动前检查：

```
def select_mode(scenario, user_input, env):
    if user_input.has_explicit_mode:
        return user_input.mode
    if scenario in ["ethical-dilemma", "interpersonal", "career-jobchange"]:
        # Identity Bias 高敏感场景
        if env.has_task_tool:
            return "independent"
        else:
            return "standard"   # fallback
    elif scenario in ["prd-review", "technical-choice", "option-tradeoff"]:
        return "standard"
    elif scenario in ["cross-doc-audit", "generic"] and low_irreversibility:
        return "fast"
    else:
        return "standard"
```

---

## 4. Subagent 调用协议（independent mode）

### 4.1 主持人的角色

```
1. 通过 input gate 校验（abstain-protocol.md §1）
2. 为每个角色构造独立的 Task 调用 prompt（见 §4.2）
3. 并发发起 N 个 Task 调用（N = 5-7，不超过 10）
4. 等待全部 subagent 返回 R1 结果
5. 收集到主 context，进入 R2 交叉质询
```

### 4.2 单个 subagent 的 prompt 模板

```markdown
你是一个独立的决策角色，被召集到一场私人董事会中。

# 你的身份
[完整粘贴该角色 role-pool 卡的内容]

# 议题
[用户议题原文]

# 输入数据
[全部用户提供的输入数据]

# 履职体检（先做这一步）
检查你的 role frontmatter 中 required_data_for_speaking 字段。
如果缺关键输入 → 严格按 abstain-protocol.md §4 模板返回 ABSTAIN 发言。
否则 → 进入实质论述。

# 输出约束
- 单条发言 ≤ 300 字
- 每个数字必须按 citation-policy.md §1 标注三态之一
- 立场值必须给出 (-1.0 ~ +1.0)
- 反对点必带 (R2/R3 阶段强制)
- [signal: 1-5] 自评

# 隔离声明
你**看不到**其他角色的角色卡和发言——这是设计如此。
你的 R1 必须基于自己的 reasoning lineage 独立产生。
请不要试图想象或假设其他角色会怎么说。

# 返回格式
严格 JSON：
{
  "role_id": "<id>",
  "round": "R1",
  "stance": <-1.0..+1.0>,
  "speech": "<发言文本>",
  "warnings": ["<勘误项>", ...],
  "abstain": false | true,
  "missing_inputs": [<字段>...] (仅 abstain=true 时填)
}
```

### 4.3 并发参数

| 参数 | 值 | 理由 |
|------|---|------|
| `concurrent_max` | 7 | 角色池上限 7（standard）/ 10（deep 含红队），不超 Task 10 并发上限 |
| `timeout_per_subagent` | 90 秒 | 单 subagent R1 输出 ≤300 字，Sonnet 90 秒充足 |
| `retry_on_failure` | 1 次 | 失败再试 1 次；2 次失败 → 主持人记录 `warnings[]` 并继续 |
| `model_per_subagent` | 默认继承 main / 可在场景配置覆盖 | deep mode 关键角色可指定 opus，其他 haiku 节省成本 |

### 4.4 失败处理

```
for subagent_result in subagent_results:
    if subagent_result.status == "timeout":
        log_warning("subagent {role} timed out, fallback to single-context generation")
        regenerate_in_main_context(role)
    elif subagent_result.status == "abstain":
        increment(abstain_count)
    elif subagent_result.status == "ok":
        collect(subagent_result)

if abstain_count >= 2:
    halt_and_request_inputs()    # abstain-protocol §5
```

---

## 5. R2/R3 为何仍单 context

学术依据 + 工程依据双重决定：

**学术**：R2 交叉质询的核心机制是"看到 R1 全部立场后构造反对点"——subagent 物理隔离反而**阻碍**了交叉，必须合并到主 context。

**工程**：Claude Code 文档明示 "Subagents cannot spawn other subagents"——R2 如果要用 subagent，必须由主 agent 重新 spawn，但此时主 agent 已经持有 R1 全部内容，再 spawn 已经无意义（信息已经穿透）。

**结论**：v0.3.0 的真隔离仅在 R1 第一轮独立陈述生效——这正是 Identity Bias / Sycophancy **首要发病点**。R2/R3 用其他机制（魔鬼代言人 + 红队 + 立场量化）控制污染。

---

## 6. independent mode 的成本评估

| 项 | standard | independent | 增量 |
|---|---------|-------------|------|
| R1 token 总量 | ~3000 | ~3000 × 5 (independent context) | +12000 |
| R1 wall time | ~30s 顺序 | ~10s 并发 | -20s |
| API 调用次数 | 1 | 5 (R1) + 1 (R2) + 1 (R3) = 7 | +6 |
| 总成本（Sonnet）| ~$0.04 | ~$0.20 | +$0.16 |

**何时值得**：
- ✅ 高不可逆决策（跳槽 / 婚姻 / 上百万投资 / 创业）
- ✅ 用户明确说"不要让 agent 互相影响"
- ✅ ethical-dilemma / interpersonal 等身份敏感场景
- ❌ 普通 PRD 评审 / 技术选型——standard 足够

---

## 7. 渐进升级路径

| 阶段 | 状态 | 何时启用 |
|------|------|---------|
| **当前 v0.3.0**：independent mode 作为 opt-in，标准默认仍 standard | 落地 | now |
| v0.3.x：测量 independent vs standard 在 5 个真实案例的差异，校准触发条件 | 待测试 | 2-4 周内 |
| v0.4：根据测试结果决定是否将 independent 设为高敏场景默认 | 计划 | 测试后 |

---

## 8. 自检 5 问（启动 independent mode 前）

- [ ] Qoder Task 工具是否可用？不可用必须 fallback standard
- [ ] 输入门禁是否已通过？
- [ ] 每个角色的 prompt 是否仅含**自己**的角色卡（不含兄弟角色卡）？
- [ ] subagent 返回格式是否严格 JSON 可解析？
- [ ] timeout / retry / abstain_count 处理逻辑是否就位？

**任一项违反 → 视为 v0.3.0 编排协议硬约束失败，回退 standard mode 并在裁决卡注明。**
