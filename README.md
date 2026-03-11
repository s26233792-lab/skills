# Claude Skills Collection

个人 Claude Code 技能集��，扩展 AI 编程助手的专业能力，覆盖设计、文档处理、学术研究、风水布局等多个领域。

## Skills 目录

### 🎨 设计与前端

| Skill | 功能描述 |
|-------|----------|
| **[frontend-design](./frontend-design/)** | 创建高质量、独具特色的前端界面，避免千篇一律的 AI 美学风格。支持网站、落地页、仪表盘、React 组件等。 |
| **[imagen](./imagen/)** | 使用 Google Gemini 生成各类图片：UI 原型、图标、插图、图表、概念艺术图等。 |
| **[article-illustration-generator](./article-illustration-generator/)** | 为文章自动生成配套插图。 |

### 📄 文档与办公

| Skill | 功能描述 |
|-------|----------|
| **[docx](./docx/)** | Word 文档的创建、编辑、分析，支持修订模式、批注、格式保留。 |
| **[pptx](./pptx/)** | PowerPoint 演示文稿的创建、编辑、布局设计和批注。 |
| **[pdf](./pdf/)** | PDF 文档处理：提取文本/表格、创建、合并/拆分、表单填写。 |
| **[xlsx](./xlsx/)** | Excel 电子表格处理：公式、格式化、数据分析、可视化。 |

### 🎓 学术与研究

| Skill | 功能描述 |
|-------|----------|
| **[paper-2-web](./paper-2-web/)** | 将学术论文转化为交互式网页 (Paper2Web)、演示视频 (Paper2Video)、会议海报 (Paper2Poster)。 |
| **[notebooklm](./notebooklm/)** | 直接查询 Google NotebookLM 笔记本，获取基于来源、带引用的答案。 |

### 📚 知识与内容

| Skill | 功能描述 |
|-------|----------|
| **[knowledge-2-web](./knowledge-2-web/)** | 将知识文章转换为精美的交互式网页，自动生成配图，适用于历史、科学、文化等主题。 |

### 🎬 多媒体

| Skill | 功能描述 |
|-------|----------|
| **[manimgl-best-practices](./manimgl-best-practices/)** | ManimGL (3Blue1Brown 版本) 数学动画引擎最佳实践指南。 |
| **[remotion](./remotion/)** | Remotion 程序化视频创作 - 使用 React 制作动画、合成和媒体处理。 |

### 🏠 风水

| Skill | 功能描述 |
|-------|----------|
| **[feng-shui-2026](./feng-shui-2026/)** | 2026 年丙午年九宫飞星风水布局。分析户型图，确定各房间吉凶，提供个性化布局建议（催婚/桃花、催事业/财运、催健康、催学业/文昌、化解凶煞），生成可导入飞书的 CSV 表格。 |

### 🛠️ 开发工具

| Skill | 功能描述 |
|-------|----------|
| **[planning-with-files](./planning-with-files/)** | 基于 Manus 风格的文件规划系统，用于复杂多步骤任务。创建 task_plan.md、findings.md、progress.md。 |
| **[skill-creator](./skill-creator/)** | 创建有效 Claude Skills 的交互式指南。 |
| **[qiuzhi-skill-creator](./qiuzhi-skill-creator/)** | 自定义技能创建向导。 |

## 安装使用

```bash
# 克隆仓库
git clone https://github.com/s26233792-lab/skills.git ~/.claude/skills

# 或者如果你已有该目录，拉取最新更改
cd ~/.claude/skills && git pull
```

## 技能系统

Claude Skills 是一种扩展 Claude Code 能力的方式，每个技能都是一个独立的目录，包含：
- **SKILL.md** - 技能定义文件，包含名称、描述、元数据
- **scripts/** - 实现技能功能的脚本
- **assets/** - 相关资源文件

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可

各技能的具体许可请参阅各自目录下的 LICENSE 文件。
