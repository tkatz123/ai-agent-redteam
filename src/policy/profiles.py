# src/policy/profiles.py
from dataclasses import dataclass

@dataclass
class Profile:
    allow_untrusted_override: bool
    sanitize_notes: bool
    sanitize_body: bool
    output_filter: bool
    allowlist: bool
    consent: bool
    regex_detector: bool = False
    regex_threshold: int = 4

PROFILES = {
    "normal": Profile(
        allow_untrusted_override=True,
        sanitize_notes=False,
        sanitize_body=False,
        output_filter=False,
        allowlist=False,
        consent=False,
        regex_detector=False,
        regex_threshold=9999
    ),
    "strict": Profile(
        allow_untrusted_override=False,
        sanitize_notes=True,
        sanitize_body=True,
        output_filter=True,
        allowlist=True,
        consent=True,
        regex_detector=True,
        regex_threshold=4
    ),
    "test": Profile(
        allow_untrusted_override=True,
        sanitize_notes=False,
        sanitize_body=False,
        output_filter=False,
        allowlist=False,
        consent=False,
        regex_detector=False,
        regex_threshold=9999
    ),
}

def get_profile(name: str) -> Profile:
    return PROFILES.get(name, PROFILES["normal"])
