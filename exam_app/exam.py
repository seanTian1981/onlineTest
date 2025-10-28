from __future__ import annotations

import random
import textwrap
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Sequence

from .questions import QUESTION_BANK, Category, Question
from .tts import TextToSpeech

OPTION_NUMBERS = ("1", "2", "3", "4", "5", "6")
SCORE_RECORD_FILE = Path(__file__).resolve().parent / "score_records.txt"


@dataclass
class QuestionResult:
    question: Question
    selected_option: Optional[int]
    is_correct: bool


@dataclass
class ExamSummary:
    title: str
    candidate: str
    total_questions: int
    answered_questions: int
    correct_answers: int
    started_at: datetime
    finished_at: datetime
    results: List[QuestionResult]

    @property
    def accuracy(self) -> float:
        if self.answered_questions == 0:
            return 0.0
        return self.correct_answers / self.answered_questions


class ExamEngine:
    def __init__(self, questions: Sequence[Question], speaker: Optional[TextToSpeech] = None) -> None:
        self._questions = list(questions)
        self._speaker = speaker
        self._rng = random.Random()
        self._candidate_name = "考生"
        self._last_summary: Optional[ExamSummary] = None

    def run(self) -> None:
        self._show_banner()
        self._candidate_name = self._ask_candidate_name()
        self._display(
            "您好，{}同学。欢迎来到计算机基础无障碍考试系统。".format(self._candidate_name),
        )
        self._display(
            "系统支持键盘操作，并可在安装 pyttsx3 库后提供语音播报。",
        )
        self._display(
            "菜单中可以选择完整考试、针对某个科目的练习或回顾上次成绩。"
        )
        while True:
            self._separator()
            self._display("主菜单：")
            self._display("1. 开始完整考试（包含四个科目）")
            self._display("2. 针对指定科目练习")
            self._display("3. 回顾最近一次答题成绩")
            self._display("4. 收听操作指南")
            self._display("Q. 退出系统")
            choice = self._get_input("请输入选项（1/2/3/4/Q）：", upper=True)
            if choice == "1":
                self._start_full_exam()
            elif choice == "2":
                self._start_practice()
            elif choice == "3":
                self._review_last_summary()
            elif choice == "4":
                self._speak_instructions()
            elif choice == "Q":
                self._display("感谢使用，祝学习顺利！再见。")
                break
            else:
                self._display("未识别的选项，请重试。")

    def _start_full_exam(self) -> None:
        questions = self._questions.copy()
        self._rng.shuffle(questions)
        title = "综合考试"
        summary = self._conduct_session(title, questions, immediate_feedback=False)
        if summary:
            self._last_summary = summary

    def _start_practice(self) -> None:
        self._display("请输入要练习的科目编号：")
        for index, category in enumerate(Category, start=1):
            self._display(f"{index}. {category.value}")
        selection = self._get_input("科目编号或按回车返回主菜单：")
        if not selection:
            return
        if not selection.isdigit():
            self._display("请输入有效的数字编号。")
            return
        index = int(selection)
        try:
            category = list(Category)[index - 1]
        except IndexError:
            self._display("编号超出范围。")
            return
        questions = [q for q in self._questions if q.category == category]
        if not questions:
            self._display("暂未找到该科目的题目。")
            return
        self._display(
            "共找到{}道题。若需随机抽取，请输入数量；直接回车表示全部答题。".format(len(questions)),
        )
        amount_text = self._get_input("请输入需要练习的题目数量：")
        selected_questions: List[Question]
        if amount_text:
            if not amount_text.isdigit():
                self._display("请输入数字或直接回车。")
                return
            amount = max(1, int(amount_text))
            selected_questions = self._rng.sample(questions, k=min(amount, len(questions)))
        else:
            selected_questions = questions
        title = f"{category.value}练习"
        summary = self._conduct_session(title, selected_questions, immediate_feedback=True)
        if summary:
            self._last_summary = summary

    def _conduct_session(
        self,
        title: str,
        questions: Sequence[Question],
        *,
        immediate_feedback: bool,
    ) -> Optional[ExamSummary]:
        if not questions:
            self._display("没有可用题目。")
            return None
        total = len(questions)
        self._display(f"现在开始“{title}”，共{total}题。")
        started = datetime.now()
        results: List[QuestionResult] = []
        for position, question in enumerate(questions, start=1):
            answer = self._ask_question(question, position, total)
            if answer is None:
                self._display("已提前结束本轮答题。")
                break
            is_correct = answer == question.correct_option
            results.append(QuestionResult(question=question, selected_option=answer, is_correct=is_correct))
            if immediate_feedback:
                if is_correct:
                    self._display("回答正确。")
                else:
                    self._display("回答错误。")
                    correct_number = question.correct_option + 1
                    self._display(f"正确答案是选项{correct_number}：{question.options[question.correct_option]}")
                    self._display(question.explanation)
        finished = datetime.now()
        answered = len(results)
        summary = ExamSummary(
            title=title,
            candidate=self._candidate_name,
            total_questions=total,
            answered_questions=answered,
            correct_answers=sum(1 for r in results if r.is_correct),
            started_at=started,
            finished_at=finished,
            results=results,
        )
        self._present_summary(summary)
        if summary.answered_questions > 0:
            if self._save_summary(summary):
                self._display("本次成绩已保存。")
        return summary

    def _ask_question(self, question: Question, position: int, total: int) -> Optional[int]:
        self._separator("=")
        header = f"第{position}题，共{total}题。科目：{question.category.value}"
        self._display(header)
        self._display(question.prompt)
        spoken_parts: List[str] = [header, question.prompt]
        for idx, option in enumerate(question.options):
            label = OPTION_NUMBERS[idx]
            option_line = f"{label}. {option}"
            self._display(option_line)
            spoken_parts.append(option_line)
        if self._speaker and self._speaker.available:
            self._speaker.speak("。".join(spoken_parts))
        self._display("请输入答案对应的数字。输入R重复朗读题干，输入Q返回主菜单。")
        while True:
            raw = self._get_input("您的选择：", upper=True)
            if raw == "":
                self._display("请选择一个选项。")
                continue
            if raw == "Q":
                return None
            if raw == "R":
                if self._speaker and self._speaker.available:
                    self._speaker.speak("。".join(spoken_parts))
                else:
                    self._display("当前未启用语音播报。")
                continue
            if raw in OPTION_NUMBERS[: len(question.options)]:
                return OPTION_NUMBERS.index(raw)
            self._display("无效输入，请输入题目选项数字。")

    def _present_summary(self, summary: ExamSummary) -> None:
        self._separator()
        duration = summary.finished_at - summary.started_at
        self._display(
            f"{summary.candidate}同学，本次“{summary.title}”答题结束。用时{int(duration.total_seconds())}秒。",
        )
        self._display(
            f"共计划{summary.total_questions}题，实际作答{summary.answered_questions}题，答对{summary.correct_answers}题。",
        )
        accuracy_percent = round(summary.accuracy * 100)
        self._display(f"正确率约为{accuracy_percent}%。")
        if summary.results:
            self._display("逐题回顾：")
        for result in summary.results:
            number_label = result.question.correct_option + 1
            correctness = "正确" if result.is_correct else "错误"
            self._display(
                f"[{correctness}] {result.question.prompt}",
            )
            self._display(
                f"正确答案：{number_label}. {result.question.options[result.question.correct_option]}",
            )
            if not result.is_correct:
                self._display(result.question.explanation)

    def _save_summary(self, summary: ExamSummary) -> bool:
        lines = [
            "-" * 50,
            f"时间：{summary.finished_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"姓名：{summary.candidate}",
            f"考试：{summary.title}",
            f"作答：{summary.answered_questions}/{summary.total_questions}",
            f"正确：{summary.correct_answers}",
            f"正确率：{round(summary.accuracy * 100)}%",
        ]
        for idx, result in enumerate(summary.results, start=1):
            choice = result.selected_option + 1 if result.selected_option is not None else "未作答"
            correctness = "正确" if result.is_correct else "错误"
            lines.append(
                f"第{idx}题：选择{choice}，{correctness}；正确答案为{result.question.correct_option + 1}。"
            )
        lines.append("")
        record = "\n".join(lines)
        try:
            with SCORE_RECORD_FILE.open("a", encoding="utf-8") as file:
                file.write(record)
            return True
        except OSError:
            self._display("保存成绩时出现问题，请检查存储位置。")
            return False

    def _review_last_summary(self) -> None:
        if not self._last_summary:
            self._display("当前暂无历史成绩，请先完成一次答题。")
            return
        self._display("为您回顾最近一次成绩：")
        self._present_summary(self._last_summary)

    def _speak_instructions(self) -> None:
        instructions = (
            "操作指南：系统以键盘输入为主，按数字选择菜单，答案输入数字即可。",
            "在题目界面可以输入R重新朗读题干（需要安装语音库），输入Q返回主菜单。",
            "练习模式会立即告知正误，完整考试则在结束后统一反馈。",
        )
        for item in instructions:
            self._display(item)

    def _show_banner(self) -> None:
        self._separator("=")
        banner = "盲人大学生计算机基础无障碍考试系统"
        self._display(banner)
        self._separator("=")
        if self._speaker and not self._speaker.available:
            self._display(
                "提示：未检测到pyttsx3语音库，将仅以文字形式呈现内容。",
            )

    def _ask_candidate_name(self) -> str:
        name = self._get_input("请输入您的姓名（可留空）：")
        if not name:
            return "考生"
        return name

    def _display(self, text: str, *, speak: bool = True) -> None:
        if not text:
            return
        for line in text.splitlines():
            print(textwrap.fill(line, width=70))
        if speak and self._speaker and self._speaker.available:
            self._speaker.speak(text.replace("\n", "。"))

    def _separator(self, char: str = "-") -> None:
        print(char * 70)

    def _get_input(self, prompt: str, *, upper: bool = False) -> str:
        value = input(prompt)
        value = value.strip()
        if upper:
            value = value.upper()
        self._echo_user_input(value)
        return value

    def _echo_user_input(self, value: str) -> None:
        if not value:
            spoken_value = "空输入"
        elif value.isdigit():
            spoken_value = "数字" + "、".join(value)
        elif len(value) == 1 and value.isalpha():
            spoken_value = f"字母{value}"
        else:
            spoken_value = value
        if self._speaker and self._speaker.available:
            self._speaker.speak(f"您输入的是{spoken_value}")


def build_exam_engine(speaker: Optional[TextToSpeech] = None) -> ExamEngine:
    return ExamEngine(QUESTION_BANK, speaker)
