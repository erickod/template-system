import asyncio
import os
from pathlib import Path
from typing import Callable


async def remove_file(
    path: str | Path,
    time_in_seconds: int = 300,
    remover: Callable = os.remove,
) -> None:
    """
    Remove or delete a path if it exists
    """

    path_str = str(path)
    if not Path(str(path)).exists:
        return
    await asyncio.sleep(time_in_seconds)
    remover(path_str)
    print(f">> Removed path {path_str}")
