"""
various small functions that should eventually go in a better place
"""

# TODO: make OS specific versions of this. also have more customizability?
# e.g. set a replacement map[chr,chr] + in some (non-path) contexts may not need to do a replacement
def make_str_pathsafe(s: str) -> str:
    """convert a string to one that is pathsafe"""
    return s.replace(' ', '_').replace('/', '_').replace('\\', '_').replace(':', '_').replace('?', '_').replace('*', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')



from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Generator
import os
import sys

@contextmanager
def move_to_isolated_dir(dirname:str='workdir_{timestamp}', delete_empty:bool=True) -> Generator[None, None, None]:
    """
    Context to create a unique isolated directory for working in, and move cd into it (and exit on context end)

    Args:
        prefix (str): Prefix for the directory name. A timestamp will be appended to this prefix.
    """
    # save the original directory
    original_dir = Path.cwd()
    
    try:
        # create and move to the isolated directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dirname = dirname.format(timestamp=timestamp)
        
        isolated_dir = Path(dirname)
        isolated_dir.mkdir(exist_ok=True, parents=True)
        os.chdir(isolated_dir)
        yield

    finally:
        # return to the original directory
        os.chdir(original_dir)

        # Optionally, remove the isolated directory if empty
        if not os.listdir(isolated_dir) and delete_empty:
            os.rmdir(isolated_dir)
