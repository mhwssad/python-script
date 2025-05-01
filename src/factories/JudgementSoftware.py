import shlex
import subprocess
from abc import ABC, abstractmethod
from typing import List, Type

from config.unzip_cinfig import path_test
from src.core.implement.BandizipCompressor import BandizipCompressor
from src.core.implement.BandizipDecompressor import BandizipDecompressor
from src.core.implement.SevenZipCompressor import SevenZipCompressor
from src.core.implement.SevenZipDecompressor import SevenZipDecompressor
from src.core.implement.WinRarCompressor import WinRarCompressor
from src.core.implement.WinRarDecompressor import WinRarDecompressor
from src.core.interfaces.unzip_interfaces import CompressionTool, DecompressionTool
from src.exceptions.unzip_excepotion import NotSoftware


class CompressionToolFactory(ABC):
    @classmethod
    @abstractmethod
    def is_available(cls) -> bool:
        pass

    @abstractmethod
    def create_compressor(self) -> CompressionTool:
        pass

    @abstractmethod
    def create_decompressor(self) -> DecompressionTool:
        pass


class BandizipFactory(CompressionToolFactory):
    @classmethod
    def is_available(cls) -> bool:
        command = f'bandizip t -y "{path_test}"'
        return JudgementSoftware.judgement(command)["success"]

    def create_compressor(self) -> CompressionTool:
        return BandizipCompressor()

    def create_decompressor(self) -> DecompressionTool:
        return BandizipDecompressor()


class SevenZipFactory(CompressionToolFactory):
    @classmethod
    def is_available(cls) -> bool:
        command = "7z"
        return JudgementSoftware.judgement(command)["success"]

    def create_compressor(self) -> CompressionTool:
        return SevenZipCompressor()

    def create_decompressor(self) -> DecompressionTool:
        return SevenZipDecompressor()


class WinRarFactory(CompressionToolFactory):
    @classmethod
    def is_available(cls) -> bool:
        command = "rar"
        return JudgementSoftware.judgement(command)["success"]

    def create_compressor(self) -> CompressionTool:
        return WinRarCompressor()

    def create_decompressor(self) -> DecompressionTool:
        return WinRarDecompressor()


class CompressionToolFactorySelector:
    _factories: List[Type[CompressionToolFactory]] = [
        BandizipFactory,
        SevenZipFactory,
        WinRarFactory
    ]

    @classmethod
    def select_factory(cls) -> CompressionToolFactory:
        for factory in cls._factories:
            if factory.is_available():
                return factory()
        raise NotSoftware("No available compression software found.")


class JudgementSoftware:
    def __init__(self):
        self._factory = CompressionToolFactorySelector.select_factory()

    @staticmethod
    def judgement(command: str) -> dict:
        try:
            command_list = shlex.split(command)
            subprocess.run(
                command_list,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return {"success": True, "error": None}
        except (subprocess.CalledProcessError, OSError, ValueError) as e:
            return {"success": False, "error": str(e)}

    def judgement_compressor(self) -> CompressionTool:
        return self._factory.create_compressor()

    def judgement_decompressor(self) -> DecompressionTool:
        return self._factory.create_decompressor()

    def __str__(self):
        return f"{self.__class__.__name__}"


if __name__ == '__main__':
    judgement = JudgementSoftware()
    print(judgement.judgement_compressor())
    print(judgement.judgement_decompressor())
