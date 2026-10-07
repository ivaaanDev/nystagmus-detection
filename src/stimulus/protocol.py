from dataclasses import dataclass


@dataclass(frozen=True)
class StimulusStep:
    target: str
    duration_s: float


TARGET_POSITIONS = {
    "left": (0.25, 0.50),
    "center": (0.50, 0.50),
    "right": (0.75, 0.50),
}


HORIZONTAL_PROTOCOL = [
    StimulusStep("center", 2.0),
    StimulusStep("left", 2.0),
    StimulusStep("center", 2.0),
    StimulusStep("right", 2.0),
    StimulusStep("center", 2.0),
]
