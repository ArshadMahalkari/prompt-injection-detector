import re

PATTERNS = {
    "override": [
        r"ignore (all )?previous instructions",
        r"disregard earlier context",
    ],
    "data_exfiltration": [
        r"reveal (the )?system prompt",
        r"show hidden instructions",
    ],
    "role_manipulation": [
        r"act as .*",
        r"you are now .*",
    ]
}

WEIGHTS = {
    "override": 0.4,
    "data_exfiltration": 0.35,
    "role_manipulation": 0.25
}


def detect_prompt_injection(text, weights=None):
    score = 0
    matched_categories = []

    for category, patterns in PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                weight = weights.get(category, 0.3) if weights else 0.3
                score += weight
                matched_categories.append(category)
                break

    return {
        "score": min(score, 1.0),
        "categories": list(set(matched_categories)),
        "is_attack": score > 0.3
    }