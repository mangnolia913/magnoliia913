"""论文查重核心模块：字符 2-gram + Jaccard 相似度"""

import re

# 预编译正则：\w 在 Unicode 下匹配中文、字母、数字、下划线
# [^\w] 表示“非单词字符”，即标点、空白、换行等
_CLEAN_PATTERN = re.compile(r'[^\w]', re.UNICODE)


def preprocess(text: str) -> str:
    """去除标点、空白，保留中文、字母、数字。

    Args:
        text: 原始文本

    Returns:
        清洗后的文本
    """
    return _CLEAN_PATTERN.sub('', text)


def get_ngrams(text: str, n: int = 2) -> set:
    """获取字符 n-gram 集合。

    Args:
        text: 已预处理的文本
        n: n-gram 的 n，默认 2

    Returns:
        n-gram 字符串集合；若文本长度 < n，返回空集合
    """
    if len(text) < n:
        return set()
    return {text[i:i + n] for i in range(len(text) - n + 1)}