from typing import List

from src.core.interfaces.unzip_interfaces import CompressionTool
from src.exceptions.unzip_excepotion import CompressionError


class SevenZipCompressor(CompressionTool):
    def __init__(self, max_workers: int = 4):
        super().__init__(max_workers)
        self.delete_after_compression = False  # 压缩后删除源文件标志

    def set_delete_after_compression(self, delete: bool):
        """设置压缩后是否删除源文件"""
        self.delete_after_compression = delete
        return self

    def _build_command(self) -> List[str]:
        """构建7z压缩命令"""
        if not self.config.output_path:
            raise CompressionError("未指定输出路径")
        if not self.config.input_path:
            raise CompressionError("未添加压缩文件")

        command = ["7z", "a", "-y"]

        # 添加密码选项
        if self.config.password:
            command.extend(["-p" + self.config.password])

        # 添加分卷选项
        if self.config.volume:
            command.extend(["-v" + f"{self.config.volume}"])

        # 添加压缩后删除源文件选项
        if self.delete_after_compression:
            command.append("-sdel")

        # 添加压缩类型
        command.append(f"-t{self.config.compression_type}")

        # 添加输出路径
        command.append(str(self.config.output_path))

        # 添加输入文件/目录
        input_paths = self.config.input_path if isinstance(self.config.input_path, list) else [self.config.input_path]
        for path in input_paths:
            command.append(str(path))

        self.log.info(f"构建7z命令: {' '.join(command)}")
        return command


if __name__ == '__main__':
    compressor = SevenZipCompressor()
    compressor.set_input_path("D:\\test.txt")\
        .set_password("123456")\
        .set_output_path("D:\\test.zip")\
        .set_volume(100).set_compression_type("zip")
    compressor._build_command()
