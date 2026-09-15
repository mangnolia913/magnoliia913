"""命令行入口：python main.py <原文> <抄袭版> <答案文件>"""

import sys

from similarity import read_text, similarity, write_answer


def main() -> int:
    """程序入口，返回退出码。"""
    # 参数校验：程序名 + 3 个路径
    if len(sys.argv) != 4:
        print("Usage: python main.py <original> <copy> <answer>")
        return 1

    orig_path, copy_path, ans_path = sys.argv[1], sys.argv[2], sys.argv[3]

    try:
        orig_text = read_text(orig_path)
        copy_text = read_text(copy_path)
        score = similarity(orig_text, copy_text)
        write_answer(ans_path, score)
        print(f"Similarity: {score:.2f}")
        return 0
    except FileNotFoundError as e:
        print(f"Error: file not found - {e}", file=sys.stderr)
        return 1
    except UnicodeDecodeError as e:
        print(f"Error: encoding failed - {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())