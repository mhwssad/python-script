from enum import auto, Enum


class Mode(Enum):
    """
    枚举类，用于指定获取内容的模式。
    - FILE: 仅获取文件。
    - DIR: 仅获取目录。
    - ALL: 获取所有内容（文件和目录）。
    """
    FILE = auto()
    DIR = auto()
    ALL = auto()
