"""Combines independent signals into one score, level, and confidence.

Each signal = {"name", "weight" (0-1: how strongly it suggests a scam), "reason" (plain language)}.
Score uses noisy-OR: many weak signals add up, but no single weak signal dominates.
"""
from math import prod


def sig(name: str, weight: float, reason: str) -> dict:
    return {"name": name, "weight": round(weight, 2), "reason": reason}


def level_for(score: float) -> str:
    if score < 25:
        return "low"
    if score < 50:
        return "medium"
    if score < 75:
        return "high"
    return "critical"


def combine(signals: list[dict], ml_prob: float | None = None, trusted: bool = False) -> dict:
    rule_p = 1 - prod(1 - s["weight"] for s in signals) if signals else 0.0
    if ml_prob is None:
        p = rule_p
    else:
        p = 0.6 * rule_p + 0.4 * ml_prob      # rules are explainable, so they get more weight
    if trusted and rule_p < 0.5:
        p *= 0.4                                # verified official domain, no strong red flags

    score = round(min(p, 0.99) * 100)
    agree = ml_prob is None or (ml_prob > 0.5) == (rule_p > 0.5)
    strength = min(len(signals), 5) / 5
    confidence = "high" if (agree and (strength >= 0.6 or score < 10)) else "medium" if agree else "low"

    verdicts = {
        "low": "No strong scam signs found",
        "medium": "Some warning signs. Be careful",
        "high": "Likely a scam",
        "critical": "Very likely a scam",
    }
    
    lvl = level_for(score)
    return {
        "score": score,
        "level": lvl,
        "verdict": verdicts[lvl],
        "confidence": confidence,
        "reasons": [s["reason"] for s in sorted(signals, key=lambda s: -s["weight"])],
        "signals": signals,
        "ml_used": ml_prob is not None,
        "disclaimer": "This is an automated estimate, not a guarantee. When in doubt, contact the company using a number you find yourself.",
    }