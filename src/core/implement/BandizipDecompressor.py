from typing import List

from py7zr import DecompressionError

from src.core.interfaces.unzip_interfaces import DecompressionTool


class BandizipDecompressor(DecompressionTool):
    """Bandizip解压工具实现类"""

    def __init__(self):
        super().__init__()
        self._delete_after_extraction = False

    def set_delete_after_extraction(self, delete: bool) -> 'BandizipDecompressor':
        """设置解压后是否删除原压缩文件

        Args:
            delete: 是否删除原文件

        Returns:
            BandizipDecompressor: 返回自身以支持链式调用
        """
        self._delete_after_extraction = delete
        return self

    def _build_command(self) -> List[str]:
        """构建Bandizip解压命令

        Returns:
            List[str]: 构建好的命令列表

        Raises:
            DecompressionError: 当缺少必要参数时抛出
        """
        if not self._config.input_path:
            raise DecompressionError("未指定输入文件")
        if not self._config.output_path:
            raise DecompressionError("未指定输出目录")

        cmd = ["bandizip", "x", "-y"]

        if self._delete_after_extraction:
            cmd.append("-d")
        if self._config.password:
            cmd.append(f"-p:{self._config.password}")

        cmd.extend([
            str(self._config.input_path),
            "-o:" + str(self._config.output_path)
        ])

        self.log.info("构建命令：" + " ".join(cmd))
        return cmd

if __name__ == '__main__':
    decompressor = BandizipDecompressor()
    decompressor.set_input_path("D:\\test.zip")\
        .set_password("123456")\
        .set_output_path("D:\\test.txt")
    decompressor._build_command()