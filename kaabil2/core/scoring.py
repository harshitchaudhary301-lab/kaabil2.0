def calculate_role_fit(required_levels, student_levels):
    """Weighted fit score: available proficiency divided by required proficiency."""
    if not required_levels:
        return 0
    scores = []
    for skill_id, required in required_levels.items():
        required = max(int(required), 1)
        current = max(0, min(int(student_levels.get(skill_id, 0)), 100))
        scores.append(min(current / required, 1.0) * 100)
    return round(sum(scores) / len(scores))

def skill_gaps(required_levels, student_levels):
    gaps = []
    for skill_id, required in required_levels.items():
        current = int(student_levels.get(skill_id, 0))
        if current < int(required):
            gaps.append({"skill_id": skill_id, "current": current, "required": int(required),
                         "gap": int(required) - current})
    return sorted(gaps, key=lambda x: x["gap"], reverse=True)
