from contextlib import contextmanager
from typing import Callable, Any, Generator
import sys



# Define a helper class that acts like a file-like object
class WriteRedirector:
    """
    A file-like object that redirects writes to a callable,
    temporarily restoring original stdout during the call.
    """
    def __init__(self, write_func: Callable[[str], Any], original_stdout: Any):
        self.write_func = write_func
        self.original_stdout = original_stdout # Keep track of the original

    def write(self, data: str):
        # --- Critical Section ---
        # Store the current redirector (self)
        current_stdout = sys.stdout
        try:
            # Temporarily set stdout back to the original
            sys.stdout = self.original_stdout
            # Call the user's write function (e.g., tqdm.write)
            # This function can now safely write to the real stdout
            self.write_func(data)
        finally:
            # ALWAYS restore our redirector, even if write_func fails
            sys.stdout = current_stdout
        # --- End Critical Section ---

    def flush(self):
        # You might want the flush to go to the original stdout as well,
        # though tqdm.write usually handles its own flushing.
        # If needed:
        # current_stdout = sys.stdout
        # try:
        #     sys.stdout = self.original_stdout
        #     # Optionally call flush on the original if the write_func needs it
        #     getattr(self.original_stdout, 'flush', lambda: None)()
        # finally:
        #     sys.stdout = current_stdout
        pass # Often sufficient for tqdm.write

@contextmanager
def redirect_stdout(write_func: Callable[[str], Any]) -> Generator[None, None, None]:
    """
    Context manager to capture stdout and redirect it to a write function
    in real-time, preventing recursion errors.

    Args:
        write_func: A callable that takes a single string argument
                    (like tqdm.write).
    """
    original_stdout = sys.stdout
    # Pass the original stdout to the redirector
    redirector = WriteRedirector(write_func, original_stdout)
    sys.stdout = redirector  # Redirect stdout
    try:
        yield  # Allow code within the 'with' block to run
    finally:
        sys.stdout = original_stdout # Restore original stdout fully on exit


