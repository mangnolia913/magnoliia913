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


def similarity(text1: str, text2: str, n: int = 2) -> float:
    """计算两段文本的 Jaccard 相似度。

    Args:
        text1: 原文
        text2: 抄袭版
        n: n-gram 的 n，默认 2

    Returns:
        0.0 ~ 1.0 的浮点数
    """
    s1 = get_ngrams(preprocess(text1), n)
    s2 = get_ngrams(preprocess(text2), n)

    # 两篇都为空 → 视为完全一致
    if not s1 and not s2:
        return 1.0
    # 一篇为空 → 视为完全无关
    if not s1 or not s2:
        return 0.0

    intersection = len(s1 & s2)
    union = len(s1 | s2)
    return intersection / union