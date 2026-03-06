#!/usr/bin/env python3
"""
AI Daily News Generator
抓取 RSS 订阅和网页，生成 AI 日报
"""

import feedparser
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import os
import re
import json
from urllib.parse import urljoin

# 配置
RSS_SOURCES = [
    # === 中文源 ===
    {"name": "宝玉", "url": "https://s.baoyu.io/feed.xml"},
    {"name": "阮一峰", "url": "http://www.ruanyifeng.com/blog/atom.xml"},
    {"name": "Tw93", "url": "https://tw93.fun/feed.xml"},
    {"name": "机器之心", "url": "https://wechat2rss-production-0187.up.railway.app/feed/3926358060.xml"},
    {"name": "BestBlogs", "url": "https://wechat2rss.bestblogs.dev/feed/25185b01482da0f485418ecb92e208b4416712fb.xml"},
    
    # === Agent 架构 ===
    {"name": "AIGC Weekly", "url": "https://aigc-weekly.agi.li/rss.xml"},
    {"name": "LangChain Blog", "url": "https://blog.langchain.com/rss/"},
    {"name": "LlamaIndex Blog", "url": "https://www.llamaindex.ai/blog/rss.xml"},
    {"name": "Last Week in AI", "url": "https://lastweekin.ai/feed"},
    {"name": "OpenAI Blog", "url": "https://openai.com/blog/rss.xml"},
    {"name": "Hugging Face Blog", "url": "https://huggingface.co/blog/feed.xml"},
    
    # === AI 开源项目 ===
    {"name": "GitHub Trending", "url": "https://mshibanami.github.io/GitHubTrendingRSS/daily/all.xml"},
    {"name": "Ollama Blog", "url": "https://ollama.com/blog/rss.xml"},
    {"name": "Replicate Blog", "url": "https://replicate.com/blog/rss.xml"},
    {"name": "Vercel AI SDK", "url": "https://sdk.vercel.ai/feed"},
    {"name": "Papers with Code", "url": "https://paperswithcode.com/rss"},
    
    # === AI 思想 & Newsletter ===
    {"name": "swyx.io", "url": "https://swyx.io/rss.xml"},
    {"name": "Eugene Yan", "url": "https://eugeneyan.com/rss.xml"},
    {"name": "The Batch", "url": "https://www.deeplearning.ai/the-batch/rss/"},
    {"name": "One Useful Thing", "url": "https://www.oneusefulthing.org/feed"},
    {"name": "Import AI", "url": "https://importai.substack.com/feed"},
    {"name": "Interconnects", "url": "https://www.interconnects.ai/feed"},
    {"name": "AI Snake Oil", "url": "https://www.aisnakeoil.com/feed"},
    # {"name": "Simon Willison", "url": "https://simonwillison.net/atom.xml"},  # 需要特殊处理
    # {"name": "LlamaIndex Blog", "url": "https://www.llamaindex.ai/blog/rss.xml"},  # 需要特殊处理
]

HTML_SOURCES = [
    {"name": "Manus Blog", "url": "https://manus.im/zh-cn/blog"},
    {"name": "Cognition Blog", "url": "https://cognition.ai/blog"},
    {"name": "Cline Blog", "url": "https://cline.bot/blog/archive"},
    {"name": "Ampcode", "url": "https://ampcode.com/chronicle"},
    {"name": "Anthropic Engineering", "url": "https://www.anthropic.com/engineering"},
    {"name": "OpenClaw Blog", "url": "https://openclaw.ai/blog"},
    {"name": "Simon Willison TIL", "url": "https://til.simonwillison.net/"},
    {"name": "Hugging Face Blog", "url": "https://huggingface.co/blog"},
    {"name": "LlamaIndex Blog", "url": "https://www.llamaindex.ai/blog"},
]

# Agent/应用相关关键词（高优先级）
AGENT_KEYWORDS = [
    "agent", "agents", "智能体", "代理",
    "mcp", "tool use", "工具调用", "function calling",
    "autonomous", "自主", "workflow", "工作流",
    "rag", "retrieval", "知识库",
    "cursor", "windsurf", "cline", "copilot",
    "coding agent", "coding assistant", "代码助手",
    "manus", "cognition", "devin", " SWE-agent",
    "app", "应用", "product", "产品",
    "orchestration", "编排", "multi-agent", "multi agent",
]

# AI 思想/工程关键词（中高优先级）
THINKING_KEYWORDS = [
    "ai engineering", "llm engineering", "mlops",
    "prompt engineering", "rag", "fine-tuning", "finetune",
    "alignment", "rlhf", "evals", "evaluation",
    "system design", "architecture", "基础设施",
    "observability", "可观测性", "tracing",
    "cost optimization", "token", "latency",
    "best practice", "教训", "lessons",
    "postmortem", "retrospective", "反思",
]

# 开源项目关键词（中优先级）
OPEN_SOURCE_KEYWORDS = [
    "open source", "github", "开源",
    "release", "v0.", "v1.", "v2.", "v3.",
    "launch", "announcing", "introducing",
    "new feature", "update", "版本",
    "self-hosted", "local", "deploy",
]

# 模型发布关键词（低优先级）
MODEL_KEYWORDS = [
    "gpt-", "claude", "gemini", "llama", "deepseek",
    "模型发布", "model release", "paper", "论文",
    "benchmark", "评测", "sota", "arxiv",
]

class NewsAggregator:
    def __init__(self):
        self.articles = []
        self.failed_sources = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
    def fetch_rss(self, source):
        """获取 RSS 订阅"""
        try:
            print(f"📡 获取 RSS: {source['name']}")
            feed = feedparser.parse(source['url'])
            
            if hasattr(feed, 'bozo_exception') and feed.bozo_exception:
                print(f"  ⚠️ RSS 警告: {feed.bozo_exception}")
            
            articles = []
            for entry in feed.entries:
                # 解析日期
                published = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6])
                
                # 获取链接
                link = entry.get('link', '')
                if hasattr(entry, 'guid') and entry.guid:
                    link = entry.guid
                    
                # 获取内容
                content = ''
                if hasattr(entry, 'content') and entry.content:
                    content = entry.content[0].value
                elif hasattr(entry, 'summary'):
                    content = entry.summary
                elif hasattr(entry, 'description'):
                    content = entry.description
                
                # 清理 HTML
                content_text = self.clean_html(content)
                
                articles.append({
                    'title': entry.get('title', 'Untitled'),
                    'link': link,
                    'published': published,
                    'content': content_text[:500],
                    'source': source['name'],
                    'raw_content': content,
                })
            
            print(f"  ✅ 获取 {len(articles)} 篇文章")
            return articles
            
        except Exception as e:
            self.failed_sources.append(f"{source['name']}: {str(e)}")
            print(f"  ❌ 失败: {e}")
            return []
    
    def fetch_html(self, source):
        """获取 HTML 页面内容"""
        try:
            print(f"🌐 获取网页: {source['name']}")
            resp = self.session.get(source['url'], timeout=30)
            resp.raise_for_status()
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            articles = []
            
            # 根据不同网站定制抓取规则
            if 'manus.im' in source['url']:
                articles = self.parse_manus(soup, source)
            elif 'cognition.ai' in source['url']:
                articles = self.parse_cognition(soup, source)
            elif 'cline.bot' in source['url']:
                articles = self.parse_cline(soup, source)
            elif 'ampcode' in source['url']:
                articles = self.parse_ampcode(soup, source)
            elif 'anthropic.com' in source['url']:
                articles = self.parse_anthropic(soup, source)
            elif 'huggingface.co' in source['url']:
                articles = self.parse_huggingface(soup, source)
            elif 'llamaindex.ai' in source['url']:
                articles = self.parse_llamaindex(soup, source)
            elif 'til.simonwillison.net' in source['url']:
                articles = self.parse_simonwillison(soup, source)
            elif 'openclaw.ai' in source['url']:
                articles = self.parse_openclaw(soup, source)
            else:
                # 通用解析
                articles = self.parse_generic(soup, source)
            
            print(f"  ✅ 获取 {len(articles)} 篇文章")
            return articles
            
        except Exception as e:
            self.failed_sources.append(f"{source['name']}: {str(e)}")
            print(f"  ❌ 失败: {e}")
            return []
    
    def parse_manus(self, soup, source):
        """解析 Manus 博客"""
        articles = []
        for item in soup.find_all('a', href=re.compile(r'/blog/')):
            title = item.get_text(strip=True)
            href = item.get('href', '')
            if title and href:
                articles.append({
                    'title': title,
                    'link': urljoin(source['url'], href),
                    'published': datetime.now(),
                    'content': '',
                    'source': source['name'],
                })
        return articles
    
    def parse_cognition(self, soup, source):
        """解析 Cognition 博客"""
        articles = []
        for item in soup.find_all('a', href=re.compile(r'/blog/')):
            title = item.get_text(strip=True)
            href = item.get('href', '')
            if title and href:
                articles.append({
                    'title': title,
                    'link': urljoin(source['url'], href),
                    'published': datetime.now(),
                    'content': '',
                    'source': source['name'],
                })
        return articles
    
    def parse_cline(self, soup, source):
        """解析 Cline 博客"""
        articles = []
        for item in soup.find_all('a', href=True):
            href = item.get('href', '')
            if '/blog/' in href:
                title = item.get_text(strip=True)
                if title:
                    articles.append({
                        'title': title,
                        'link': urljoin(source['url'], href),
                        'published': datetime.now(),
                        'content': '',
                        'source': source['name'],
                    })
        return articles
    
    def parse_ampcode(self, soup, source):
        """解析 Ampcode"""
        articles = []
        for item in soup.find_all('a', href=re.compile(r'/chronicle/')):
            title = item.get_text(strip=True)
            href = item.get('href', '')
            if title and href:
                articles.append({
                    'title': title,
                    'link': urljoin(source['url'], href),
                    'published': datetime.now(),
                    'content': '',
                    'source': source['name'],
                })
        return articles
    
    def parse_anthropic(self, soup, source):
        """解析 Anthropic Engineering"""
        articles = []
        for item in soup.find_all('a', href=True):
            href = item.get('href', '')
            if '/engineering/' in href and item.find(['h2', 'h3', 'h4']):
                title = item.get_text(strip=True)
                if title:
                    articles.append({
                        'title': title,
                        'link': urljoin(source['url'], href),
                        'published': datetime.now(),
                        'content': '',
                        'source': source['name'],
                    })
        return articles

    def parse_huggingface(self, soup, source):
        """解析 Hugging Face Blog"""
        articles = []
        for article in soup.find_all('article'):
            link = article.find('a', href=True)
            if link:
                title = link.get_text(strip=True)
                href = link.get('href', '')
                if title and href and '/blog/' in href:
                    articles.append({
                        'title': title,
                        'link': urljoin(source['url'], href),
                        'published': datetime.now(),
                        'content': '',
                        'source': source['name'],
                    })
        return articles[:20]

    def parse_llamaindex(self, soup, source):
        """解析 LlamaIndex Blog"""
        articles = []
        for item in soup.find_all('a', href=re.compile(r'/blog/')):
            title = item.get_text(strip=True)
            href = item.get('href', '')
            if title and len(title) > 10 and href:
                articles.append({
                    'title': title,
                    'link': urljoin(source['url'], href),
                    'published': datetime.now(),
                    'content': '',
                    'source': source['name'],
                })
        return articles[:20]

    def parse_simonwillison(self, soup, source):
        """解析 Simon Willison TIL"""
        articles = []
        for item in soup.find_all('article', class_='entry'):
            link = item.find('a', href=True)
            if link:
                title = link.get_text(strip=True)
                href = link.get('href', '')
                if title and href:
                    articles.append({
                        'title': f"TIL: {title}",
                        'link': urljoin(source['url'], href),
                        'published': datetime.now(),
                        'content': '',
                        'source': source['name'],
                    })
        return articles[:15]

    def parse_openclaw(self, soup, source):
        """解析 OpenClaw Blog"""
        articles = []
        for item in soup.find_all('a', href=re.compile(r'/blog/')):
            title = item.get_text(strip=True)
            href = item.get('href', '')
            if title and href:
                articles.append({
                    'title': title,
                    'link': urljoin(source['url'], href),
                    'published': datetime.now(),
                    'content': '',
                    'source': source['name'],
                })
        return articles
    
    def parse_generic(self, soup, source):
        """通用解析"""
        articles = []
        # 找文章链接
        for item in soup.find_all(['article', 'div', 'a']):
            link = item.find('a', href=True) if item.name != 'a' else item
            if link:
                href = link.get('href', '')
                title = link.get_text(strip=True)
                if title and len(title) > 10 and href:
                    articles.append({
                        'title': title,
                        'link': urljoin(source['url'], href),
                        'published': datetime.now(),
                        'content': '',
                        'source': source['name'],
                    })
        return articles[:20]  # 限制数量
    
    def clean_html(self, html):
        """清理 HTML 标签"""
        if not html:
            return ''
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    
    def calculate_priority(self, article):
        """计算文章优先级分数"""
        title_lower = article['title'].lower()
        content_lower = article.get('content', '').lower()
        text = title_lower + ' ' + content_lower
        
        score = 0
        base_score = 0
        
        # Agent/应用相关加分（最高优先级）
        for kw in AGENT_KEYWORDS:
            if kw.lower() in text:
                score += 15
                base_score = max(base_score, 15)
        
        # AI 思想/工程加分（高优先级）
        for kw in THINKING_KEYWORDS:
            if kw.lower() in text:
                score += 10
                base_score = max(base_score, 10)
        
        # 开源项目加分（中优先级）
        for kw in OPEN_SOURCE_KEYWORDS:
            if kw.lower() in text:
                score += 8
                base_score = max(base_score, 8)
        
        # 来源加权 - 优先高质量思想源
        source_priority = {
            'Anthropic Engineering': 5,
            'Simon Willison': 5,
            'swyx.io': 5,
            'Eugene Yan': 4,
            'One Useful Thing': 4,
            'Import AI': 4,
            'Interconnects': 4,
            'AI Snake Oil': 4,
            'Last Week in AI': 3,
            'AIGC Weekly': 3,
            'LangChain Blog': 3,
            'LlamaIndex Blog': 3,
        }
        score += source_priority.get(article.get('source', ''), 0)
        
        # 模型发布减分
        for kw in MODEL_KEYWORDS:
            if kw.lower() in text:
                score -= 5
        
        return score
    
    def categorize(self, article):
        """对文章进行分类"""
        title_lower = article['title'].lower()
        content_lower = article.get('content', '').lower()
        text = title_lower + ' ' + content_lower
        source = article.get('source', '')
        
        # Agent 相关
        if any(kw in text for kw in ['agent', 'agents', '智能体', 'mcp', 'coding agent', 'devin', 'manus', 'cognition', 'swe-agent']):
            return '🤖 Agent & 智能体'
        
        # 开源项目发布
        if any(kw in text for kw in ['open source', 'github', 'release', 'launch', 'announcing']):
            if any(kw in text for kw in ['v0.', 'v1.', 'v2.', 'v3.', 'version']):
                return '🚀 开源发布'
        
        # AI 思想/工程深度文章（优先检测来源）
        thinking_sources = ['Simon Willison', 'swyx.io', 'Eugene Yan', 'One Useful Thing', 
                          'Import AI', 'Interconnects', 'AI Snake Oil', 'The Batch']
        if source in thinking_sources:
            return '💡 AI 思想 & 洞察'
        
        # 工程实践
        if any(kw in text for kw in ['engineering', 'architecture', '系统设计', '最佳实践', 
                                     'lesson', 'postmortem', 'observability', 'mlops', 'cost']):
            return '⚙️ 工程实践'
        
        # 开发工具
        if any(kw in text for kw in ['cursor', 'cline', 'windsurf', 'ide', 'vscode', 'ollama', 'replicate']):
            return '🛠️ 开发工具'
        
        # 产品/应用
        if any(kw in text for kw in ['product', 'launch', '发布', '上线', 'app', '应用']):
            return '📱 产品动态'
        
        # 模型
        if any(kw in text for kw in ['model', 'gpt', 'claude', 'llama', 'deepseek', '论文', 'paper']):
            return '🧠 模型与学术'
        
        # 框架/库
        if any(kw in text for kw in ['framework', 'library', 'sdk', 'api', '平台']):
            return '📦 框架与库'
        
        # 默认：检查来源是否是思想类
        if any(s in source.lower() for s in ['simon', 'swyx', 'yan', 'mollick', 'batch']):
            return '💡 AI 思想 & 洞察'
        
        return '📰 其他资讯'
    
    def generate_summary(self, article):
        """生成文章摘要（使用简单的启发式方法）"""
        content = article.get('content', '')
        if not content:
            return '暂无摘要'
        
        # 取前 200 字符作为摘要
        summary = content[:300].strip()
        if len(content) > 300:
            summary += '...'
        
        return summary
    
    def run(self, days=3):
        """运行聚合器"""
        print(f"\n{'='*60}")
        print(f"🚀 AI Daily News Generator")
        print(f"📅 检查最近 {days} 天的更新")
        print(f"{'='*60}\n")
        
        cutoff_date = datetime.now() - timedelta(days=days)
        all_articles = []
        
        # 获取 RSS
        print("📥 获取 RSS 源...")
        for source in RSS_SOURCES:
            articles = self.fetch_rss(source)
            all_articles.extend(articles)
        
        # 获取 HTML
        print("\n📥 获取网页源...")
        for source in HTML_SOURCES:
            articles = self.fetch_html(source)
            all_articles.extend(articles)
        
        # 过滤最近的文章
        print(f"\n📊 过滤最近 {days} 天的文章...")
        recent_articles = []
        for art in all_articles:
            if art.get('published'):
                if art['published'] >= cutoff_date:
                    recent_articles.append(art)
            else:
                # 没有日期的也保留
                recent_articles.append(art)
        
        print(f"   共 {len(recent_articles)} 篇近期文章")
        
        # 去重
        seen = set()
        unique_articles = []
        for art in recent_articles:
            key = art['title'] + art.get('link', '')
            if key not in seen:
                seen.add(key)
                unique_articles.append(art)
        
        print(f"   去重后 {len(unique_articles)} 篇")
        
        # 计算优先级和分类
        for art in unique_articles:
            art['priority'] = self.calculate_priority(art)
            art['category'] = self.categorize(art)
            art['summary'] = self.generate_summary(art)
        
        # 按优先级排序
        unique_articles.sort(key=lambda x: x['priority'], reverse=True)
        
        return unique_articles
    
    def generate_markdown(self, articles, output_dir=None):
        """生成 Markdown 日报"""
        today = datetime.now()
        date_str = today.strftime('%Y%m%d')
        filename = f"{date_str}_v1.md"
        
        if output_dir:
            filepath = os.path.join(output_dir, filename)
        else:
            filepath = filename
        
        # 按分类组织
        categories = {}
        for art in articles:
            cat = art.get('category', '📰 其他资讯')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(art)
        
        # 生成 Markdown
        lines = []
        lines.append(f"# AI 日报 - {today.strftime('%Y年%m月%d日')}")
        lines.append("")
        lines.append(f"> 共收录 {len(articles)} 篇文章")
        lines.append("")
        
        # 失效源
        if self.failed_sources:
            lines.append("## ⚠️ 失效的 RSS 源")
            lines.append("")
            for src in self.failed_sources:
                lines.append(f"- {src}")
            lines.append("")
        
        # 分类输出（按优先级排序）
        category_order = [
            '🤖 Agent & 智能体',
            '💡 AI 思想 & 洞察',
            '🚀 开源发布',
            '🛠️ 开发工具',
            '⚙️ 工程实践',
            '📱 产品动态',
            '📦 框架与库',
            '🧠 模型与学术',
            '📰 其他资讯',
        ]
        
        for cat in category_order:
            if cat in categories and categories[cat]:
                lines.append(f"## {cat}")
                lines.append("")
                for art in categories[cat]:
                    lines.append(f"### {art['title']}")
                    lines.append("")
                    lines.append(f"**Summary**: {art['summary']}")
                    lines.append("")
                    lines.append(f"**原文地址**: [{art.get('link', 'N/A')}]({art.get('link', '#')})")
                    lines.append(f"**来源**: {art['source']}")
                    if art.get('published'):
                        lines.append(f"**时间**: {art['published'].strftime('%Y-%m-%d')}")
                    lines.append("")
        
        content = '\n'.join(lines)
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n✅ 日报已保存: {filepath}")
        return filepath, content


def main():
    """主函数"""
    # 工作目录
    workspace = os.path.expanduser('~/.openclaw/workspace')
    os.makedirs(workspace, exist_ok=True)
    
    # 运行聚合
    aggregator = NewsAggregator()
    articles = aggregator.run(days=3)
    
    if not articles:
        print("\n⚠️ 没有找到新文章")
        return
    
    # 生成日报
    filepath, content = aggregator.generate_markdown(articles, workspace)
    
    # 输出摘要
    print(f"\n{'='*60}")
    print("📋 日报摘要")
    print(f"{'='*60}")
    print(f"文章总数: {len(articles)}")
    print(f"失效源数: {len(aggregator.failed_sources)}")
    print(f"保存路径: {filepath}")
    
    # 返回文件路径用于通知
    return filepath


if __name__ == '__main__':
    main()
