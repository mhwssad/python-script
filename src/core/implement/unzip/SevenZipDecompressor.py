from typing import List

from py7zr import DecompressionError

from src.core.interfaces.unzip_interfaces import DecompressionTool


class SevenZipDecompressor(DecompressionTool):
    """7z解压工具实现类"""

    def __init__(self):
        super().__init__()
        self.delete = False

    def set_delete_after_extraction(self, delete: bool) -> 'SevenZipDecompressor':
        """设置解压后是否删除原文件"""
        self.delete = delete
        return self

    def _build_command(self) -> List[str]:
        """构建7z解压命令"""
        if not self._config.input_path:
            raise DecompressionError("未指定输入文件")
        if not self._config.output_path:
            raise DecompressionError("未指定输出目录")

        cmd = ["7z", "x", "-y"]
        if self.delete:
            cmd.append("-sdel")
        if self._config.password:
            cmd.extend(["-p" + self._config.password])

        cmd.extend([str(self._config.input_path), "-o" + str(self._config.output_path)])
        self.log.info(f"构建命令：{cmd}")

        return cmd


if __name__ == '__main__':
    decompressor = SevenZipDecompressor()
    decompressor.set_input_path("D:\\test.zip").set_password("123456").set_output_path("D:\\test.txt")
    decompressor._build_command()
