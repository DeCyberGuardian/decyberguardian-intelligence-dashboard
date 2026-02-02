def generate_tiktok_script(title, summary):
    return f"""
Hook (0–5s):
Blue teamers, this just dropped.

Context (5–20s):
{title}

Key Insight (20–45s):
{summary[:300]}...

Why It Matters (45–55s):
This affects detection, response, and defensive posture.

CTA (55–60s):
Follow DeCyberGuardian for daily CTI insights.
"""
