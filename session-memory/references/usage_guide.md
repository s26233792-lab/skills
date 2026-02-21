# 会话记忆管理 - 使用��南

## 概述

`session-memory` Skill 帮助你管理 Claude Code 的会话记忆，自动记录生成的文件和对话历史，方便日后检索和恢复。

## 快速开始

### 1. 保存会话记录

在 Claude Code 中说：

```
保存记录
```

或者直接运行脚本：

```bash
python ~/.claude/skills/session-memory/scripts/capture_session.py
python ~/.claude/skills/session-memory/scripts/generate_record.py
```

记录文件会保存到：`~/Downloads/claude记录/`

### 2. 搜索历史记录

```bash
# 按关键词搜索
python ~/.claude/skills/session-memory/scripts/search_records.py --keyword <关键词>

# 按日期搜索
python ~/.claude/skills/session-memory/scripts/search_records.py --date 2026-02-17

# 按项目名搜索
python ~/.claude/skills/session-memory/scripts/search_records.py --project <项目名>

# 列出所有记录
python ~/.claude/skills/session-memory/scripts/search_records.py --list
```

### 3. 加载历史记录

```bash
# 加载指定记录
python ~/.claude/skills/session-memory/scripts/search_records.py --load <记录文件名>
```

## 文件命��规则

记录文件按以下格式命名：

```
{YYYY-MM-DD}-{project_name}-{session_id_short}.md
```

示例：
- `2026-02-17-my-project-a1b2c3d4.md`
- `2026-02-17-claude-code-session-e5f6g7h8.md`

## 记录文件结构

生成的 markdown 文件包含以下部分：

```markdown
# 会话记录: {项目名}

## 基本信息
- 日期、时间、会话ID
- 工作目录、项目名称、Git 分支

## 生成的文件
文件路径、类型、大小、修改时间

## 任务历史
任务内容、状态、时间

## 对话摘要
主要请求、完成的工作、生成的文件列表

## 技术栈
自动检测的技术栈

## 备注
```

## 自定义配置

### 修改保存目录

在脚本中指定 `--output` 参数：

```bash
python ~/.claude/skills/session-memory/scripts/generate_record.py --output /path/to/dir
```

### 使用自定义模板

```bash
python ~/.claude/skills/session-memory/scripts/generate_record.py --template /path/to/template.md
```

## 数据源

Skill 读取以下 Claude Code 数据源：

| 数据源 | 位置 | 用途 |
|--------|------|------|
| 文件历史 | `~/.claude/file-history/{session-id}/` | 生成的文件列表和版本 |
| 会话环境 | `~/.claude/session-env/` | 工作目录和项目信息 |
| 任务列表 | `~/.claude/todos/*.json` | 任务执行历史 |
| 调试日志 | `~/.claude/debug/latest` | 详细操作记录 |
| 统计数据 | `~/.claude/stats-cache.json` | 活动统计 |

## 常见问题

### Q: 记录文件保存在哪里？

A: 默认保存在 `~/Downloads/claude记录/`，可以通过参数修改。

### Q: 如何恢复之前的会话上下文？

A: 使用搜索命令找到记录，然后用 `--load` 参数加载内容。

### Q: 记录会自动生成吗？

A: 需要手动触发，说"保存记录"或运行脚本。

### Q: 可以搜索对话内容吗？

A: 可以，使用 `--keyword` 参数搜索整个记录内容。

## 技巧

1. **定期保存**：完成重要工作后说"保存记录"
2. **使用有意义的描述**：在记录中添加备注说明工作内容
3. **按项目组织**：搜索时使用项目名快速定位
4. **备份记录**：定期备份 `~/Downloads/claude记录/` 目录

## 示例工作流

```
1. 开始工作
2. 完成一些任务
3. 说"保存记录"
4. 下次打开时
5. 说"搜索会话 - <项目名>"
6. 选择记录加载
7. 快速恢复上下文
```
