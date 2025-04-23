from typing import List

from src.core.interfaces.unzip_interfaces import CompressionTool
from src.exceptions.unzip_excepotion import CompressionError


class BandizipCompressor(CompressionTool):

    def _build_command(self) -> List[str]:
        """构建Bandizip压缩命令

        Returns:
            List[str]: 构建好的命令列表

        Raises:
            CompressionError: 当缺少必要参数时抛出
        """
        if not self._config.output_path:
            raise CompressionError("未指定输出路径")
        if not self._config.input_path:
            raise CompressionError("未添加压缩文件")

        cmd = ["bandizip", "a", "-y", "-storeroot:yes"]

        if self._config.password:
            cmd.append(f"-p:{self._config.password}")

        if self._config.volume:
            cmd.append(f"-v{self.config.volume}")

        if self._config.compression_type:
            cmd.append(f"-fmt:{self._config.compression_type}")

        cmd.append(self._config.output_path)
        cmd.append(self._config.input_path)
        self.log.info("构建命令：" + " ".join(cmd))
        return cmd

if __name__ == '__main__':
    compressor = BandizipCompressor()
    compressor.set_input_path("D:\\test.txt")\
        .set_password("123456")\
        .set_output_path("D:\\test.zip")\
        .set_volume(100).set_compression_type("7z")
    compressor._build_command()
