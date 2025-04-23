from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union


@dataclass
class ToolConfig:
    password: Optional[str] = None
    input_path: Optional[Union[str, Path]] = None
    output_path: Optional[Union[str, Path]] = None
    compression_type: Optional[str] = "7z"
    volume: Optional[str] = None
