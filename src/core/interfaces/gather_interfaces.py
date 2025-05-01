from logging import WARNING
from abc import ABC, abstractmethod
from pathlib import Path
from queue import Queue
from typing import Union, Optional

from magika import magika

from config.gather_config import COMPRESS
from config.unzip_cinfig import log_file
from src.enumerate.gather_enum import Mode
from src.utils.LogDecorator import LogDecorator


class GatherInterfaces(ABC):
    log = LogDecorator(__name__, level=WARNING, logfile=log_file)

    def __init__(self, queue: Queue, path: Optional[Union[Path, str]] = None, types: set = COMPRESS):
        self.queue = queue
        self.path = self._validate_path(path)
        self.type = types
        self.__magika_obj = magika.Magika()
        self._should_stop = False  # 新增停止标志

    def set_type(self, types: set):
        self.type = types

    def get_type(self) -> set:
        return self.type

    def set_path(self, path: Union[Path, str]):
        self.path = self._validate_path(path)

    def get_path(self) -> Path:
        return self.path

    def get_type_name(self, path: Path) -> str:
        """
        获取文件类型。
        :param path: 文件路径。
        :return: 文件类型字符串。
        @rtype: object
        """
        try:
            file_type = self.__magika_obj.identify_path(path)
            return file_type.dl.ct_label
        except magika.MagikaError as e:
            raise RuntimeError(f"识别文件类型失败，错误原因：{e}")

    @staticmethod
    def _validate_path(path: Union[Path, str]) -> Path:
        """验证路径有效性并返回Path对象"""
        path_obj = path
        if isinstance(path, str):
            path_obj = Path(path)
            if not path_obj.exists():
                raise FileNotFoundError(f"路径不存在: {path}")
            return path_obj
        return path_obj

    @abstractmethod
    def start_collection(self) -> None:
        """启动文件收集的抽象方法"""
        pass

    def get_collection(self):
        while not self.queue.empty():
            yield self.queue.get()

    def stop_collection(self) -> None:
        """设置停止标志，安全终止收集过程"""
        self._should_stop = True

    @classmethod
    def check_directory_content(cls, directory: Path, mode: Mode = Mode.ALL) -> bool:
        """检查目录内容是否符合指定模式"""
        if not directory.is_dir():
            raise ValueError(f"无效的目录路径: {directory}")

        has_files = False
        has_dirs = False

        for item in directory.iterdir():
            if item.is_file():
                has_files = True
            elif item.is_dir():
                has_dirs = True

            # 模式冲突立即返回
            if (mode == Mode.FILE and has_dirs) or (mode == Mode.DIR and has_files):
                return False

        # 根据模式返回结果
        if mode == Mode.ALL:
            return has_files or has_dirs
        return (mode == Mode.FILE and has_files) or (mode == Mode.DIR and has_dirs)
