#!/usr/bin/env python3
"""
CLI interface for ToneScript generator
"""

import argparse
import os
import sys
import numpy as np
import soundfile as sf
from .core import ToneScriptParser, ToneGenerator


def main():
    parser = argparse.ArgumentParser(
        description="WAV generator from ToneScript",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "350@-19,440@-19;10(*/0/1+2)" output/dial_tone.wav
  %(prog)s "480@-19,620@-19;10(.5/.5/1+2)" output/busy.wav --duration 5.0
        """,
    )
    parser.add_argument("script", type=str, help="ToneScript string")
    parser.add_argument("output", type=str, help="Output WAV file")
    parser.add_argument(
        "--duration", type=float, help="Duration in seconds (optional)", default=None
    )

    args = parser.parse_args()

    try:
        # Parse script
        parser_script = ToneScriptParser(args.script)
        generator = ToneGenerator(parser_script)

        # Generate audio
        audio = generator.generate_tone(args.duration)

        # Normalize
        max_amp = np.max(np.abs(audio))
        if max_amp > 1.0:
            audio = audio / max_amp * 0.95

        # Create directory if needed
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save
        sf.write(args.output, audio, parser_script.SAMPLE_RATE, subtype="PCM_16")
        print(f"✅ WAV file saved: {args.output}")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
