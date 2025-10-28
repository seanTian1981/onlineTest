from __future__ import annotations

if __package__ in (None, ""):
    import os
    import sys

    current_directory = os.path.dirname(os.path.abspath(__file__))
    if current_directory not in sys.path:
        sys.path.insert(0, current_directory)

    from exam import build_exam_engine
    from tts import build_tts
else:
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
