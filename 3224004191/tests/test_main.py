"""命令行端到端测试：通过 subprocess 调用 main.py"""

import re
import subprocess
import sys
from pathlib import Path

MAIN = Path(__file__).resolve().parent.parent / "main.py"
DATA = Path(__file__).resolve().parent / "data"


def test_cli_normal(tmp_path):
    """正常调用：应生成两位小数的答案文件"""
    orig = tmp_path / "orig.txt"
    copy = tmp_path / "copy.txt"
    ans = tmp_path / "ans.txt"
    orig.write_text("今天是星期天，天气晴。", encoding="utf-8")
    copy.write_text("今天是周天，天气晴朗。", encoding="utf-8")

    ret = subprocess.run(
        [sys.executable, str(MAIN), str(orig), str(copy), str(ans)],
        capture_output=True, text=True
    )
    assert ret.returncode == 0
    assert re.fullmatch(r"\d+\.\d{2}", ans.read_text(encoding="utf-8"))


def test_cli_missing_args():
    """参数不足：应返回非 0 退出码并提示 Usage"""
    ret = subprocess.run(
        [sys.executable, str(MAIN)],
        capture_output=True, text=True
    )
    assert ret.returncode != 0
    assert "Usage" in ret.stdout or "Usage" in ret.stderr


def test_cli_file_not_found(tmp_path):
    """文件不存在：应返回非 0 退出码并提示错误"""
    ans = tmp_path / "ans.txt"
    ret = subprocess.run(
        [sys.executable, str(MAIN), "no_such.txt", "no_such2.txt", str(ans)],
        capture_output=True, text=True
    )
    assert ret.returncode != 0
    assert "not found" in ret.stderr.lower() or "error" in ret.stderr.lower()


def test_cli_identical_files(tmp_path):
    """相同文件：答案应为 1.00"""
    orig = tmp_path / "orig.txt"
    ans = tmp_path / "ans.txt"
    orig.write_text("测试文本内容", encoding="utf-8")

    ret = subprocess.run(
        [sys.executable, str(MAIN), str(orig), str(orig), str(ans)],
        capture_output=True, text=True
    )
    assert ret.returncode == 0
    assert ans.read_text(encoding="utf-8") == "1.00"


def test_cli_real_data(tmp_path):
    """用老师提供的真实样例跑命令行"""
    ans = tmp_path / "ans.txt"
    ret = subprocess.run(
        [sys.executable, str(MAIN),
         str(DATA / "orig.txt"),
         str(DATA / "orig_0.8_add.txt"),
         str(ans)],
        capture_output=True, text=True
    )
    assert ret.returncode == 0
    content = ans.read_text(encoding="utf-8")
    assert re.fullmatch(r"\d+\.\d{2}", content)