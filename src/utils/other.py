from src.enumerate.unzip_enum import BandiZipUnit, WinRarUnit


class OtherTool:

    @staticmethod
    def suffix_to_bytes(bytes_str: str):
        if bytes_str == "SevenZipCompressor":
            return BandiZipUnit
        else:
            return WinRarUnit

    @staticmethod
    def format_size(size_bytes, bytes_str: str):
        enum_unit = OtherTool.suffix_to_bytes(bytes_str)
        if size_bytes < 1024:
            return f"{size_bytes}{enum_unit.K.value}"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f}{enum_unit.KB.value}"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.2f}{enum_unit.MB.value}"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f}{enum_unit.GB.value}"
