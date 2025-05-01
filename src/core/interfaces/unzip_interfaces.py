import asyncio
import subprocess
import threading
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import List, Union

from config.unzip_cinfig import log_file
from src.exceptions.unzip_excepotion import CompressionError, TerminationError, TerminationMESSAGE
from src.models.ToolConfig import ToolConfig
from src.utils.LogDecorator import LogDecorator
from src.utils.other import OtherTool


class BaseExecutor(ABC):
    """命令执行基类"""
    log = LogDecorator(name=__name__, console=False, logfile=str(log_file))

    def __init__(self, max_workers: int = 4):
        self.current_process: Union[subprocess.Popen, asyncio.subprocess.Process, None] = None  # 当前子进程
        self._manually_terminated = False  # 新增手动终止标记
        self._process_lock = threading.Lock()  # 用于保护current_process的线程安全
        self.thread_executor = ThreadPoolExecutor(max_workers=max_workers)  # 线程池

    def _run_command(self, command: List[str]) -> str:
        """同步执行命令（支持静默手动终止）"""
        try:
            with self._process_lock:
                self._manually_terminated = False  # 重置状态
                self.current_process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    encoding="gbk",
                    errors="replace"
                )

            stdout, stderr = self.current_process.communicate()

            # 手动终止时跳过错误检查
            if self._manually_terminated:
                raise TerminationError("终止")

            # 正常错误处理
            if self.current_process.returncode != 0:
                error_msg = f"命令执行失败，返回码：{self.current_process.returncode}"
                if stderr.strip():
                    error_msg += f"\n错误信息：{stderr.strip()}"
                raise CompressionError(error_msg)

            return stdout.strip()

        except FileNotFoundError as e:
            raise CompressionError(f"找不到命令：{command[0]}") from e
        except subprocess.SubprocessError as e:
            if self._manually_terminated:
                raise TerminationError("终止")
            else:
                raise CompressionError("子进程执行错误") from e
        finally:
            with self._process_lock:
                self.current_process = None

    async def _async_run_command(self, command: List[str]) -> str:
        """异步执行命令"""
        try:
            with self._process_lock:
                self._manually_terminated = False  # 重置状态
                self.current_process = await asyncio.create_subprocess_exec(
                    *command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

            stdout, stderr = await self.current_process.communicate()

            # 手动终止时跳过错误检查
            if self._manually_terminated:
                raise TerminationError("终止")

            if self.current_process.returncode != 0:
                error_msg = f"命令执行失败，返回码：{self.current_process.returncode}"
                if stderr:
                    decoded_stderr = stderr.decode('gbk', errors='replace').strip()
                    error_msg += f"\n错误信息：{decoded_stderr}"
                raise CompressionError(error_msg)

            return stdout.decode('gbk', errors='replace').strip()

        except FileNotFoundError as e:
            raise CompressionError(f"找不到命令：{command[0]}") from e
        except subprocess.SubprocessError as e:
            if self._manually_terminated:
                raise TerminationError("终止")
            else:
                raise CompressionError("子进程执行错误") from e
        finally:
            with self._process_lock:
                self.current_process = None

    def _run_in_thread(self, command: List[str]):
        """
        在线程中运行命令（多线程执行）

        :param command: 命令列表
        :return: 返回一个 Future 对象，可以通过 result() 获取结果
        """
        return self.thread_executor.submit(self._run_command, command)

    def terminate_process(self):
        """终止进程并标记为手动终止"""
        with self._process_lock:
            if self.current_process is not None:
                try:
                    self._manually_terminated = True  # 标记为手动终止
                    if isinstance(self.current_process, subprocess.Popen):
                        self.current_process.terminate()
                        try:
                            self.current_process.wait(timeout=1)  # 等待进程结束
                        except subprocess.TimeoutExpired:
                            self.current_process.kill()
                            self.current_process.wait()
                    elif isinstance(self.current_process, asyncio.subprocess.Process):
                        self.current_process.terminate()
                except ProcessLookupError:
                    pass  # 进程已结束无需处理
                except Exception as e:
                    self.log.error(f"终止进程时发生非致命错误：{e}")


class BaseTool(BaseExecutor, ABC):
    """工具基类，提供配置管理"""

    def __init__(self, max_workers: int = 4):
        super().__init__(max_workers)
        self._config = ToolConfig()

    @property
    def config(self) -> ToolConfig:
        """获取配置对象(只读)"""
        return self._config

    def set_password(self, password: str) -> 'BaseTool':
        """设置密码"""
        self._config.password = password
        return self

    def set_input_path(self, input_path: str) -> 'BaseTool':
        """设置输入路径"""
        self._config.input_path = input_path
        return self

    def set_output_path(self, output_path: str) -> 'BaseTool':
        """设置输出路径"""
        self._config.output_path = output_path
        return self

    @abstractmethod
    def _build_command(self) -> List[str]:
        """构建命令(子类必须实现)"""
        pass

    def execute(self) -> str:
        """同步执行"""
        return self._run_command(self._build_command())

    async def async_execute(self) -> str:
        """异步执行"""
        return await self._async_run_command(self._build_command())

    def thread_execute(self):
        """多线程执行"""
        return self._run_in_thread(self._build_command())

    def __str__(self) -> str:
        return self.__class__.__name__


class CompressionTool(BaseTool, ABC):
    """压缩工具基类"""

    def set_compression_type(self, compression_type: str) -> 'CompressionTool':
        """设置压缩类型"""
        self._config.compression_type = compression_type
        return self

    def set_volume(self, volume: int) -> 'CompressionTool':
        """设置分卷大小(MB)"""
        if volume <= 0:
            raise ValueError("分卷大小必须大于0")
        self._config.volume = OtherTool.format_size(volume, self.__class__.__name__)
        return self


class DecompressionTool(BaseTool, ABC):
    """解压工具基类"""
    pass
