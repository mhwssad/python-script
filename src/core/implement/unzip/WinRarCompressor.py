from typing import List

from src.core.interfaces.unzip_interfaces import CompressionTool
from src.exceptions.unzip_excepotion import CompressionError


class WinRarCompressor(CompressionTool):
    def __init__(self):
        super().__init__()
        self.delete = False

    def set_delete_after_compression(self, delete: bool) -> 'WinRarCompressor':
        """设置压缩后是否删除原文件

        Args:
            delete: 是否删除原文件

        Returns:
            WinRarCompressor: 返回自身以支持链式调用
        """
        self.delete = delete
        return self

    def _build_command(self) -> List[str]:
        """构建WinRAR压缩命令

        Returns:
            List[str]: 构建好的命令列表

        Raises:
            CompressionError: 当缺少必要参数时抛出
        """
        if not self._config.output_path:
            raise CompressionError("未指定输出路径")
        if not self._config.input_path:
            raise CompressionError("未添加压缩文件")

        command = ["winrar", "a", "-y", "-ep1"]

        if self._config.password:
            command.append("-p" + self._config.password)

        if self._config.volume:
            command.append("-v" + self.config.volume)

        if self.delete:
            command.append("-df")

        command.append(f"{str(self._config.output_path)}")
        command.append(self._config.input_path)

        self.log.info(f"构建命令：{command}")
        return command

if __name__ == '__main__':
    compressor = WinRarCompressor()
    compressor.set_input_path("D:\\test.txt").set_password("123456")\
        .set_output_path("D:\\test.zip").set_compression_type("zip").set_volume(10000)
    compressor._build_command()