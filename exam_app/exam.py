from __future__ import annotations

import random
import textwrap
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Sequence

from .questions import QUESTION_BANK, Category, Question
from .tts import TextToSpeech

OPTION_LETTERS = ("A", "B", "C", "D", "E", "F")


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
            self._display("1. 开始完整考试（包含四个科目）", speak=False)
            self._display("2. 针对指定科目练习", speak=False)
            self._display("3. 回顾最近一次答题成绩", speak=False)
            self._display("4. 收听操作指南", speak=False)
            self._display("Q. 退出系统", speak=False)
            choice = input("请输入选项（1/2/3/4/Q）：").strip().upper()
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
                self._display("未识别的选项，请重试。", speak=False)

    def _start_full_exam(self) -> None:
        questions = self._questions.copy()
        self._rng.shuffle(questions)
        title = "综合考试"
        summary = self._conduct_session(title, questions, immediate_feedback=False)
        if summary:
            self._last_summary = summary

    def _start_practice(self) -> None:
        self._display("请输入要练习的科目编号：", speak=False)
        for index, category in enumerate(Category, start=1):
            self._display(f"{index}. {category.value}", speak=False)
        selection = input("科目编号或按回车返回主菜单：").strip()
        if not selection:
            return
        if not selection.isdigit():
            self._display("请输入有效的数字编号。", speak=False)
            return
        index = int(selection)
        try:
            category = list(Category)[index - 1]
        except IndexError:
            self._display("编号超出范围。", speak=False)
            return
        questions = [q for q in self._questions if q.category == category]
        if not questions:
            self._display("暂未找到该科目的题目。", speak=False)
            return
        self._display(
            "共找到{}道题。若需随机抽取，请输入数量；直接回车表示全部答题。".format(len(questions)),
            speak=False,
        )
        amount_text = input("请输入需要练习的题目数量：").strip()
        selected_questions: List[Question]
        if amount_text:
            if not amount_text.isdigit():
                self._display("请输入数字或直接回车。", speak=False)
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
            self._display("没有可用题目。", speak=False)
            return None
        total = len(questions)
        self._display(f"现在开始“{title}”，共{total}题。", speak=True)
        started = datetime.now()
        results: List[QuestionResult] = []
        for position, question in enumerate(questions, start=1):
            answer = self._ask_question(question, position, total)
            if answer is None:
                self._display("已提前结束本轮答题。", speak=True)
                break
            is_correct = answer == question.correct_option
            results.append(QuestionResult(question=question, selected_option=answer, is_correct=is_correct))
            if immediate_feedback:
                if is_correct:
                    self._display("回答正确。", speak=True)
                else:
                    self._display("回答错误。")
                    self._display(f"正确答案是{OPTION_LETTERS[question.correct_option]}：{question.options[question.correct_option]}")
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
        return summary

    def _ask_question(self, question: Question, position: int, total: int) -> Optional[int]:
        self._separator("=")
        header = f"第{position}题，共{total}题。科目：{question.category.value}"
        self._display(header)
        self._display(question.prompt)
        spoken_parts: List[str] = [header, question.prompt]
        for idx, option in enumerate(question.options):
            letter = OPTION_LETTERS[idx]
            option_line = f"{letter}. {option}"
            self._display(option_line, speak=False)
            spoken_parts.append(option_line)
        if self._speaker and self._speaker.available:
            self._speaker.speak("。".join(spoken_parts))
        self._display("请输入答案对应的字母。输入R重复朗读题干，输入Q返回主菜单。", speak=False)
        while True:
            raw = input("您的选择：").strip().upper()
            if raw == "":
                self._display("请选择一个选项。", speak=False)
                continue
            if raw == "Q":
                return None
            if raw == "R":
                if self._speaker and self._speaker.available:
                    self._speaker.speak("。".join(spoken_parts))
                else:
                    self._display("当前未启用语音播报。", speak=False)
                continue
            if raw in OPTION_LETTERS[: len(question.options)]:
                return OPTION_LETTERS.index(raw)
            self._display("无效输入，请输入题目选项字母。", speak=False)

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
        self._display(f"正确率约为{accuracy_percent}%。", speak=False)
        if summary.results:
            self._display("逐题回顾：", speak=False)
        for result in summary.results:
            letter = OPTION_LETTERS[result.question.correct_option]
            correctness = "正确" if result.is_correct else "错误"
            self._display(
                f"[{correctness}] {result.question.prompt}",
                speak=False,
            )
            self._display(
                f"正确答案：{letter}. {result.question.options[result.question.correct_option]}",
                speak=False,
            )
            if not result.is_correct:
                self._display(result.question.explanation, speak=False)

    def _review_last_summary(self) -> None:
        if not self._last_summary:
            self._display("当前暂无历史成绩，请先完成一次答题。", speak=False)
            return
        self._display("为您回顾最近一次成绩：", speak=False)
        self._present_summary(self._last_summary)

    def _speak_instructions(self) -> None:
        instructions = (
            "操作指南：系统以键盘输入为主，按数字选择菜单，答案输入大写或小写字母均可。",
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
                speak=False,
            )

    def _ask_candidate_name(self) -> str:
        name = input("请输入您的姓名（可留空）：").strip()
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


def build_exam_engine(speaker: Optional[TextToSpeech] = None) -> ExamEngine:
    return ExamEngine(QUESTION_BANK, speaker)
