---
title: 我的第一篇博客
date: 2024-05-20
category: 技术
tags: Python, 博客, 教程
---

# 个人博客调试


# Markdown 综合示例：数学公式与代码高亮

## 1. LaTeX 数学公式支持

**行内公式**：
质能方程 $E = mc^2$ 是物理学中最著名的公式之一。

**独立公式块**：
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

**矩阵与多行公式**：
$$
f(x) = \begin{cases} 
      x^2 & \text{if } x > 0 \\
      0 & \text{if } x \le 0 
   \end{cases}
$$

## 2. 语法高亮代码块

**Python 示例**：
```python
import numpy as np

def calculate_energy(mass, c=3e8):
    """计算质能方程 E=mc^2"""
    return mass * c**2

print(calculate_energy(1))