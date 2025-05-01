from pathlib import Path

from src.core.interfaces.gather_interfaces import GatherInterfaces
from src.enumerate.gather_enum import Mode


class DirectoryGather(GatherInterfaces):
    def start_collection(self) -> None:
        target_path = self.get_path()
        if not target_path:
            raise ValueError("文件路径未设置")
        if self._should_stop:
            return

        if target_path.is_file():
            raise ValueError("当前方法只能处理目录")
        elif target_path.is_dir():
            self._process_directory(target_path)

    def _process_directory(self, directory: Path) -> None:
        """智能目录处理器"""
        if self._should_stop:
            return
        try:
            if self.check_directory_content(directory, Mode.DIR):
                self._handle_pure_dir(directory)
            elif self.check_directory_content(directory, Mode.ALL):
                self.queue.put(Path(directory))
        except ValueError as e:
            self.log.info(f"跳过无效目录: {e}")

    def _handle_pure_dir(self, directory: Path) -> None:
        """处理纯目录结构"""
        for item in directory.iterdir():
            if self._should_stop:
                return
            if item.is_dir():
                self._process_directory(item)  # 递归处理子目录


if __name__ == '__main__':
    from queue import Queue

    fp = r"E:\下载文件\百度网盘下载文件\15"
    fg = DirectoryGather(Queue(), fp)
    fg.start_collection()
    list_name = []
    for i in fg.get_collection():
        list_name.append(i)
        print(i)
    print(len(list_name))
