
TerminationMESSAGE = "操作被手动终止"


class TerminationError(Exception):
    """手动终止异常"""
    pass


class CompressionError(Exception):
    """压缩/解压错误"""
    pass

class NotSoftware(Exception):
    """软件不存在"""
    pass