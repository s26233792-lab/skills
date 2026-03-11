#!/usr/bin/env python3
"""
搜索脚本
搜索历史会话记录
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


class RecordSearcher:
    """搜索会话记录"""

    def __init__(self, records_dir: str = None):
        if records_dir is None:
            records_dir = Path.home() / "Downloads" / "claude记录"
        else:
            records_dir = Path(records_dir)

        self.records_dir = records_dir

    def list_records(self) -> List[Dict[str, Any]]:
        """列出所有记录文件"""
        if not self.records_dir.exists():
            return []

        records = []
        for file_path in self.records_dir.glob("*.md"):
            stat = file_path.stat()

            # 解析文件名
            name = file_path.stem  # 去掉 .md
            parts = name.split("-")

            record = {
                "path": str(file_path),
                "name": file_path.name,
                "mtime": stat.st_mtime,
                "size": stat.st_size,
                "date_str": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            }

            # 尝试解析日期和项目名
            if len(parts) >= 3:
                try:
                    record["date"] = f"{parts[0]}-{parts[1]}-{parts[2]}"
                    record["project"] = parts[3] if len(parts) > 3 else "unknown"
                except ValueError:
                    record["date"] = "unknown"
                    record["project"] = "unknown"

            records.append(record)

        return sorted(records, key=lambda x: x["mtime"], reverse=True)

    def search_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """按关键词搜索记录内容"""
        results = []
        keyword_lower = keyword.lower()

        for record in self.list_records():
            try:
                content = Path(record["path"]).read_text(encoding="utf-8")

                # 搜索关键词
                if keyword_lower in content.lower():
                    # 提取匹配行上下文
                    lines = content.split("\n")
                    matches = []

                    for i, line in enumerate(lines):
                        if keyword_lower in line.lower():
                            # 获取上下文（前后各 2 行）
                            start = max(0, i - 2)
                            end = min(len(lines), i + 3)
                            context = lines[start:end]
                            matches.append({
                                "line_num": i + 1,
                                "line": line.strip(),
                                "context": context
                            })

                    if matches:
                        record["matches"] = matches
                        results.append(record)
            except Exception as e:
                print(f"Warning: Failed to read {record['path']}: {e}", file=sys.stderr)

        return results

    def search_by_date(self, date: str) -> List[Dict[str, Any]]:
        """按日期搜索记录"""
        results = []

        # 支持多种日期格式
        date_patterns = [
            date,  # 原样
            date.replace("-", ""),  # 去掉横杠
            date.replace("/", ""),  # 去掉斜杠
        ]

        for record in self.list_records():
            record_date = record.get("date", "")
            for pattern in date_patterns:
                if pattern in record["name"] or pattern in record_date:
                    results.append(record)
                    break

        return results

    def search_by_project(self, project: str) -> List[Dict[str, Any]]:
        """按项目名搜索记录"""
        results = []
        project_lower = project.lower()

        for record in self.list_records():
            record_project = record.get("project", "").lower()
            if project_lower in record["name"].lower() or project_lower in record_project:
                results.append(record)

        return results

    def format_results(self, results: List[Dict[str, Any]], show_content: bool = False) -> str:
        """格式化搜索结果"""
        if not results:
            return "未找到匹配的记录。"

        lines = []
        lines.append(f"找到 {len(results)} 条记录：\n")

        for i, record in enumerate(results, 1):
            lines.append(f"## {i}. {record['name']}")
            lines.append(f"   路径: {record['path']}")
            lines.append(f"   修改时间: {record['date_str']}")

            if "matches" in record and show_content:
                lines.append(f"   匹配数: {len(record['matches'])}")
                lines.append("   匹配内容:")
                for match in record["matches"][:3]:  # 最多显示 3 个匹配
                    lines.append(f"     行 {match['line_num']}: {match['line'][:80]}...")

            lines.append("")

        return "\n".join(lines)

    def load_record(self, record_path: str) -> str:
        """加载记录文件内容"""
        path = Path(record_path)

        if not path.exists():
            # 尝试按名称搜索
            for record in self.list_records():
                if record_path in record["name"]:
                    path = Path(record["path"])
                    break
            else:
                raise FileNotFoundError(f"未找到记录: {record_path}")

        return path.read_text(encoding="utf-8")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="搜索会话记录")
    parser.add_argument("--keyword", "-k", help="搜索关键词")
    parser.add_argument("--date", "-d", help="按日期搜索 (YYYY-MM-DD)")
    parser.add_argument("--project", "-p", help="按项目名搜索")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有记录")
    parser.add_argument("--load", help="加载指定记录的内容")
    parser.add_argument("--records-dir", help="记录目录路径")
    parser.add_argument("--show-content", "-c", action="store_true", help="显示匹配内容")

    args = parser.parse_args()

    searcher = RecordSearcher(records_dir=args.records_dir)

    # 加载记录
    if args.load:
        try:
            content = searcher.load_record(args.load)
            print(content)
            return
        except FileNotFoundError as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)

    # 列出所有记录
    if args.list:
        results = searcher.list_records()
        print(searcher.format_results(results))
        return

    # 搜索
    results = []

    if args.keyword:
        results = searcher.search_by_keyword(args.keyword)
    elif args.date:
        results = searcher.search_by_date(args.date)
    elif args.project:
        results = searcher.search_by_project(args.project)
    else:
        parser.print_help()
        sys.exit(1)

    print(searcher.format_results(results, show_content=args.show_content))


if __name__ == "__main__":
    main()
