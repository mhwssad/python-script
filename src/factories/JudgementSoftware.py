import shlex
import subprocess

from config.unzip_cinfig import path_test
from src.core.implement.BandizipCompressor import BandizipCompressor
from src.core.implement.BandizipDecompressor import BandizipDecompressor
from src.core.implement.SevenZipCompressor import SevenZipCompressor
from src.core.implement.SevenZipDecompressor import SevenZipDecompressor
from src.core.implement.WinRarCompressor import WinRarCompressor
from src.core.implement.WinRarDecompressor import WinRarDecompressor
from src.core.interfaces.unzip_interfaces import CompressionTool, DecompressionTool
from src.exceptions.unzip_excepotion import NotSoftware


class JudgementSoftware:
    def __init__(self):

        self._command = [f'bandizip  t -y "{path_test}"', "rar", "7z"]

    @staticmethod
    def _get_compressor(command: str):
        if command == "7z":
            return SevenZipCompressor()
        elif command == "rar":
            return WinRarCompressor()
        elif command == f'bandizip  t -y "{path_test}"':
            return BandizipCompressor()

    @staticmethod
    def _get_decompressor(command: str):
        if command == "7z":
            return SevenZipDecompressor()
        elif command == "rar":
            return WinRarDecompressor()
        elif command == f'bandizip  t -y "{path_test}"':
            return BandizipDecompressor()

    @staticmethod
    def judgement(command) -> dict:
        try:
            command_list = shlex.split(command)
            subprocess.run(command_list, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return {"success": True, "error": None}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": str(e)}
        except OSError as e:
            return {"success": False, "error": str(e)}
        except ValueError as e:
            return {"success": False, "error": str(e)}

    def judgement_compressor(self) -> CompressionTool:
        for command in self._command:
            if self.judgement(command)["success"]:
                return self._get_compressor(command)
        raise NotSoftware("没有安装压缩软件")

    def judgement_decompressor(self) -> DecompressionTool:
        for command in self._command:
            result = self.judgement(command)
            if result["success"]:
                return self._get_decompressor(command)
        raise NotSoftware("没有安装压缩软件")

    def __str__(self):
        return f"{self.__class__.__name__}"


if __name__ == '__main__':
    judgement = JudgementSoftware()
    print(judgement.judgement_compressor())
