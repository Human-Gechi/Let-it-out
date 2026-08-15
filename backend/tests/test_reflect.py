# Confirms POST /api/v1/reflect:
# - never persists letter_text anywhere (no DB/file writes as a side effect)
# - returns safe_to_release=False + CRISIS_NOTE when flagged text is submitted
# - falls back gracefully when the AI provider is unavailable
