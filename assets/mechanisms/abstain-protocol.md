# 履职门禁与 Abstain 协议（Abstain Protocol）· v0.3.0

> **核心原则**：角色在缺关键输入时**必须 abstain**，不允许用通用知识填补缺口。主持人收到 abstain 计数 ≥ 2 立即中止辩论，返还用户索数据。
>
> 这是 v0.2.1 dry-run 复盘后的硬约束——之前角色 R1 在没拿到 scope/薪资/期权 vesting 等关键输入时就直接进入"窗口期 12-18 月""3 个月学习曲线"等二阶论述，跳过了专家应当先问的输入数据。

---

## 1. 输入门禁（Input Gate）

每个场景预设的 `输入预处理` 段从 v0.2.0 的"建议提供"升级为 **v0.3.0 的强制门禁**。

### 启动检查
主持人在 R1 启动前执行：

```
def gate_check(scenario, user_input):
    required = scenario.required_inputs   # 场景文件硬约束清单
    missing = [f for f in required if not user_input.has(f)]
    if len(missing) > 0:
        return REJECT(missing_fields=missing, ask_user=True)
    return PROCEED
```

**不通过门禁** → 主持人输出标准索数据模板（见第 5 节），**不启动辩论**。

---

## 2. 各场景的 required_inputs

| 场景 | 必填字段（缺一即拒启动）|
|------|----------------------|
| **career-jobchange** | 现职 base/bonus 包 / 新 offer base/bonus/sign-on / **期权数量+strike+预估估值+vesting+cliff** / scope（团队规模 + 汇报对象 + 负责模块）/ 决策窗口 / 当下生命阶段（房贷/家庭/可承担风险时长）|
| **prd-review** | PRD 文档 / 目标用户画像 / 业务指标 / 资源约束（人/钱/时间）|
| **project-go-no-go** | 立项书 / 预算 / 团队配置 / 不可逆点（哪些决策做完反悔代价大）|
| **technical-choice** | 技术选项至少 2 个 / 性能/成本/团队熟悉度数据 / 长期维护成本估计 |
| **financial-decision** | 投资标的 / 本金占比 / 时间框 / 替代方案对照 |
| **ethical-dilemma** | 涉事各方 / 已造成/未造成的事实损害 / 法律边界 |
| **health-lifestyle** | 当前生理指标 / 医生意见（若有）/ 干预选项 / 时长承诺 |
| **interpersonal** | 关系性质 / 已发生事件时间线 / 双方诉求 |
| **option-tradeoff** | 选项至少 2 个 / 每个选项的 5 维属性（成本/收益/风险/时间/不可逆性）|
| **cross-doc-audit** | 待审文档 / 参照标准（KPI / 模板 / 历史版本）|
| **generic** 兜底 | 议题 / 决策窗口 / 不可逆程度 / 已知约束 |

---

## 3. 角色级 Abstain 触发条件

每个角色在 R1 收到议题 + 输入数据后，**先做履职体检**：

```
def role_self_check(role, scenario_input):
    role_required = role.required_data_for_speaking   # 角色卡新增字段
    missing = [f for f in role_required if not scenario_input.has(f)]
    if len(missing) > 0:
        return ABSTAIN(missing_fields=missing)
    return PROCEED
```

### role-pool 各角色卡 frontmatter 新增

```yaml
required_data_for_speaking:
  - <字段名 1>
  - <字段名 2>
abstain_threshold: any | majority | all
```

**示例（投资人）**：

```yaml
required_data_for_speaking:
  - 期权数量+strike price
  - 预估公司当前估值
  - vesting schedule（cliff + 总年限）
  - 替代投资机会成本（如：留下来的 base + bonus）
abstain_threshold: any   # 任一缺失即 abstain
```

**示例（Bayesian）**：

```yaml
required_data_for_speaking:
  - base rate 数据源（同类决策成功/失败比例）
  - 用户当前先验（信念强度）
abstain_threshold: any
```

**示例（用户派 / 在 PRD 场景）**：

```yaml
required_data_for_speaking:
  - 目标用户画像（至少 1 个 persona）
  - 用户使用场景描述（至少 1 个）
abstain_threshold: majority   # 大多数缺失才 abstain
```

---

## 4. Abstain 发言模板（角色 R1 强制使用）

```markdown
**[角色名] · R1 · ABSTAIN**

我无法在缺少以下关键输入的情况下论证：

1. <字段 1>：[为什么我需要它——一句话]
2. <字段 2>：[为什么我需要它——一句话]
3. <字段 3>：[为什么我需要它——一句话]

如果强行论证，我将不得不依赖通用经验或编造数据——这违反 v0.3.0 引证策略。

**请用户先补齐上述输入，或主持人裁决放弃我的角色席位。**

[signal: N/A · abstain]
```

**违反此模板**（即角色没拿到数据还在 R1 输出实质论证）→ 主持人在裁决卡的 `verdict.warnings[]` 中标记 "履职跳过"，该角色发言**整体不计入**加权置信度。

---

## 5. 主持人中止流程

```
abstain_count = sum(1 for role in roles if role.r1_state == ABSTAIN)

if abstain_count >= 2:
    EMIT_HALT_REPORT(missing_fields_union)
    pause_debate()
    request_user_input()
elif abstain_count == 1:
    proceed_with_warning(in verdict.warnings[])
elif abstain_count == 0:
    proceed_normal()
```

### 标准索数据模板（主持人输出）

```markdown
## ⏸ 辩论暂停 · 等待用户补齐输入

[N] 个角色已声明 abstain，原因是缺少关键决策依据。继续辩论将引发履职跳过 / 编造数据。

**请补齐以下数据：**

| # | 字段 | 缺失角色 | 为什么需要 |
|---|------|---------|----------|
| 1 | 期权数量+strike price | 投资人 / Bayesian | 计算 EV 与 base rate 后验 |
| 2 | 团队 scope（汇报对象+负责模块）| Steelman | 构造"留下"vs"走"最强版本 |
| 3 | ... | ... | ... |

补齐后请回复"已补充：<字段>=<值>"，主持人将自动重启 R1。

**为什么严格**：v0.2.1 dry-run 显示，跳过这些数据直接进辩论 →
角色为了发言不沉默，会编造"a16z 报告""Carta 数据"等假精度引证 →
看起来专业但实际是剧场化。本协议是 v0.3 的硬约束之一。
```

---

## 6. 例外条款

仅以下三种情况允许在缺数据时进入 R1：

1. **议题本身就是"我该不该收集 X 数据"** —— 这种 meta-决策不需要先有数据
2. **第一性原理派 / 战略派的纯逻辑推演** —— frontmatter 标 `citation_obligation: exempt` 的角色可在缺数据时输出**纯定性论述**（但仍不能编数字）
3. **用户明确签字接受 hypothesis-only 模式** —— 用户输入 `--mode hypothesis-only` 时主持人允许全员推演但裁决卡顶部强制挂 `⚠️ 本辩论基于假设而非真实数据，结论不可作为决策依据`

---

## 7. 自检 4 问（每次启动辩论前）

- [ ] 已对照场景的 `required_inputs` 跑过 input gate？
- [ ] 缺失字段是否已在索数据模板中显式列出？
- [ ] 各角色 frontmatter 的 `required_data_for_speaking` 已配置完整？
- [ ] 进入 R1 后是否检查每个角色的 abstain 状态并合计 `abstain_count`？

**任一项违反 → 视为 v0.3.0 履职门禁失败，主持人必须撤回当前裁决。**
