"""核心算法单元测试：覆盖正常、边界、异常三类情况"""

import os

import pytest

from similarity import (
    read_text,
    write_answer,
    preprocess,
    get_ngrams,
    similarity,
)


# ---------- 正常路径 ----------

def test_identical_text_returns_one():
    """完全相同的文本，相似度应为 1.00"""
    assert similarity("今天是星期天，天气晴", "今天是星期天，天气晴") == pytest.approx(1.0)


def test_completely_different_text():
    """完全无关的文本，相似度应接近 0"""
    score = similarity("今天是星期天，天气晴", "计算机操作系统进程调度算法")
    assert score < 0.1


def test_small_modification():
    """少量增删改，相似度应大于 0.3（短文本 2-gram 敏感，阈值放宽）"""
    score = similarity(
        "今天是星期天，天气晴，今天晚上我要去看电影。",
        "今天是周天，天气晴朗，我晚上要去看电影。"
    )
    assert score > 0.3


def test_punctuation_only_difference():
    """仅标点不同，相似度应很高"""
    score = similarity("今天天气晴。", "今天天气晴！")
    assert score > 0.9


def test_whitespace_only_difference():
    """仅空白不同，相似度应很高"""
    score = similarity("今天 天气 晴", "今天\n天气\t晴")
    assert score > 0.9


def test_english_case_sensitive():
    """英文大小写敏感：算法不做 lower 归一化，Hello 与 hello 不完全一致"""
    score = similarity("Hello World", "hello world")
    assert 0.0 < score < 1.0


# ---------- 边界路径 ----------

def test_empty_original():
    """原文为空，相似度应为 0"""
    assert similarity("", "今天天气晴") == 0.0


def test_empty_copy():
    """抄袭版为空，相似度应为 0"""
    assert similarity("今天天气晴", "") == 0.0


def test_both_empty():
    """两篇都为空，视为完全一致"""
    assert similarity("", "") == 1.0


def test_text_shorter_than_n():
    """文本长度小于 n，n-gram 集合为空"""
    assert get_ngrams("啊", n=2) == set()
    assert get_ngrams("", n=2) == set()


def test_preprocess_removes_punctuation():
    """预处理应去除标点和空白"""
    assert preprocess("你好，世界！\n") == "你好世界"
    assert preprocess("Hello, World! 123") == "HelloWorld123"


# ---------- 异常路径 ----------

def test_read_text_file_not_found():
    """读取不存在的文件应抛 FileNotFoundError"""
    with pytest.raises(FileNotFoundError):
        read_text("not_exist_file_xyz.txt")


def test_write_answer_two_decimal(tmp_path):
    """答案文件应保留两位小数"""
    ans = tmp_path / "ans.txt"
    write_answer(str(ans), 0.856)
    assert ans.read_text(encoding="utf-8") == "0.86"


def test_write_answer_rounding(tmp_path):
    """四舍五入测试"""
    ans = tmp_path / "ans.txt"
    write_answer(str(ans), 0.854)
    assert ans.read_text(encoding="utf-8") == "0.85"


# ---------- 真实数据集成测试 ----------

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def test_real_data_orig_vs_add():
    """真实样例 orig vs orig_0.8_add：相似度应在合理区间"""
    orig = read_text(os.path.join(DATA_DIR, "orig.txt"))
    copy = read_text(os.path.join(DATA_DIR, "orig_0.8_add.txt"))
    score = similarity(orig, copy)
    assert 0.3 < score < 0.9


def test_real_data_orig_vs_dis_1():
    """1% 字符扰乱，相似度应很高"""
    orig = read_text(os.path.join(DATA_DIR, "orig.txt"))
    copy = read_text(os.path.join(DATA_DIR, "orig_0.8_dis_1.txt"))
    score = similarity(orig, copy)
    assert score > 0.7


def test_real_data_orig_vs_dis_15():
    """15% 字符扰乱，相似度应较低"""
    orig = read_text(os.path.join(DATA_DIR, "orig.txt"))
    copy = read_text(os.path.join(DATA_DIR, "orig_0.8_dis_15.txt"))
    score = similarity(orig, copy)
    assert score < 0.6
    