"""ToneScript to WAV Generator"""

from .core import ToneScriptParser, ToneGenerator
from .cli import main as cli_main
from .tester import main as tester_main

__version__ = "0.1.0"
__all__ = ["ToneScriptParser", "ToneGenerator", "cli_main", "tester_main"]
