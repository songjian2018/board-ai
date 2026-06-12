# EVOLUTION — Skill 自我进化协议（v0.1）

> 本协议定义 multi-perspective-debate 如何**积累经验、产出改进候选、由用户拍板采纳**。
> 设计原则：自动产出**候选**，人工拍板**采纳**——绝不让 skill 直接改自己。

---

## 0. 设计哲学

**为什么不全自动**：
- LLM 改自己的 prompt 容易越改越花哨（reward hacking）
- 改坏了用户没感知，污染会滚雪球
- 没有 ground truth，自动评分器自己也是 LLM，循环自欺
- 真正有价值的改进往往来自"用户拍桌骂"那一两次

**为什么不全人工**：
- 用户记不住每次哪里不对劲
- 同样的失败模式不归档就会反复重蹈

**结论：半自动收集 + 人工审核**。

---

## 1. 目录结构

```
multi-perspective-debate/evolution/
├── EVOLUTION.md              # 本文件，协议本体
├── changelog.md              # 已采纳的演进记录
├── runs/                     # 每次调用的归档
│   └── YYYY-MM-DD-{slug}.json
├── feedback/                 # 用户反馈（主动+被动）
│   └── YYYY-MM-DD-{slug}.md
├── candidates/               # 待审核的演进提案
│   └── PR-NNN-{title}.md
└── stable-tag.txt            # 当前稳定版指针，回滚用
```

---

## 2. 触发时机（什么时候记什么）

### 2.1 自动触发（每次 skill 调用时）

调用结束时强制写入 `runs/YYYY-MM-DD-{slug}.json`：

```json
{
  "run_id": "2026-06-12-jobchange-001",
  "timestamp": "2026-06-12T14:32:11+08:00",
  "skill_version": "0.4.0",
  "input": {
    "topic": "该不该跳槽到 X 公司",
    "mode": "standard",
    "scenario": "career-jobchange"
  },
  "execution": {
    "duration_sec": 287,
    "rounds_run": 3,
    "speeches_count": 16,
    "abstain_count": 0,
    "mind_changes": 2,
    "final_confidence": 0.68,
    "verifiable_citation_ratio": 0.81
  },
  "tool_usage": {
    "task_concurrent": false,
    "fallback_to_standard": true,
    "research_pipeline_called": false
  },
  "warnings_triggered": ["citation_ratio_low"],
  "output_hash": "sha256:..."
}
```

**自动写入不打扰用户**——是基础设施，类似 access log。

### 2.2 半自动触发（用户主动反馈）

用户使用过程中说出以下**信号词**触发收集 feedback：
- "这次不太对" / "这个判断有问题" / "差点意思"
- "好用" / "这个有意思" / "学到了"
- "下次能不能 X" / "希望增加 Y"
- "辩论太啰嗦" / "缺少 Z 角色"

skill 检测到信号 → 主动开一个 `feedback/YYYY-MM-DD-{slug}.md`：

```markdown
# 用户反馈 — 2026-06-12 跳槽议题

**关联 run**：2026-06-12-jobchange-001
**用户原话**："执行派的判断太理想化了，没考虑公司实际审批流程"
**情绪倾向**：负面
**指向问题**：角色卡 04-executor 缺少"组织流程现实"维度

**用户期望**：[用户进一步说明]

**自动归类**：
- 类型：角色行为偏差
- 影响范围：04-executor 角色卡
- 严重度：中

**是否触发候选**：是 → 已生成 PR-007
```

### 2.3 定期触发（按月复盘）

每月初自动跑一个分析任务：
- 扫描上月所有 runs/ 和 feedback/
- 找出**重复出现的失败模式**（≥ 3 次）
- 找出**表现最好的 run**（用户给好评的）
- 产出 `candidates/PR-monthly-YYYY-MM.md` 提交月度复盘建议

---

## 3. 演进提案格式（候选 PR）

每个 `candidates/PR-NNN-*.md` 必须包含：

```markdown
# PR-007: 04-executor 角色卡补"组织流程现实"维度

**提案日期**：2026-06-12
**触发来源**：feedback/2026-06-12-jobchange.md
**类型**：角色卡修订 / 机制调整 / PITFALLS 新增 / 场景预设修订 / 术语词典扩展
**预估影响**：低 / 中 / 高
**是否需要回归测试**：是

## 当前问题

[具体复述当前 skill 在什么场景下表现不佳，引用 run 数据]

## 建议改动

### Diff

文件：`assets/role-pool/04-executor.md`

```diff
- 思维方式：实操落地
+ 思维方式：实操落地（含组织流程现实约束）
+
+ 强制提示：判断"能否执行"时必须考虑：
+ - 审批层级
+ - 跨部门协调成本
+ - 资源争夺
```

## 风险

[这次改动可能带来什么副作用]

## 测试计划

- 用 tests/dry-run-cases.md 中 case-3（组织协调类决策）回归测试
- 对比改前后输出差异

## 用户拍板

- [ ] 采纳
- [ ] 拒绝
- [ ] 改后采纳（用户写出修改意见）
```

---

## 4. 采纳流程（人工拍板）

用户审核 PR 后操作：

### 采纳流程

1. 用户在 PR 文件勾选"采纳"
2. skill 自动：
   - 备份当前文件到 `evolution/backups/v{当前版}-{文件名}-{日期}`
   - 应用 diff
   - 跑 `tests/dry-run-cases.md` 回归测试
   - 测试通过 → 写入 `changelog.md` + 更新 `stable-tag.txt`
   - 测试失败 → 自动回滚 + 通知用户失败原因
3. PR 文件移动到 `candidates/applied/`

### 拒绝流程

1. 用户在 PR 文件写明拒绝理由
2. PR 文件移动到 `candidates/rejected/`
3. 拒绝理由进入"反 PITFALLS"知识——下次类似提案直接 skip

---

## 5. 改动类型限制

不是所有 skill 内容都能演进。按风险分级：

| 改动类型 | 允许自动产出候选？ | 备注 |
|---------|-----------------|------|
| 新增 PITFALLS 条目 | ✅ | 低风险，最常见 |
| 扩展术语词典 | ✅ | 低风险 |
| 新增场景预设 | ✅ | 低风险 |
| 角色卡补充字段 | ✅ | 中风险，要回归测试 |
| 修改铁律 | ⚠️ | 高风险，必须人工写 |
| 修改 SKILL.md description | ❌ | 触发器漂移风险，禁止自动 |
| 修改 version 字段 | ❌ | 必须人工 |
| 删除现有内容 | ❌ | 必须人工 |

---

## 6. 回归测试

每次采纳前必跑 `tests/dry-run-cases.md` 中的所有 case：

```
Test cases:
1. 跳槽决策（Identity Bias 高敏）
2. 技术选型（数据驱动）
3. PRD 审查（多角色协作）
4. 伦理两难（无标准答案）

Pass criteria:
- 不报错
- 输出格式合规
- 自检 8 项全过
- 与 baseline 输出 diff < 30%（防止剧烈漂移）
```

测试失败 → 自动回滚到 `stable-tag.txt` 指向的版本。

---

## 7. 与 research-pipeline 的协作

调研管线产出的 `trace` 文件应同步归档到 evolution/runs/：

```
multi-perspective-debate 调用 research-pipeline 取证
  ↓
research-pipeline 产出 trace
  ↓
trace 写入 multi-perspective-debate/evolution/runs/{run_id}/research-trace.json
  ↓
后续可分析：哪些来源类型最常被引用？哪些工具最常失败？
```

---

## 8. 反 prompt-hacking 防御

LLM 可能给自己提"看起来很好实则烂"的修改建议。防御：

1. **候选必须引用具体 run 数据**——不能凭空说"应该改"
2. **候选必须有量化预期**——"预期 verifiable_citation_ratio 提升 5%"
3. **采纳后必须跑回归**——结果由 baseline 比对决定
4. **diff 大小硬上限**——单次 PR 修改不超过 200 行
5. **频率上限**——同一文件 30 天内不允许超过 2 次修改

---

## 9. 用户使用入口

### 主动反馈

```
用户："这次辩论里执行派太理想化了"
skill：[感知到反馈信号]
       已记录到 feedback/2026-06-12-jobchange.md
       生成候选 PR-007，您可以在 evolution/candidates/PR-007-*.md 审核
```

### 被动收集

每次 skill 跑完，结尾追加一段（默认开启，`--no-evolution` 关闭）：
```
---
本次运行已归档到 evolution/runs/2026-06-12-jobchange-001.json
若有改进建议，回复"反馈：xxx"或编辑该文件
```

### 月度复盘

每月 1 号自动产生 `candidates/PR-monthly-YYYY-MM.md`，列出：
- 上月运行总数
- 触发警告 top 3
- 用户反馈聚类
- 建议采纳的改进 top 3
- 建议人工 review 的复杂问题

---

## 10. 版本历史

- **v0.1**（2026-06-12）：协议初版。runs 自动归档 + feedback 半自动 + candidates 人工审 + 月度复盘 + 回归测试 + 回滚机制。
