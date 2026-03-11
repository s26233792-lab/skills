#!/usr/bin/env python3
"""
记录生成脚本
基于捕获的会话数据和模板，生成 markdown 记录文件
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class RecordGenerator:
    """生成会话记录 markdown 文件"""

    def __init__(
        self,
        template_path: str = None,
        output_dir: str = None,
        skill_dir: str = None
    ):
        if skill_dir is None:
            skill_dir = Path(__file__).parent.parent
        else:
            skill_dir = Path(skill_dir)

        # 模板路径
        if template_path is None:
            template_path = skill_dir / "templates" / "session_record.md"
        else:
            template_path = Path(template_path)

        # 输出目录
        if output_dir is None:
            output_dir = Path.home() / "Downloads" / "claude记录"
        else:
            output_dir = Path(output_dir)

        self.template_path = template_path
        self.output_dir = output_dir
        self.skill_dir = skill_dir

    def load_template(self) -> str:
        """加载模板文件"""
        if not self.template_path.exists():
            raise FileNotFoundError(f"模板文件不存在: {self.template_path}")

        return self.template_path.read_text(encoding="utf-8")

    def load_session_data(self, data_path: str = None) -> Dict[str, Any]:
        """加载会话数据"""
        if data_path is None:
            # 尝试从 /tmp 加载最新的 session 数据
            import glob
            session_files = glob.glob("/tmp/session_*.json")
            if session_files:
                data_path = max(session_files, key=os.path.getmtime)
            else:
                raise FileNotFoundError("未找到会话数据文件")

        with open(data_path, "r") as f:
            return json.load(f)

    def format_file_type(self, path: str) -> str:
        """根据文件扩展名返回文件类型"""
        ext = Path(path).suffix.lower()
        type_map = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".tsx": "React/TSX",
            ".jsx": "React/JSX",
            ".md": "Markdown",
            ".txt": "文本",
            ".json": "JSON",
            ".yaml": "YAML",
            ".yml": "YAML",
            ".html": "HTML",
            ".css": "CSS",
            ".sh": "Shell",
            ".sql": "SQL",
        }
        return type_map.get(ext, ext.lstrip(".") or "文件")

    def format_size(self, size: int) -> str:
        """格式化文件大小"""
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def format_time(self, timestamp: float) -> str:
        """格式化时间戳"""
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    def generate_files_table(self, files: list) -> str:
        """生成文件表格"""
        if not files:
            return "| 无文件 | | | |\n|----|----|----|----|"

        rows = []
        for f in files[:20]:  # 最多显示 20 个文件
            path = f.get("path", f.get("full_path", ""))
            file_type = self.format_file_type(path)
            size = self.format_size(f.get("size", 0))
            mtime = self.format_time(f.get("mtime", 0))

            # 截断过长的路径
            if len(path) > 50:
                path = "..." + path[-47:]

            rows.append(f"| {path} | {file_type} | {size} | {mtime} |")

        return "\n".join(rows)

    def generate_todos_table(self, todos: list) -> str:
        """生成任务表格"""
        if not todos:
            return "| 无任务 | | | |\n|----|----|----|----|"

        rows = []
        for todo in todos:
            content = todo.get("content", "")
            status = todo.get("status", "unknown")
            active_form = todo.get("activeForm", content)

            # 状态图标
            status_map = {
                "completed": "✅ 完成",
                "in_progress": "🔄 进行中",
                "pending": "⏳ 待办"
            }

            rows.append(f"| {active_form} | {status_map.get(status, status)} | | |")

        return "\n".join(rows)

    def detect_tech_stack(self, files: list) -> str:
        """检测技术栈"""
        extensions = set()
        for f in files:
            path = f.get("path", "")
            ext = Path(path).suffix.lower()
            if ext:
                extensions.add(ext)

        stack_map = {
            {".py"}: "Python",
            {".js"}: "JavaScript",
            {".ts", ".tsx"}: "TypeScript",
            {".jsx", ".js"}: "React",
            {".vue"}: "Vue",
            {".go"}: "Go",
            {".rs"}: "Rust",
            {".java"}: "Java",
            {".swift"}: "Swift",
            {".kt"}: "Kotlin",
            {".cpp", ".cc", ".cxx", ".hpp"}: "C++",
            {".c", ".h"}: "C",
            {".html", ".css", ".js"}: "Web",
        }

        for exts, tech in stack_map.items():
            if exts.issubset(extensions):
                return tech

        return "未知"

    def render(self, session_data: Dict[str, Any]) -> str:
        """渲染 markdown 记录"""
        template = self.load_template()

        # 准备替换数据
        replacements = {
            "{PROJECT_NAME}": session_data.get("project_name", "unknown"),
            "{DATE}": session_data.get("date", datetime.now().strftime("%Y-%m-%d")),
            "{TIME}": session_data.get("time", datetime.now().strftime("%H:%M:%S")),
            "{SESSION_ID}": session_data.get("session_id", "unknown"),
            "{WORKING_DIR}": session_data.get("working_dir", os.getcwd()),
            "{GIT_BRANCH}": session_data.get("git_branch", "main"),
            "{FILES_TABLE}": self.generate_files_table(session_data.get("files", [])),
            "{TODOS_TABLE}": self.generate_todos_table(session_data.get("todos", [])),
            "{TECH_STACK}": self.detect_tech_stack(session_data.get("files", [])),
            "{MAIN_REQUEST}": "见对话内容",
            "{COMPLETED_WORK}": f"完成了 {len([t for t in session_data.get('todos', []) if t.get('status') == 'completed'])} 个任务",
            "{GENERATED_FILES_LIST}": f"生成了 {len(session_data.get('files', []))} 个文件",
            "{NOTES}": "无",
            "{GENERATION_TIMESTAMP}": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # 执行替换
        result = template
        for key, value in replacements.items():
            result = result.replace(key, str(value))

        return result

    def generate(self, session_data: Dict[str, Any] = None, data_path: str = None) -> str:
        """生成记录文件"""
        # 加载会话数据
        if session_data is None:
            session_data = self.load_session_data(data_path)

        # 渲染内容
        content = self.render(session_data)

        # 生成文件名
        filename = f"{session_data.get('date', datetime.now().strftime('%Y-%m-%d'))}-{session_data.get('project_name', 'unknown')}-{session_data.get('session_id', 'unknown')[:8]}.md"

        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 写入文件
        output_path = self.output_dir / filename
        output_path.write_text(content, encoding="utf-8")

        return str(output_path)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="生成会话记录 markdown 文件")
    parser.add_argument("--data", "-d", help="会话数据 JSON 文件路径")
    parser.add_argument("--output", "-o", help="输出目录路径")
    parser.add_argument("--template", "-t", help="模板文件路径")

    args = parser.parse_args()

    generator = RecordGenerator(
        template_path=args.template,
        output_dir=args.output
    )

    try:
        output_path = generator.generate(data_path=args.data)
        print(f"记录文件已生成: {output_path}")
    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"生成失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
