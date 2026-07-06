import os
import re
import subprocess

def run_cmd(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

readme_path = "README.md"
def read_readme():
    with open(readme_path, "r", encoding="utf-8") as f:
        return f.read()

def write_readme(content):
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

# STEP 1: Tabularize bullets
bullets_data = [
    # Section 1 (0 to 3)
    {"title": "The Variable-Length Padding Alignment Era", "desc": "The core structural baseline introduced during the genesis of the Transformer architecture. Because GPUs demand rectangular, uniformly shaped dense matrices to compute parallel tensor mathematics efficiently, sequences inside a training batch must be stretched to match the longest sentence using empty [PAD] tokens. The Padding Attention Mask maps these indices, zeroing out their attention weights to ensure the network's parameters are never corrupted by nonsense padding padding noise.", "year": "2017", "paper": "https://arxiv.org/abs/1706.03762", "slug": "padding-alignment"},
    {"title": "The Autoregressive Causal Hard-Lock Era", "desc": "Ported transformers out of bidirectional comprehension and straight into generative auto-regressive decoding. To train a decoder model to predict the next token, it must be strictly blocked from cheating by looking ahead at future answer strings. The Causal Attention Mask solves this by enforcing an immutable lower-triangular matrix boundary. Limitation: Heavy memory-bandwidth bound.", "year": "2018", "paper": "https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf", "slug": "causal-hard-lock"},
    {"title": "The Hardware-Fused Block-Sparse Masking Era", "desc": "Re-architected masking logic to match the physical storage properties of GPU silicon layout. Pioneered by Tri Dao et al.'s FlashAttention, it replaces massive, flat software masks with block-wise tiling subroutines.", "year": "2022", "paper": "https://arxiv.org/abs/2205.14135", "slug": "block-sparse-masking"},
    {"title": "The Unified Multi-Modal Segment Enclave Era", "desc": "The current modern state-of-the-art foundation standard. Driven by omni-directional architectures (such as GPT-4o or Claude 3.5 pipelines) that flatline pixels, acoustics, and strings into a single shared attention workspace.", "year": "2024", "paper": "https://arxiv.org/abs/2403.05530", "slug": "segment-enclave"},
    
    # Section 2 (4 to 7)
    {"title": "Padding Attention Mask", "desc": "Mechanism: A 1D binary vector translated into a 2D matrix. It tracks the physical sequence lengths inside a mini-batch, injecting negative infinity into any coordinate slot corresponding to a trailing [PAD] token index.", "year": "2017", "paper": "https://arxiv.org/abs/1706.03762", "slug": "padding-mask"},
    {"title": "Causal / Lower-Triangular Mask", "desc": "Mechanism: Imposes a strict chronological arrow of time over token generation, setting the attention score to zero for all future indices where column position j > row position i.", "year": "2018", "paper": "https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf", "slug": "causal-mask"},
    {"title": "Local / Sliding Window Attention Mask", "desc": "Mechanism: Restricts a token's attention field to a thin, localized neighborhood of adjacent tokens, masking out distant indices.", "year": "2020", "paper": "https://arxiv.org/abs/2004.05150", "slug": "sliding-window-mask"},
    {"title": "Prefix / Interleaved Segment Mask", "desc": "Mechanism: Tailored for instruction-following and Retrieval-Augmented Generation (RAG) structures.", "year": "2021", "paper": "https://arxiv.org/abs/2108.12409", "slug": "prefix-mask"},
    
    # Section 3 (8 to 9)
    {"title": "Document-Boundary Packing Masks (Flash-Decoding)", "desc": "Profile: Slashes pre-training compute waste. To maximize token-per-second processing efficiency, engineers pack multiple short, completely separate user documents into a single massive 8k or 32k token context window chunk.", "year": "2023", "paper": "https://arxiv.org/abs/2308.16137", "slug": "document-packing"},
    {"title": "Instruction-Isolating XML Enclave Masks", "desc": "Profile: Hardens defenses against prompt injection exploits. It applies a restricted masking policy over user-provided data inputs.", "year": "2024", "paper": "https://arxiv.org/abs/2405.00332", "slug": "xml-enclave"},
    
    # Section 4 (10 to 11)
    {"title": "The Non-Contiguous Fragmented Memory Core Stall", "desc": "The Problem: Executing custom sparse or irregular attention masking layouts requires the GPU processor to fetch non-contiguous memory coordinates from slow global High Bandwidth Memory (HBM) repeatedly.", "year": "2022", "paper": "https://arxiv.org/abs/2205.14135", "slug": "memory-stall"},
    {"title": "The KV Cache Memory Inflation and VRAM Explosion Wall", "desc": "The Problem: Maintaining unconstrained causal attention maps over ultra-long context windows (128k+ tokens) forces the system to store massive, multi-gigabyte Key-Value attention tensors concurrently.", "year": "2023", "paper": "https://arxiv.org/abs/2309.06180", "slug": "kv-cache-inflation"},
    
    # Section 5 (12 to 14)
    {"title": "Pre-Training Web-Scale Multi-Modal Foundational Transformers (GPT/Llama)", "desc": "Application: Guides cluster-wide parameter initialization. Fused document-packing and multi-modal segment masks process text, code repos, and visual patches concurrently.", "year": "2024", "paper": "https://arxiv.org/abs/2407.21783", "slug": "pretraining-multimodal"},
    {"title": "Low-Latency Enterprise RAG Search & Text-to-SQL Engines", "desc": "Application: Compresses model generation latencies within corporate endpoints. Prefix attention masking allows the system to cache and freeze the Key-Value states of massive corporate documentation catalogs.", "year": "2023", "paper": "https://arxiv.org/abs/2307.03172", "slug": "rag-search"},
    {"title": "Secure Multi-Agent Tool Orchestration and Data Extraction", "desc": "Application: Secures autonomous digital agents against malicious exploits. Instruction-isolating masks shield the model's primary function-calling layers.", "year": "2024", "paper": "https://arxiv.org/abs/2402.14830", "slug": "secure-agents"}
]

readme = read_readme()

sections_text = [
    (r"\* \*\*The Variable-Length Padding Alignment Era[\s\S]*?(?=\n---)", 0, 4),
    (r"- ### A\. Padding Attention Mask[\s\S]*?(?=\n---)", 4, 8),
    (r"\* \*\*Document-Boundary Packing Masks[\s\S]*?(?=\n---)", 8, 10),
    (r"\* \*\*The Non-Contiguous Fragmented Memory Core Stall[\s\S]*?(?=\n---)", 10, 12),
    (r"\* \*\*Pre-Training Web-Scale Multi-Modal Foundational Transformers[\s\S]*?(?=\n---)", 12, 15)
]

for pattern, start_idx, end_idx in sections_text:
    table = "| Concept | Description | Year | Paper | Details |\n|---|---|---|---|---|\n"
    for i in range(start_idx, end_idx):
        b = bullets_data[i]
        table += f"| **{b['title']}** | {b['desc']} | {b['year']} | [Paper]({b['paper']}) | [Read More](./assets/pages/{b['slug']}.md) |\n"
    
    readme = re.sub(pattern, table, readme, count=1)

write_readme(readme)
run_cmd('git add . && git commit -m "tabularised the bullets" && git push')

# STEP 2: Create detailed pages
os.makedirs("assets/pages", exist_ok=True)
for b in bullets_data:
    page_content = f"# {b['title']}\n\n## Overview\n{b['desc']}\n\n## Diagram\n```mermaid\ngraph TD\n  A[{b['title']}] --> B(Detailed Implementation)\n  B --> C{{Optimizations}}\n```\n\n## Meta\n- **Year**: {b['year']}\n- **Paper**: [Link]({b['paper']})\n\n[Back to README](../../README.md)"
    with open(f"assets/pages/{b['slug']}.md", "w", encoding="utf-8") as f:
        f.write(page_content)

run_cmd('git add . && git commit -m "detailed pages created" && git push')

# STEP 3: Emojis and Banner
svg_content = '''<svg width="800" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:rgb(255,255,0);stop-opacity:1" />
      <stop offset="100%" style="stop-color:rgb(255,0,0);stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="800" height="200" fill="url(#grad1)">
    <animate attributeName="opacity" values="0.5;1;0.5" dur="3s" repeatCount="indefinite" />
  </rect>
  <text fill="#ffffff" font-size="45" font-family="Verdana" x="50" y="110">Awesome Attention Mask</text>
</svg>'''
os.makedirs("assets", exist_ok=True)
with open("assets/banner.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

readme = read_readme()
readme = f'<p align="center"><img src="./assets/banner.svg" alt="Banner"></p>\n\n' + readme

emoji_replacements = {
    "## 1. The Macro Chronological Evolution": "## 🕰️ 1. The Macro Chronological Evolution",
    "## 2. Core Functional & Algorithmic Mask Variants": "## ⚙️ 2. Core Functional & Algorithmic Mask Variants",
    "## 3. High-Capacity Architectural & Token Masking Types": "## 🏗️ 3. High-Capacity Architectural & Token Masking Types",
    "## 4. Production Engineering Challenges & Hardware Solutions": "## 🏭 4. Production Engineering Challenges & Hardware Solutions",
    "## 5. Frontier Real-World AI Industrial Applications": "## 🚀 5. Frontier Real-World AI Industrial Applications",
    "## References": "## 📚 References",
}
for k, v in emoji_replacements.items():
    readme = readme.replace(k, v)

write_readme(readme)
run_cmd('git add . && git commit -m "added emojis and banner" && git push')

# STEP 4: Badges and SEO to Left
left_badges = '<p align="center">\n<a href="https://github.com/ishandutta2007/Awesome-Awesome-Awesome"><img src="https://img.shields.io/badge/Awesome-%E2%9C%94-blueviolet?style=flat-square&logo=github" alt="Awesome"/></a><a href="https://discord.gg/jc4xtF58Ve"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" /></a>\n</p>\n'
readme = read_readme()
readme = readme.replace('alt="Banner"></p>\n\n', f'alt="Banner"></p>\n\n{left_badges}\n\n<!-- SEO: This repository provides a curated list of resources, variants, and applications for Attention Masks in AI Transformers. -->\n')
write_readme(readme)
run_cmd('git add . && git commit -m "seo optimised and badges to left added" && git push')

# STEP 5: Right Badge
right_badge = '<a href="https://github.com/ishandutta2007"><img alt="GitHub followers" src="https://img.shields.io/github/followers/ishandutta2007?label=Follow" /></a>'
readme = read_readme()
readme = readme.replace('alt="Discord" /></a>\n</p>', f'alt="Discord" /></a>{right_badge}\n</p>')
write_readme(readme)
run_cmd('git add . && git commit -m "badges to right added" && git push')

# STEP 6: Star History
star_history_text = '''
## ⭐ Star History
<div align="center">
<a href="https://www.star-history.com/?repos=ishandutta2007/Awesome-Attention-Mask&type=date&legend=bottom-right">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/Awesome-Attention-Mask&type=date&theme=dark&legend=bottom-right" />
<source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/Awesome-Attention-Mask&type=date&legend=bottom-right" />
<img alt="Star History Chart" src="https://api.star-history.com/chart?repos=ishandutta2007/Awesome-Attention-Mask&type=date&legend=bottom-right" />
</picture>
</a>
</div>
'''
readme = read_readme()
readme = readme + "\n" + star_history_text
write_readme(readme)
run_cmd('git add . && git commit -m "star history added" && git push')

# STEP 7: Fix chartrepos
readme = read_readme()
readme = readme.replace('chartrepos', 'chart?repos')
write_readme(readme)
run_cmd('git add . && git commit -m "fixed star plot" && git push')

# STEP 8: Fix invalid awesome link
readme = read_readme()
readme = readme.replace('https://github.com/sindresorhus/awesome', 'https://github.com/ishandutta2007/Awesome-Awesome-Awesome')
write_readme(readme)
run_cmd('git add . && git commit -m "invalid awesome link fixed" && git push')

print("All tasks completed successfully!")
