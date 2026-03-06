#!/usr/bin/env python3
"""
报告生成模块
"""

from datetime import datetime
from pathlib import Path

def extract_context(answer: str, keyword: str, context_len: int = 50) -> str:
    """提取关键词周围的上下文"""
    idx = answer.lower().find(keyword.lower())
    if idx == -1:
        return ""
    start = max(0, idx - context_len)
    end = min(len(answer), idx + len(keyword) + context_len)
    context = answer[start:end]
    if start > 0:
        context = "..." + context
    if end < len(answer):
        context = context + "..."
    return context

def analyze_results(results: list, keywords: list) -> dict:
    """分析所有模型的回答结果，按问题分组"""
    by_question = {}
    for result in results:
        q = result["question"]
        if q not in by_question:
            by_question[q] = []
        by_question[q].append(result)
    return by_question

def generate_markdown_report(results: list, keywords: list) -> str:
    """生成 Markdown 格式的对比报告"""
    by_question = analyze_results(results, keywords)
    
    lines = [
        "# LLM 关键词监控报告",
        "",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"监控关键词：{', '.join(keywords)}",
        "",
        "---",
        ""
    ]
    
    total_mentions = 0
    total_models = 0
    
    for i, (question, model_results) in enumerate(by_question.items(), 1):
        lines.append(f"## 问题 {i}：{question}")
        lines.append("")
        lines.append("| 模型 | 提到关键词 | 上下文 |")
        lines.append("|------|-----------|--------|")
        
        for r in model_results:
            total_models += 1
            mentions = ", ".join(r["mentions"]) if r["mentions"] else "无"
            contexts = " / ".join(r["contexts"]) if r["contexts"] else "-"
            if len(contexts) > 100:
                contexts = contexts[:100] + "..."
            
            status = "✅" if r["success"] else "❌"
            lines.append(f"| {r['model']} {status} | {mentions} | {contexts} |")
            
            if r["mentions"]:
                total_mentions += 1
        
        lines.append("")
    
    # 总结
    coverage = (total_mentions / total_models * 100) if total_models > 0 else 0
    lines.append("---")
    lines.append("")
    lines.append("## 总结")
    lines.append("")
    lines.append(f"- **监控模型数**：{len(set(r['model'] for r in results))}")
    lines.append(f"- **问题数**：{len(by_question)}")
    lines.append(f"- **总回答数**：{total_models}")
    lines.append(f"- **提到关键词**：{total_mentions}/{total_models} ({coverage:.1f}%)")
    lines.append("")
    
    return "\n".join(lines)

def save_report(content: str) -> Path:
    """保存报告到文件"""
    reports_dir = Path(__file__).parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-llm-monitor.md")
    filepath = reports_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath
