#!/usr/bin/env python3
"""
会话捕获脚本
读取 Claude Code 的现有数据源，捕获当前会话信息
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


class SessionCapture:
    """捕获 Claude Code 会话信息"""

    def __init__(self, claude_dir: str = None):
        self.claude_dir = Path(claude_dir or os.path.expanduser("~/.claude"))
        self.session_data = {}

    def get_session_id(self) -> str:
        """从环境变量或最新会话目录获取 session ID"""
        # 尝试从环境变量获取
        session_id = os.environ.get("CLAUDE_SESSION_ID")
        if session_id:
            return session_id

        # 从最新�� file-history 目录获取
        file_history_dir = self.claude_dir / "file-history"
        if file_history_dir.exists():
            sessions = sorted(
                [d for d in file_history_dir.iterdir() if d.is_dir()],
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            if sessions:
                return sessions[0].name

        return "unknown-session"

    def get_working_dir(self) -> str:
        """获取当前工作目录"""
        return os.getcwd()

    def get_project_name(self) -> str:
        """从工作目录或 git repo 获取项目名称"""
        working_dir = Path(self.get_working_dir())

        # 从 git repo 获取
        git_dir = working_dir / ".git"
        if git_dir.exists():
            # 读取 git config 获取项目名
            head_file = git_dir / "HEAD"
            if head_file.exists():
                content = head_file.read_text().strip()
                if content.startswith("ref: refs/heads/"):
                    branch = content.split("/")[-1]
                    return branch

        # 使用目录名作为项目名
        return working_dir.name

    def get_git_branch(self) -> str:
        """获取当前 git 分支"""
        working_dir = Path(self.get_working_dir())
        head_file = working_dir / ".git" / "HEAD"

        if head_file.exists():
            content = head_file.read_text().strip()
            if content.startswith("ref: refs/heads/"):
                return content.split("/")[-1]
        return "main"

    def get_file_history(self, session_id: str) -> List[Dict[str, Any]]:
        """获取文件修改历史"""
        file_history_dir = self.claude_dir / "file-history" / session_id

        if not file_history_dir.exists():
            return []

        files = []
        for file_path in file_history_dir.rglob("*"):
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    "path": str(file_path.relative_to(file_history_dir)),
                    "size": stat.st_size,
                    "mtime": stat.st_mtime,
                    "full_path": str(file_path)
                })

        return sorted(files, key=lambda x: x["mtime"], reverse=True)

    def get_todos(self, session_id: str) -> List[Dict[str, Any]]:
        """获取任务列表"""
        todos_dir = self.claude_dir / "todos"

        if not todos_dir.exists():
            return []

        todos = []
        for todo_file in todos_dir.glob(f"{session_id}*agent*.json"):
            try:
                data = json.loads(todo_file.read_text())
                if "todos" in data:
                    todos.extend(data["todos"])
            except Exception as e:
                print(f"Warning: Failed to read {todo_file}: {e}", file=sys.stderr)

        return todos

    def get_session_env(self) -> Dict[str, Any]:
        """获取会话环境信息"""
        session_env_dir = self.claude_dir / "session-env"

        if not session_env_dir.exists():
            return {}

        # 读取最新的会话环境
        env_files = sorted(
            session_env_dir.rglob("*.json"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )

        if env_files:
            try:
                return json.loads(env_files[0].read_text())
            except Exception:
                pass

        return {}

    def capture(self) -> Dict[str, Any]:
        """捕获完整的会话信息"""
        session_id = self.get_session_id()

        self.session_data = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "working_dir": self.get_working_dir(),
            "project_name": self.get_project_name(),
            "git_branch": self.get_git_branch(),
            "files": self.get_file_history(session_id),
            "todos": self.get_todos(session_id),
            "env": self.get_session_env()
        }

        return self.session_data

    def save(self, output_path: str = None) -> str:
        """保存捕获的会话数据到 JSON 文件"""
        if output_path is None:
            output_path = f"/tmp/session_{self.session_data.get('session_id', 'unknown')}.json"

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(self.session_data, f, indent=2, ensure_ascii=False)

        return str(output_path)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="捕获 Claude Code 会话信息")
    parser.add_argument("--output", "-o", help="输出 JSON 文件路径")
    parser.add_argument("--claude-dir", help="Claude 配置目录路径")

    args = parser.parse_args()

    capturer = SessionCapture(claude_dir=args.claude_dir)
    data = capturer.capture()
    output_path = capturer.save(args.output)

    print(f"会话数据已保存到: {output_path}")
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
