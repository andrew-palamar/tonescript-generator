#!/usr/bin/env python3
"""
Tester for all standard telephone tones
"""

import os
import sys
import numpy as np
import soundfile as sf
from .core import ToneScriptParser, ToneGenerator


# Dictionary with all tones
TONES = {
    "Dial_tone": "350@-19,440@-19;10(*/0/1+2)",
    "Second_dial_tone": "420@-19,520@-19;10(*/0/1+2)",
    "Outside_dial_tone": "420@-16;10(*/0/1)",
    "Prompt_tone": "520@-19,620@-19;10(*/0/1+2)",
    "Busy_tone": "480@-19,620@-19;10(.5/.5/1+2)",
    "Reorder_tone": "480@-19,620@-19;10(.25/.25/1+2)",
    "Howler_tone": "480@-10,620@0;10(.125/.125/1+2)",
    "Ringback_tone": "440@-19,480@-19;*(2/4/1+2)",
    "Comfort_tone": "600@-16;1(.25/.25/1)",
    "SIT1": "985@-16,1428@-16,1777@-16;20(.380/0/1,.380/0/2,.380/0/3,0/4/0)",
    "SIT2": "914@-16,1371@-16,1777@-16;20(.274/0/1,.274/0/2,.380/0/3,0/4/0)",
    "SIT3": "914@-16,1371@-16,1777@-16;20(.380/0/1,.380/0/2,.380/0/3,0/4/0)",
    "SIT4": "985@-16,1371@-16,1777@-16;20(.380/0/1,.274/0/2,.380/0/3,0/4/0)",
    "MWI_Dial_Tone": "350@-19,440@-19;2(.1/.1/1+2);10(*/0/1+2)",
    "Call_Forward_Dial_Tone": "350@-19,440@-19;2(.2/.2/1+2);10(*/0/1+2)",
    "Holding_tone": "600@-19;*(.1/.1/1,.1/.1/1,.1/9.5/1)",
    "Conference_call_Tone": "350@-19;20(.1/.1/1,.1/9.7/1)",
    "Call_waiting_tone": "440@-10;30(.3/9.7/1)",
}


def normalize_filename(name: str) -> str:
    """Convert name to filename"""
    return name.replace(" ", "_") + ".wav"


def generate_tone(
    name: str, script: str, output_dir: str, duration: float = 3.0
) -> bool:
    """Generate a single tone"""
    try:
        parser = ToneScriptParser(script)
        generator = ToneGenerator(parser)

        # Special duration for some tones
        if "Ringback" in name:
            duration = 6.0
        elif "SIT" in name:
            duration = 4.0

        # Generate audio
        audio = generator.generate_tone(duration=duration)

        # Normalize
        max_amp = np.max(np.abs(audio))
        if max_amp > 1.0:
            audio = audio / max_amp * 0.95

        # Save
        filepath = os.path.join(output_dir, f"{name}.wav")
        sf.write(filepath, audio, parser.SAMPLE_RATE, subtype="PCM_16")

        return True
    except Exception as e:
        print(f"   ❌ {name}: {e}")
        return False


def main():
    """Main tester function"""
    print("=" * 60)
    print("🧪 Generating all standard telephone tones")
    print("=" * 60)

    # Create output directory
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created directory: {output_dir}")

    # Generate tones
    success = 0
    total = len(TONES)

    for i, (name, script) in enumerate(TONES.items(), 1):
        print(f"\n[{i}/{total}] 📞 {name}")
        print(f"   Script: {script}")

        if generate_tone(name, script, output_dir):
            print(f"   ✅ Saved: {output_dir}/{name}.wav")
            success += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"📊 RESULTS:")
    print(f"   ✅ Successful: {success}")
    print(f"   ❌ Failed: {total - success}")
    print(f"   📁 Directory: {os.path.abspath(output_dir)}")
    print("=" * 60)

    return 0 if success == total else 1


if __name__ == "__main__":
    sys.exit(main())
