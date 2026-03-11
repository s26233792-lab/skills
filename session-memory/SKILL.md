---
name: session-memory
description: |
  会话记忆管理 - 自动记录 Claude Code 会话的生成文件和对话历史。

  触发场景：
  - 用户说"保存记录"、"结束会话"、"记录会话"时触发自动保存
  - 用户说"搜索会话"、"查看历史"、"查找记录"时触发搜索
  - 用户说"加载��话"、"恢复记忆"、"恢复上下文"时触发加载

  功能：
  - 自动捕获会话信息（生成的文件、任务、对话）
  - 生成结构化的 markdown 记录文件
  - 支持搜索和检索历史会话
  - 支持加载会话上下文
---

## Overview

这个 Skill 帮助你管理 Claude Code 的会话记忆，自动记录生成的文件和对话历史，方便日后检索和恢复。

## 记录保存位置

默认保存到：`~/Downloads/claude记录/`

## 文件命名规则

```
{YYYY-MM-DD}-{project_name}-{session_id}.md
```

示例：
- `2026-02-17-my-project-a1b2c3d4.md`
- `2026-02-17-claude-code-session-e5f6g7h8.md`

## 核心功能

### 1. 保存会话记录

触发词：`保存记录`、`结束会话`、`记录会话`

**工作流程：**
1. 调用 `scripts/capture_session.py` 捕获当前会话信息
2. 调用 `scripts/generate_record.py` 生成 markdown 文件
3. 保存到 `~/Downloads/claude记录/`

**命令格式：**
```bash
python ~/.claude/skills/session-memory/scripts/capture_session.py
python ~/.claude/skills/session-memory/scripts/generate_record.py
```

### 2. 搜索历史记录

触发词：`搜索会话`、`查看历史`、`查找记录`

**命令格式：**
```bash
python ~/.claude/skills/session-memory/scripts/search_records.py --keyword <关键词>
python ~/.claude/skills/session-memory/scripts/search_records.py --date <日期>
python ~/.claude/skills/session-memory/scripts/search_records.py --project <项目名>
```

### 3. 加载会话上下文

触发词：`加载会话`、`恢复记忆`、`恢复上下文`

**工作流程：**
1. 搜索并选择要加载的记录
2. 读取 markdown 文件内容
3. 将上下文信息呈现给用户

## 记录文件结构

生成的 markdown 文件包含以下部分：

```markdown
# 会话记录: {项目名}

## 基本信息
- 日期: {YYYY-MM-DD}
- 时间: {HH:MM:SS}
- 会话ID: {session-id}
- 工作目录: {working_directory}
- 项目名称: {project_name}

## 生成的文件
| 文件路径 | 类型 | 时间 |
|---------|------|------|
| ... | ... | ... |

## 任务历史
| 任务 | 状态 | 时间 |
|-----|------|------|
| ... | ... | ... |

## 对话摘要
{对话内容摘要}
```

## 使用场景

| 场景 | 操作 |
|------|------|
| 会话结束时保存 | 说"保存记录" |
| 查找之前生成的文件 | 说"搜索会话 - 关键词" |
| 恢复之前的工作上下文 | 说"加载会话 - 项目名" |

## 详细文档

- [完整使用指南](references/usage_guide.md)
- [数据源说明](references/data_sources.md)
