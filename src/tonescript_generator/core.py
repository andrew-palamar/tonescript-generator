#!/usr/bin/env python3
"""
ToneScript to WAV Generator - Core module
"""

import numpy as np
import soundfile as sf
import re
import os
from typing import List, Tuple, Optional, Dict, Any


class ToneScriptParser:
    """ToneScript format parser - extended version"""

    SAMPLE_RATE = 48000
    MAX_DURATION = 60.0  # Maximum duration for infinite tones

    def __init__(self, script: str):
        self.script = script.strip()
        self.components: List[Tuple[float, float]] = []
        self.sections: List[Dict[str, Any]] = []
        self.infinite_mode = False
        self.parse()

    def parse(self):
        """Main ToneScript parsing method"""
        try:
            # Split into components and sections
            parts = self.script.split(";")
            if len(parts) < 2:
                raise ValueError("Invalid ToneScript format: missing ';' separator")

            # Parse components
            self._parse_components(parts[0])

            # Parse sections
            sections_str = parts[1:]
            self._parse_sections(sections_str)

        except Exception as e:
            raise ValueError(f"Error parsing ToneScript '{self.script}': {e}")

    def _parse_components(self, components_str: str):
        """Parse frequency components"""
        component_pattern = r"(\d+(?:\.\d+)?)@(-?\d+(?:\.\d+)?)"
        matches = re.findall(component_pattern, components_str)

        if not matches:
            raise ValueError("No frequency components found")

        for freq_str, dbm_str in matches:
            freq = float(freq_str)
            dbm = float(dbm_str)
            self.components.append((freq, dbm))

    def _parse_sections(self, sections_str: List[str]):
        """Parse sections with '*' duration support"""

        for section_str in sections_str:
            section_str = section_str.strip()

            # Check for infinite section
            if section_str.startswith("*("):
                duration = float("inf")
                subsections_str = section_str[2:-1]  # Remove '*(' and ')'
                self.infinite_mode = True
            else:
                # Regular format: number(
                match = re.match(r"(\d+(?:\.\d+)?|\*)\(([^)]+)\)", section_str)
                if not match:
                    raise ValueError(f"Invalid section format: {section_str}")

                duration_str = match.group(1)
                duration = float("inf") if duration_str == "*" else float(duration_str)
                subsections_str = match.group(2)

            # Parse subsections
            subsections = self._parse_subsections(subsections_str)

            self.sections.append({"duration": duration, "subsections": subsections})

    def _parse_subsections(self, subsections_str: str) -> List[Dict[str, Any]]:
        """Parse subsections with component selection support"""
        subsections = []

        for subsection in subsections_str.split(","):
            sub_parts = subsection.split("/")
            if len(sub_parts) != 3:
                raise ValueError(f"Invalid subsection format: {subsection}")

            on_time_str, off_time_str, components_str = sub_parts

            # Parse timing
            on_time = float("inf") if on_time_str == "*" else float(on_time_str)
            off_time = 0.0 if off_time_str == "0" else float(off_time_str)

            # Parse components (supports formats: "1", "1+2", "0" for silence)
            component_indices = []
            if components_str and components_str != "0":
                for comp in components_str.split("+"):
                    if comp.strip():
                        idx = int(comp.strip()) - 1
                        if 0 <= idx < len(self.components):
                            component_indices.append(idx)

            subsections.append(
                {
                    "on_time": on_time,
                    "off_time": off_time,
                    "components": component_indices,  # Can be empty for silences
                }
            )

        return subsections

    def dbm_to_amplitude(self, dbm: float) -> float:
        """Convert dBm to amplitude"""
        vrms = 0.775 * (10 ** (dbm / 20))
        vpp = vrms * 2 * np.sqrt(2)
        amplitude = vpp / 2.0
        return amplitude * 0.5  # 6dB headroom


class ToneGenerator:
    """Tone generator - extended version"""

    def __init__(self, parser: ToneScriptParser):
        self.parser = parser
        self.sample_rate = parser.SAMPLE_RATE
        self.phase_state: Dict[Tuple[int, ...], float] = (
            {}
        )  # Store phase for continuity

    def generate_tone(self, duration: Optional[float] = None) -> np.ndarray:
        """Generate audio with complex pattern support"""

        if duration is None:
            # Determine total duration
            if self.parser.infinite_mode:
                duration = ToneScriptParser.MAX_DURATION
                print(f"Infinite mode, generating {duration} sec")
            else:
                duration = 0
                for section in self.parser.sections:
                    if section["duration"] == float("inf"):
                        duration += ToneScriptParser.MAX_DURATION
                    else:
                        duration += section["duration"]

        total_samples = int(duration * self.sample_rate)
        audio = np.zeros(total_samples)

        current_sample = 0
        section_index = 0

        while current_sample < total_samples and section_index < len(
            self.parser.sections
        ):
            section = self.parser.sections[section_index]

            # Section duration
            if section["duration"] == float("inf"):
                section_samples = total_samples - current_sample
            else:
                section_samples = int(section["duration"] * self.sample_rate)

            # Generate section
            section_audio = self._generate_section(section, section_samples)

            # Insert into main stream
            end_sample = min(current_sample + len(section_audio), total_samples)
            audio[current_sample:end_sample] = section_audio[
                : end_sample - current_sample
            ]

            current_sample = end_sample
            section_index += 1

        return audio

    def _generate_section(
        self, section: Dict[str, Any], num_samples: int
    ) -> np.ndarray:
        """Generate section with multiple subsections"""
        audio = np.zeros(num_samples)

        if not section["subsections"]:
            return audio

        current_pos = 0
        subsection_index = 0

        while current_pos < num_samples:
            subsection = section["subsections"][
                subsection_index % len(section["subsections"])
            ]

            # Convert time to samples
            if subsection["on_time"] == float("inf"):
                on_samples = num_samples - current_pos
            else:
                on_samples = int(subsection["on_time"] * self.sample_rate)

            off_samples = int(subsection["off_time"] * self.sample_rate)

            # Generate signal for on-phase
            if on_samples > 0 and current_pos < num_samples:
                # Limit number of samples
                actual_on_samples = min(on_samples, num_samples - current_pos)

                if subsection["components"]:
                    # Generate tone for active components
                    tone_audio = self._generate_components_tone(
                        subsection["components"],
                        actual_on_samples / self.sample_rate,
                        start_phase=self.phase_state.get(
                            tuple(subsection["components"]), 0
                        ),
                    )

                    end_pos = min(current_pos + actual_on_samples, num_samples)
                    audio[current_pos:end_pos] = tone_audio[: end_pos - current_pos]

                current_pos += actual_on_samples

            # Skip off-phase
            current_pos += off_samples
            subsection_index += 1

        return audio

    def _generate_components_tone(
        self, component_indices: List[int], duration: float, start_phase: float = 0.0
    ) -> np.ndarray:
        """Generate tone from specified components"""
        samples = int(duration * self.sample_rate)
        if samples == 0:
            return np.array([])

        t = np.linspace(0, duration, samples, endpoint=False)
        audio = np.zeros(samples)

        for idx in component_indices:
            if idx < len(self.parser.components):
                freq, dbm = self.parser.components[idx]
                amplitude = self.parser.dbm_to_amplitude(dbm)

                # Generate sine wave with phase consideration
                tone = amplitude * np.sin(2 * np.pi * freq * t + start_phase)
                audio += tone

        return audio
