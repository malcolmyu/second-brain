#!/usr/bin/env python3
"""
LLM 关键词监控主程序

使用方式:
    cd ~/.openclaw/workspace
    python3 ~/.openclaw/skills/llm-keyword-monitor/run.py
"""

import json
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from config_loader import load_questions, load_keywords
from report_generator import generate_markdown_report, save_report

# 导入各模型监控模块
from yuanbao import monitor_yuanbao
from deepseek import monitor_deepseek
from kimi import monitor_kimi
from doubao import monitor_doubao
from tongyi import monitor_tongyi

def main():
    """主函数"""
    print("=" * 60)
    print("LLM 关键词监控")
    print("=" * 60)
    
    # 加载配置
    questions = load_questions()
    keywords = load_keywords()
    
    print(f"\n监控问题 ({len(questions)} 个):")
    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q}")
    
    print(f"\n监控关键词: {', '.join(keywords)}")
    print("\n" + "-" * 60)
    
    # 定义监控函数列表
    monitors = [
        monitor_yuanbao,
        monitor_deepseek,
        monitor_kimi,
        monitor_doubao,
        monitor_tongyi
    ]
    
    all_results = []
    
    # 遍历每个问题
    for q_idx, question in enumerate(questions, 1):
        print(f"\n[{q_idx}/{len(questions)}] 提问: {question}")
        
        # 遍历每个模型
        for monitor in monitors:
            model_name = monitor.__name__.replace("monitor_", "")
            print(f"  → 检查 {model_name}...", end=" ", flush=True)
            
            try:
                result = monitor(question, keywords)
                all_results.append(result)
                
                if result["success"]:
                    mentions = len(result["mentions"])
                    print(f"✅ (提到 {mentions} 个关键词)")
                else:
                    error_msg = result.get('error', '未知错误')
                    if len(error_msg) > 30:
                        error_msg = error_msg[:30] + "..."
                    print(f"❌ ({error_msg})")
                    
            except Exception as e:
                print(f"❌ (异常: {e})")
                all_results.append({
                    "model": model_name,
                    "question": question,
                    "answer": "",
                    "mentions": [],
                    "contexts": [],
                    "success": False,
                    "error": str(e)
                })
    
    print("\n" + "=" * 60)
    print("生成报告...")
    
    # 生成报告
    report_content = generate_markdown_report(all_results, keywords)
    report_path = save_report(report_content)
    
    print(f"✅ 报告已保存: {report_path}")
    
    # 输出报告摘要到控制台
    print("\n" + "=" * 60)
    print("报告摘要")
    print("=" * 60)
    
    # 只打印前1500字符
    summary = report_content[:1500]
    if len(report_content) > 1500:
        summary += "\n\n... (完整报告请查看文件)"
    print(summary)
    
    return report_path, report_content

if __name__ == "__main__":
    main()
