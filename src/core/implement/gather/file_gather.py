from pathlib import Path

from src.core.interfaces.gather_interfaces import GatherInterfaces
from src.enumerate.gather_enum import Mode


class FileGather(GatherInterfaces):

    def start_collection(self) -> None:
        self._should_stop = False  # 重置标志
        target_path: Path = self.get_path()
        if target_path is None:
            raise ValueError("文件路径未设置")
        if target_path.is_file():
            self._process_single(target_path)
        elif target_path.is_dir():
            self._process_directory(target_path)

    def _process_single(self, file_path: Path) -> None:
        """处理单个文件"""
        file_type = self.get_type_name(file_path)
        if file_type in self.type:
            self.queue.put((file_path, file_type))
            self.log.info(f"{file_path} 添加到队列中")

    def _process_directory(self, directory: Path) -> None:
        """智能目录处理器"""
        if self._should_stop:
            return
        try:
            if self.check_directory_content(directory, Mode.DIR):
                self._handle_pure_dir(directory)
            elif self.check_directory_content(directory, Mode.FILE):
                self._collect_files(directory)
        except ValueError as e:
            print(f"跳过无效目录: {e}")

    def _handle_pure_dir(self, directory: Path) -> None:
        """处理纯目录结构"""
        for item in directory.iterdir():
            if self._should_stop:
                return
            if item.is_dir():
                self._process_directory(item)  # 递归处理子目录

    def _collect_files(self, directory: Path) -> None:
        """收集纯文件目录"""
        file_groups = {}  # 文件名分组: {name: [files]}
        has_target_files = set()  # 包含目标文件的分组名

        for item in directory.iterdir():
            if self._should_stop:  # 关键停止点
                break
            # 确保只处理文件
            if not item.is_file():
                continue

            # 获取文件类型
            try:
                fctype = self.get_type_name(item)
            except Exception as e:
                self.log.error(f"文件类型识别失败: {item}, 错误: {e}")
                continue

            # 提取主文件名
            item_name = item.stem.split(".", 1)[0]

            # 初始化分组
            if item_name not in file_groups:
                file_groups[item_name] = []

            # 添加文件到分组
            file_groups[item_name].append((item, fctype))

            # 标记目标文件分组
            if fctype in self.type:
                has_target_files.add(item_name)

        # 仅保留含目标文件的分组
        valid_groups = {
            name: files
            for name, files in file_groups.items()
            if name in has_target_files
        }
        if self._should_stop:
            return  # 停止收集
        # 加入队列
        for group in valid_groups.values():
            self.queue.put(group)
            self.log.info(f"分组入队: {[f[0].name for f in group]}")


if __name__ == '__main__':
    from queue import Queue

    fp = r"E:\下载文件\百度网盘下载文件\15"
    fg = FileGather(Queue(), fp)
    fg.start_collection()
    list_name = []
    for i in fg.get_collection():
        for j in i:
            list_name.append(j)
    print(len(list_name))
