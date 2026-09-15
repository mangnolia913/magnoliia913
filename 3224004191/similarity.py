"""论文查重核心模块：字符 2-gram + Jaccard 相似度"""

import re

# 预编译正则：\w 在 Unicode 下匹配中文、字母、数字、下划线
# [^\w] 表示“非单词字符”，即标点、空白、换行等
_CLEAN_PATTERN = re.compile(r'[^\w]', re.UNICODE)


def read_text(path: str, encoding: str = 'utf-8') -> str:
    """读取文本文件。

    Args:
        path: 文件绝对路径
        encoding: 文件编码，默认 utf-8

    Returns:
        文件内容字符串

    Raises:
        FileNotFoundError: 文件不存在
        UnicodeDecodeError: 编码不匹配
    """
    with open(path, 'r', encoding=encoding) as file_reader:
        return file_reader.read()


def write_answer(path: str, score: float) -> None:
    """将相似度写入答案文件，保留两位小数。

    Args:
        path: 答案文件绝对路径
        score: 相似度，0.0 ~ 1.0
    """
    with open(path, 'w', encoding='utf-8') as file_writer:
        file_writer.write(f"{score:.2f}")


def preprocess(text: str) -> str:
    """去除标点、空白，保留中文、字母、数字。

    Args:
        text: 原始文本

    Returns:
        清洗后的文本
    """
    return _CLEAN_PATTERN.sub('', text)


def get_ngrams(text: str, ngram_size: int = 2) -> set:
    """获取字符 n-gram 集合（优化版：用 zip 滑窗）。

    Args:
        text: 已预处理的文本
        ngram_size: n-gram 的 n，默认 2

    Returns:
        n-gram 字符串集合；若文本长度 < ngram_size，返回空集合
    """
    if len(text) < ngram_size:
        return set()
    return {''.join(t) for t in zip(*(text[i:] for i in range(ngram_size)))}


def similarity(text1: str, text2: str, ngram_size: int = 2) -> float:
    """计算两段文本的 Jaccard 相似度。

    Args:
        text1: 原文
        text2: 抄袭版
        ngram_size: n-gram 的 n，默认 2

    Returns:
        0.0 ~ 1.0 的浮点数
    """
    ngrams1 = get_ngrams(preprocess(text1), ngram_size)
    ngrams2 = get_ngrams(preprocess(text2), ngram_size)

    # 两篇都为空 → 视为完全一致
    if not ngrams1 and not ngrams2:
        return 1.0
    # 一篇为空 → 视为完全无关
    if not ngrams1 or not ngrams2:
        return 0.0

    intersection = len(ngrams1 & ngrams2)
    union = len(ngrams1 | ngrams2)
    return intersection / union