from __future__ import annotations

from .exam import build_exam_engine
from .tts import build_tts


def main() -> None:
    speaker = build_tts()
    engine = build_exam_engine(speaker)
    try:
        engine.run()
    except KeyboardInterrupt:
        print("\n已退出考试系统。")
    except EOFError:
        print("\n检测到输入结束，已退出考试系统。")


if __name__ == "__main__":
    main()
