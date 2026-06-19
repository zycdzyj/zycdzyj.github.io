#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import re
import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# --- 配置区 ---
TEMPLATE_FILE = 'template.html'
MARKDOWN_DIR = 'markdown'
OUTPUT_DIR = 'post'

def parse_markdown_file(filepath):
    """解析 Markdown 文件，提取前置标记和内容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 默认数据
    meta = {
        'title': '未命名文章',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'category': '未分类',
        'tags': ['随笔'],
        'content': '',
        'link': '#'
    }

    # 使用正则提取 --- 之间的标记
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if match:
        fm_str = match.group(1)
        md_body = match.group(2)
        
        # 解析标记中的键值对
        for line in fm_str.split('\n'):
            if ':' in line:
                k, v = map(str.strip, line.split(':', 1))
                if k == 'title': meta['title'] = v
                elif k == 'date': meta['date'] = v
                elif k == 'category': meta['category'] = v
                elif k == 'tags': meta['tags'] = [t.strip() for t in v.split(',')]
        
        # 将 Markdown 转换为 HTML
        meta['content'] = markdown.markdown(md_body, extensions=['extra'])
        
        # 生成详情页的相对链接
        safe_title = re.sub(r'[^\w\u4e00-\u9fff]', '_', meta['title'])
        meta['link'] = f"{meta['date']}_{safe_title}.html"
        
    return meta

def generate():
    # 1. 检查模板
    if not os.path.exists(TEMPLATE_FILE):
        print(f"❌ 错误：找不到模板文件 {TEMPLATE_FILE}")
        return

    # 2. 加载 Jinja2 模板
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(TEMPLATE_FILE)

    # 3. 遍历 markdown 文件夹下的所有 .md 文件
    md_files = glob.glob(os.path.join(MARKDOWN_DIR, "*.md"))
    if not md_files:
        print(f"⚠️ 警告：在 {MARKDOWN_DIR} 目录下没有找到任何 .md 文件。")
        return

    articles = []
    category_count = {}
    year_count = {}

    print(f"🔍 找到 {len(md_files)} 篇文章，开始处理...")
    for md_file in md_files:
        try:
            article = parse_markdown_file(md_file)
            articles.append(article)
            
            # 统计分类
            cat = article['category']
            category_count[cat] = category_count.get(cat, 0) + 1
            
            # 统计年份归档
            year = article['date'][:4]
            year_count[year] = year_count.get(year, 0) + 1
        except Exception as e:
            print(f"❌ 处理 {md_file} 时出错: {e}")

    # 4. 按日期倒序排列（最新的在最前面）
    articles.sort(key=lambda x: x['date'], reverse=True)

    # 5. 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 6. 生成每篇文章的详情页
    print("📝 正在生成详情页...")
    for article in articles:
        detail_context = {
            'articles': [article],
            'is_detail_page': True,
            'sorts': [{'name': k, 'count': v} for k, v in category_count.items()],
            'archives': year_count,
            'tags': [{'name': tag} for tag in set(sum([a['tags'] for a in articles], []))]
        }
        detail_path = os.path.join(OUTPUT_DIR, article['link'])
        with open(detail_path, 'w', encoding='utf-8') as f:
            f.write(template.render(**detail_context))
        print(f"   ✅ 生成: {article['title']}")

    # 7. 生成首页
    print("🏠 正在生成首页 index.html...")
    index_context = {
        'articles': articles,
        'is_detail_page': False,
        'sorts': [{'name': k, 'count': v} for k, v in category_count.items()],
        'archives': year_count,
        'tags': [{'name': tag} for tag in set(sum([a['tags'] for a in articles], []))]
    }
    index_path = os.path.join(OUTPUT_DIR, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(template.render(**index_context))

    print(f"\n🎉 构建成功！")
    print(f"📄 共生成 {len(articles)} 篇文章")
    print(f"📁 输出目录: ./{OUTPUT_DIR}/")

if __name__ == '__main__':
    generate()