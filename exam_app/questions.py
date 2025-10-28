from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Sequence


class Category(str, Enum):
    COMPUTER_BASICS = "计算机基础知识"
    WORD = "Word操作"
    EXCEL = "Excel操作"
    POWERPOINT = "PPT操作"


@dataclass(frozen=True)
class Question:
    id: str
    category: Category
    prompt: str
    options: List[str]
    correct_option: int
    explanation: str


QUESTION_BANK: Sequence[Question] = (
    Question(
        id="basic-1",
        category=Category.COMPUTER_BASICS,
        prompt="以下哪一项属于计算机的输出设备？",
        options=["键盘", "鼠标", "显示器", "扫描仪"],
        correct_option=2,
        explanation="显示器负责向用户呈现信息，因此属于输出设备。",
    ),
    Question(
        id="basic-2",
        category=Category.COMPUTER_BASICS,
        prompt="操作系统的主要作用是什么？",
        options=[
            "只负责保护计算机",
            "管理硬件和软件资源并提供运行环境",
            "自动升级所有应用程序",
            "生产新的硬件设备",
        ],
        correct_option=1,
        explanation="操作系统负责协调硬件和软件资源，为应用程序提供运行环境。",
    ),
    Question(
        id="basic-3",
        category=Category.COMPUTER_BASICS,
        prompt="在校园网络中，IP地址的作用是？",
        options=[
            "存储个人文档",
            "唯一标识网络中的一台设备",
            "加密无线信号",
            "修复网络线路",
        ],
        correct_option=1,
        explanation="IP地址用于在网络中唯一标识一台设备，方便数据正确传输。",
    ),
    Question(
        id="basic-4",
        category=Category.COMPUTER_BASICS,
        prompt="以下哪种做法有助于安全地使用校园网络？",
        options=[
            "在公共电脑上保存登录密码",
            "养成定期更新系统补丁的习惯",
            "与他人共享个人账户",
            "关闭杀毒软件以节省资源",
        ],
        correct_option=1,
        explanation="定期更新系统补丁可以修补漏洞，增强网络使用安全性。",
    ),
    Question(
        id="basic-5",
        category=Category.COMPUTER_BASICS,
        prompt="扩展名为 .pdf 的文件通常用于？",
        options=[
            "存放可执行程序",
            "存放结构化的文档内容",
            "存放临时缓存",
            "存放系统驱动",
        ],
        correct_option=1,
        explanation="PDF是一种便于跨平台阅读的文档格式，适合保存排版后的内容。",
    ),
    Question(
        id="basic-6",
        category=Category.COMPUTER_BASICS,
        prompt="为了防止数据丢失，最合适的做法是？",
        options=[
            "只保存在桌面",
            "定期做多份备份并存放在不同位置",
            "只依赖回收站",
            "不使用任何密码",
        ],
        correct_option=1,
        explanation="多地备份可以在设备损坏或误删时迅速恢复重要数据。",
    ),
    Question(
        id="word-1",
        category=Category.WORD,
        prompt="在Word中快速选中整个文档的快捷键是？",
        options=["Ctrl+A", "Ctrl+S", "Ctrl+Shift+L", "Alt+F4"],
        correct_option=0,
        explanation="按下Ctrl+A会选中文档中的全部内容。",
    ),
    Question(
        id="word-2",
        category=Category.WORD,
        prompt="为了让屏幕阅读器可以准确识别文档结构，应该怎样设置章节标题？",
        options=[
            "直接调大字体",
            "应用内置的标题样式",
            "使用文本框排版",
            "插入图片充当标题",
        ],
        correct_option=1,
        explanation="应用标题样式可以让文档结构对屏幕阅读器友好。",
    ),
    Question(
        id="word-3",
        category=Category.WORD,
        prompt="在Word中插入分页符以开始新的一页，应使用哪种操作？",
        options=["Ctrl+Enter", "Ctrl+Shift+P", "Alt+Tab", "Ctrl+Alt+Del"],
        correct_option=0,
        explanation="按下Ctrl+Enter可以插入分页符，使内容从新的一页开始。",
    ),
    Question(
        id="word-4",
        category=Category.WORD,
        prompt="要为插入的图片添加替代文字以帮助盲人同学理解内容，应打开哪个对话框？",
        options=[
            "图片版式",
            "设置为背景",
            "图片格式中的替代文字",
            "拼写与语法",
        ],
        correct_option=2,
        explanation="在图片格式设置中填写替代文字可以让屏幕阅读器朗读图片含义。",
    ),
    Question(
        id="word-5",
        category=Category.WORD,
        prompt="以下哪种方法可以通过键盘快速创建项目符号列表？",
        options=[
            "输入星号加空格后输入内容",
            "按下Ctrl+Shift+S",
            "按下Alt+F9",
            "按下Ctrl+Alt+Delete",
        ],
        correct_option=0,
        explanation="在段落开头输入*加空格后继续输入文字，Word会自动转换为项目符号列表。",
    ),
    Question(
        id="word-6",
        category=Category.WORD,
        prompt="为确保共享文档时保留格式并方便阅读，通常应保存为哪种格式？",
        options=[".txt", ".docx", ".tmp", ".log"],
        correct_option=1,
        explanation=".docx格式支持大多数Word功能和辅助技术，是通用的共享格式。",
    ),
    Question(
        id="excel-1",
        category=Category.EXCEL,
        prompt="在Excel中查看单元格公式而不进入编辑状态，可以使用哪个快捷键？",
        options=["F2", "Shift+F3", "Alt+F8", "Ctrl+S"],
        correct_option=0,
        explanation="按下F2可查看并编辑当前单元格的公式或内容。",
    ),
    Question(
        id="excel-2",
        category=Category.EXCEL,
        prompt="要让第一行标题在滚动时始终可见，应使用哪项功能？",
        options=["条件格式", "冻结窗格", "分列", "筛选"],
        correct_option=1,
        explanation="冻结窗格可以锁定特定的行或列，使其在滚动时保持可见。",
    ),
    Question(
        id="excel-3",
        category=Category.EXCEL,
        prompt="以下哪个函数可以计算一组数据的平均值？",
        options=["SUM", "AVERAGE", "MAX", "COUNT"],
        correct_option=1,
        explanation="AVERAGE函数用于计算选中范围内数值的平均值。",
    ),
    Question(
        id="excel-4",
        category=Category.EXCEL,
        prompt="在Excel中为图表添加替代文字，应使用的操作是？",
        options=[
            "双击图表区域并选择替代文字",
            "切换到页面布局视图",
            "使用打印预览",
            "插入批注",
        ],
        correct_option=0,
        explanation="在图表格式设置中填写替代文字可以帮助解释图表内容。",
    ),
    Question(
        id="excel-5",
        category=Category.EXCEL,
        prompt="若想一次性为多列添加统一的数字格式，应先怎么做？",
        options=[
            "逐列分别设置",
            "使用筛选功能",
            "先选中所有目标列再设置格式",
            "复制到Word中设置",
        ],
        correct_option=2,
        explanation="先选中需要设置的列，再统一设置数字格式可以节省时间并避免遗漏。",
    ),
    Question(
        id="excel-6",
        category=Category.EXCEL,
        prompt="Excel中使用快捷键复制单元格内容的组合键是？",
        options=["Ctrl+C", "Ctrl+V", "Ctrl+X", "Ctrl+Y"],
        correct_option=0,
        explanation="Ctrl+C是复制选中内容的标准快捷键。",
    ),
    Question(
        id="ppt-1",
        category=Category.POWERPOINT,
        prompt="在PowerPoint中要确保所有幻灯片使用统一样式，应编辑哪一项？",
        options=["幻灯片母版", "幻灯片备注", "放映计时", "动画窗格"],
        correct_option=0,
        explanation="通过幻灯片母版可以统一设置字体、颜色和版式。",
    ),
    Question(
        id="ppt-2",
        category=Category.POWERPOINT,
        prompt="为了让屏幕阅读器正确朗读幻灯片对象，应注意什么？",
        options=[
            "让对象按照正确的阅读顺序排列",
            "只使用背景图片",
            "隐藏所有文本框",
            "将所有内容转换为图片",
        ],
        correct_option=0,
        explanation="设置正确的阅读顺序可以让屏幕阅读器按照逻辑朗读内容。",
    ),
    Question(
        id="ppt-3",
        category=Category.POWERPOINT,
        prompt="在PowerPoint中添加音频描述的常见方式是？",
        options=[
            "在备注页编写说明并在放映中朗读",
            "增加动画数量",
            "把文字改成图片",
            "只使用表格",
        ],
        correct_option=0,
        explanation="在备注页编写说明可以为演讲者提供音频描述提示，方便盲人同学理解。",
    ),
    Question(
        id="ppt-4",
        category=Category.POWERPOINT,
        prompt="若想一次性更换全套幻灯片的配色方案，应使用哪项功能？",
        options=["设计主题", "动画方案", "放映设置", "视图切换"],
        correct_option=0,
        explanation="设计主题可以快速更换配色、字体等整体外观设置。",
    ),
    Question(
        id="ppt-5",
        category=Category.POWERPOINT,
        prompt="在插入图片或图形后，为了提高无障碍性应立即做什么？",
        options=[
            "设置动画",
            "添加替代文字",
            "设置艺术效果",
            "调整打印边距",
        ],
        correct_option=1,
        explanation="添加替代文字可以让看不到图片的同学了解其内容。",
    ),
    Question(
        id="ppt-6",
        category=Category.POWERPOINT,
        prompt="放映过程中若需要使用键盘跳转到下一张幻灯片，应按下哪一个键？",
        options=["N键或方向右键", "Esc键", "F1键", "Tab键"],
        correct_option=0,
        explanation="在放映模式下按N键或方向右键可以进入下一张幻灯片。",
    ),
)
