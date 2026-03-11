# 数据源说明

## Claude Code 内部数据结构

`session-memory` Skill 通过读取 Claude Code 的现有数据源来捕获会话信息。

## 目录结构

```
~/.claude/
├── file-history/          # 文件修改历史（版本化）
├── session-env/           # 会话环境变量
├── todos/                 # 任务列表（JSON）
├── plans/                 # 任务计划文件
├── debug/                 # 调试日志
└── stats-cache.json       # 使用统计数据
```

## 数据源详解

### 1. file-history/ - 文件历史

**位置**: `~/.claude/file-history/{session-id}/`

**结构**:
```
{session-id}/
├── file1.py@v1
├── file1.py@v2
├── file2.ts@v1
└── ...
```

**用途**: 获取所有生成的文件及其版本信息

**读取方式**:
```python
file_history_dir = claude_dir / "file-history" / session_id
for file_path in file_history_dir.rglob("*"):
    if file_path.is_file():
        # 处理文件
        stat = file_path.stat()
        files.append({
            "path": str(file_path.relative_to(file_history_dir)),
            "size": stat.st_size,
            "mtime": stat.st_mtime
        })
```

### 2. session-env/ - 会话环境

**位置**: `~/.claude/session-env/`

**格式**: JSON 文件

**用途**: 获取工作目录、项目信息、会话配置

**读取方式**:
```python
session_env_dir = claude_dir / "session-env"
for env_file in session_env_dir.glob("*.json"):
    data = json.loads(env_file.read_text())
    # 提取会话信息
```

### 3. todos/ - 任务列表

**位置**: `~/.claude/todos/`

**文件名**: `{session-id}-agent-{agent-id}.json`

**格式**:
```json
{
  "todos": [
    {
      "content": "任务描述",
      "activeForm": "进行中的描述",
      "status": "pending|in_progress|completed"
    }
  ]
}
```

**用途**: 获取任务执行历史

**读取方式**:
```python
todos_dir = claude_dir / "todos"
for todo_file in todos_dir.glob(f"{session_id}*agent*.json"):
    data = json.loads(todo_file.read_text())
    todos.extend(data.get("todos", []))
```

### 4. debug/latest - 调试日志

**位置**: `~/.claude/debug/latest`

**格式**: 文本日志

**用途**: 获取详细的操作记录和对话历史

**读取方式**:
```python
debug_log = claude_dir / "debug" / "latest"
content = debug_log.read_text()
# 解析日志内容
```

### 5. stats-cache.json - 统计数据

**位置**: `~/.claude/stats-cache.json`

**格式**: JSON

**用途**: 获取活动统计、使用模式

**读取方式**:
```python
stats_file = claude_dir / "stats-cache.json"
stats = json.loads(stats_file.read_text())
```

## 会话 ID 获取

会话 ID 可以通过以下方式获取：

### 方法 1: 环境变量
```python
session_id = os.environ.get("CLAUDE_SESSION_ID")
```

### 方法 2: 最新 file-history 目录
```python
file_history_dir = claude_dir / "file-history"
sessions = sorted(
    [d for d in file_history_dir.iterdir() if d.is_dir()],
    key=lambda x: x.stat().st_mtime,
    reverse=True
)
session_id = sessions[0].name if sessions else "unknown"
```

## 项目信息获取

### 工作目录
```python
working_dir = os.getcwd()
```

### 项目名称

从 Git 获取：
```python
git_dir = Path(working_dir) / ".git"
if git_dir.exists():
    head_file = git_dir / "HEAD"
    if head_file.exists():
        content = head_file.read_text().strip()
        if content.startswith("ref: refs/heads/"):
            branch = content.split("/")[-1]
            project_name = branch
```

或使用目录名：
```python
project_name = Path(working_dir).name
```

## 数据完整性

某些数据可能在以下情况下不可用：
- 会话刚刚开始，还没有生成文件
- 会话没有使用 todo 功能
- 调试日志被清理

建议在读取时进行错误处理，提供合理的默认值。
