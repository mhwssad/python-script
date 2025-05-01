TerminationMESSAGE = "操作被手动终止"


class CollectionError(Exception):
    """基类异常"""


class TerminationError(Exception):
    """手动终止异常"""


class CompressionError(Exception):
    """压缩/解压错误"""


class NotSoftware(Exception):
    """软件不存在"""


class InvalidPathError(CollectionError):
    """路径无效异常"""


class PermissionDeniedError(CollectionError):
    """权限异常"""


class CorruptedFileError(CollectionError):
    """文件损坏异常"""
