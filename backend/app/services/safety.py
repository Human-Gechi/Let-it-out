SELF_HARM_SIGNALS = [
    "kill myself",
    "want to die",
    "end my life",
    "no reason to live",
    "hurting myself",
    "self harm",
    "self-harm",
    "suicide",
    "don't want to be alive",
    "better off dead",
    "death is the best thing, right now",
]

CRISIS_NOTE = (
    "It sounds like you might be carrying something very heavy right now. "
    "If you're in crisis or thinking about harming yourself, please reach out "
    "to a real person: in the US, call or text 988 (Suicide & Crisis Lifeline); "
    "in the UK, call Samaritans at 116 123; in Nigeria, call Nigeria Mentally Aware Nigeria Initiative (MANI) at 08091116264  "
    "You don't have to go through this alone much 💝"
)


def flag_risk(text: str) -> bool:
    text = text.lower()
    return any(signal in text for signal in SELF_HARM_SIGNALS)
