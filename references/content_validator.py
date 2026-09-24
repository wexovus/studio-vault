#!/usr/bin/env python3
"""
Content Validator — YouTube Automation Pipeline
Applies the Show Me The Money content quality framework BEFORE production.
Runs: topic gate, information density scoring, AI authenticity audit, hook check.

Run: python3 scripts/content_validator.py --topic "desk exercises for diabetics"
     python3 scripts/content_validator.py --script path/to/script.md
     python3 scripts/content_validator.py --topic "road warrior restaurant guide" --niche "senior health"
"""

import sys
import os
import json
import re
import argparse
from datetime import datetime
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.yaml")
    try:
        import yaml
        with open(config_path) as f:
            return yaml.safe_load(f)
    except:
        return {"anthropic": {"api_key": os.environ.get("ANTHROPIC_API_KEY", "")}}


# ─────────────────────────────────────────────
# STAGE 1: TOPIC GATE
# ~80% of performance is locked at topic selection
# ─────────────────────────────────────────────

TOPIC_GATE_PROMPT = """You are a content strategist. Evaluate this topic against 4 forcing questions.

TOPIC: {topic}
NICHE: {niche}

For each question below:
- Answer with PASS or FAIL
- Give a 1-sentence justification

---

DEMAND TEST: Whose specific pain does this topic serve? Are people already searching for (or paying for) a worse answer to it?
- PASS: Specific audience has documented pain + is already seeking solutions
- FAIL: "It's about my product" — product introductions have no organic demand

SUPPLY TEST: Who else already covers this, and how well? Is it saturated by better-resourced players?
- PASS: Either (a) few cover it well, OR (b) you have a clear edge
- FAIL: Saturated by well-funded competitors AND you have no identified edge

EDGE TEST: The top results already explain this. What makes THIS piece BETTER — not just "also exists"?
Valid edges (pick one):
  1. First-hand data or results nobody else has
  2. Contrarian-but-correct take
  3. Translate complexity into plain words better than incumbents
- PASS: Can articulate one of the 3 edges clearly
- FAIL: "Mine is more complete" is NOT an edge

TWO-AUDIENCE TEST: Would the target customer love it AND would a stranger not be annoyed by it?
- PASS: Evergreen value even to outsiders
- FAIL: Insider-only content that reads as noise to everyone else

---

After all 4 tests, output:

GATE_RESULT: PASS (proceed to production) or FAIL (kill the topic)

If FAIL: Suggest an angle adjustment that would pass the gate.

Be brutal. A topic that fails the gate cannot be rescued by better writing."""


def run_topic_gate(topic: str, niche: str, api_key: str) -> dict:
    """Run the 4-question topic gate."""
    if not HAS_ANTHROPIC or not api_key or api_key == "your-anthropic-api-key-here":
        return _run_topic_gate_fallback(topic, niche)

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": TOPIC_GATE_PROMPT.format(topic=topic, niche=niche)
        }]
    )
    return {"result": response.content[0].text.strip(), "source": "claude"}


def _run_topic_gate_fallback(topic: str, niche: str) -> dict:
    """Fallback topic gate when Claude isn't available."""
    # Lightweight heuristic check
    score = 0
    notes = []

    # Check for specificity signals
    if any(w in topic.lower() for w in ["diabetics", "blood sugar", "senior", "over 60", "desk"]):
        score += 1
        notes.append("+ Specific health audience identified")
    if any(w in topic.lower() for w in ["guide", "tips", "exercises", "order", "meal"]):
        score += 1
        notes.append("+ Actionable format signal")
    if len(topic.split()) >= 4:
        score += 1
        notes.append("+ Specific enough (4+ words)")

    result = f"FALLBACK CHECK (no API key):\n"
    for n in notes:
        result += f"  {n}\n"
    result += f"\nPreliminary score: {score}/3 — " + ("PASS (get API key for full check)" if score >= 2 else "FAIL")
    return {"result": result, "source": "fallback"}


# ─────────────────────────────────────────────
# STAGE 2: INFORMATION DENSITY SCORING
# ─────────────────────────────────────────────

DENSITY_PROMPT = """Score each information point in this script for information density.

SCORE ANCHORS:
- 80+: A specific conclusion unavailable anywhere else — first-hand data, original finding, judgment tied to concrete numbers
- 60-79: Valuable and specific — a sharp pain point, a directly executable action, a named tool with use
- 40-59: True but commonplace — what everyone covering this topic says, correct concept without example
- Below 40: Filler — rhetorical padding, repetition, off-topic detours

RULES:
- Hook and transition sentences are NOT scored on density (their job is retention/flow)
- Cite the actual sentence in every verdict
- Score each distinct information point individually

---
SCRIPT:
{script}
---

Output as a table:

| Sentence/Point | Score | Reason |
|---|---|---|
| "[exact quote]" | 80+ / 60-79 / 40-59 / <40 | why |

Then:
- Pass threshold (short-form 60-90s): ≥8 sentences at 60+, of which ≥4 at 80+
- Pass/Fail verdict for THIS script
- If FAIL: which sentences are filler that should be cut?"""


def score_density(script: str, api_key: str) -> dict:
    """Score information density of a script."""
    if not HAS_ANTHROPIC or not api_key or api_key == "your-anthropic-api-key-here":
        return {"result": "[No API key — density scoring requires Claude]", "source": "none"}

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": DENSITY_PROMPT.format(script=script[:4000])}]
    )
    return {"result": response.content[0].text.strip(), "source": "claude"}


# ─────────────────────────────────────────────
# STAGE 3: AUTHENTICITY AUDIT (AI Fingerprint Detection)
# ─────────────────────────────────────────────

AUTHENTICITY_PROMPT = """Audit this script for AI-sounding patterns that kill credibility.
Check ALL 12 signals:

| # | Signal | What It Looks Like | Severity |
|---|--------|-------------------|----------|
| 1 | Universal hedging | "It's worth noting", "one might argue", "to be fair" | 🔴 Strong |
| 2 | Frictionless structure | Every point flows perfectly — no rough edges | 🔴 Strong |
| 3 | Metronomic rhythm | All sentences same length | 🔴 Strong |
| 4 | Fixed-position connectors | "However," / "That said," always at sentence start | ⚠️ Medium |
| 5 | Balanced-to-a-fault lists | Every pro has a con, every point has exactly 3 sub-points | ⚠️ Medium |
| 6 | Generic specificity | "A marketing director at a mid-size SaaS company" (nobody) | 🔴 Strong |
| 7 | Vocabulary inflation | "leverage", "landscape", "delve", "game-changer", "tapestry" | 🔴 Strong |
| 8 | Performative emotion | "This is truly remarkable" / "extraordinary results" | ⚠️ Medium |
| 9 | Summary-restates-everything | Final para re-lists all points, zero new info | ⚠️ Medium |
| 10 | Everything resolved | No tensions left open, no gaps admitted | 🔴 Strong |
| 11 | Trinity opener | Every piece follows hook + pain + promise | ⚠️ Medium |
| 12 | Translation artifacts | "In terms of", "with regard to", "based on" | 💡 Weak |

SCORING:
- 0-2 signals: ✅ AUTHENTIC — safe to publish
- 3-5 signals: ⚠️ NEEDS POLISH — fix flagged signals
- 6+ signals: ❌ REWRITE — sounds like AI, find the actual voice

---
SCRIPT:
{script}
---

For each detected signal, quote the exact phrase and suggest how to fix it.
Then give overall VERDICT."""


def audit_authenticity(script: str, api_key: str) -> dict:
    """Check for AI fingerprint patterns."""
    if not HAS_ANTHROPIC or not api_key or api_key == "your-anthropic-api-key-here":
        return {"result": "[No API key — authenticity audit requires Claude]", "source": "none"}

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1536,
        messages=[{"role": "user", "content": AUTHENTICITY_PROMPT.format(script=script[:4000])}]
    )
    return {"result": response.content[0].text.strip(), "source": "claude"}


# ─────────────────────────────────────────────
# STAGE 4: HOOK & TITLE CHECK
# ─────────────────────────────────────────────

HOOK_PROMPT = """Evaluate the hook of this video script against 8 psychological mechanisms.
A strong hook triggers at least 2 mechanisms simultaneously.

MECHANISMS:
1. Cognitive dissonance — contradicts firmly held belief
2. Information gap — activates curiosity (unknown knowledge)
3. Loss aversion — frame the cost of inaction
4. Social identity — "this is for people like me"
5. Anchoring — large number sets expectation
6. Specificity = credibility — precise numbers feel real
7. Scarcity/urgency — limited opportunity
8. Authority contrast — named authority + unexpected viewpoint

Also check against these 12 hook patterns:

| Pattern | Skeleton |
|---------|----------|
| Result-first reversal | "I {achieved X}. The path was {opposite}." |
| Single-number anchor | "{Specific number}. {What it means}." |
| The thing nobody admits | "Nobody talks about this, but {truth}." |
| Yesterday's failure | "Yesterday I {failed}. Here's what I'm changing." |
| N years, one lesson | "I spent {N} years doing X. One thing I'd tell myself." |
| Setup → flip | "Everyone says X. But X is actually {opposite}." |
| Watch what happens | "{Action}. {What happened next}." |
| The question they're afraid to ask | "Should you {decision}? Here's the honest answer." |
| Two roads | "Two roads. {A leads to Y}. {B leads to Z}. Pick one." |
| The price of X | "The price of {decision} is {specific cost}." |
| Reverse credentials | "I'm not a {expected authority}. But {what I know}." |
| The receipt | "{Bold claim}. Receipts: {specific evidence}." |

---
HOOK (first 5-15 seconds of script):
{hook}

THUMBNAIL TEXT (if any):
{thumbnail}

---
Output:
- Which mechanisms does this hook trigger? (minimum 2 required)
- Which pattern does it match?
- Does it PASS or FAIL?
- If FAIL: rewrite the hook to trigger 2+ mechanisms"""


def check_hook(hook: str, thumbnail: str, api_key: str) -> dict:
    """Evaluate hook effectiveness."""
    if not HAS_ANTHROPIC or not api_key or api_key == "your-anthropic-api-key-here":
        return {"result": "[No API key — hook check requires Claude]", "source": "none"}

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": HOOK_PROMPT.format(hook=hook, thumbnail=thumbnail)}]
    )
    return {"result": response.content[0].text.strip(), "source": "claude"}


# ─────────────────────────────────────────────
# STAGE 5: ONE-CORE RESONANCE CHECK
# ─────────────────────────────────────────────

CORE_PROMPT = """Check this script for structural resonance problems.

A piece that says six things says nothing — one core mechanism per piece.

FAILURE MODES:
1. Core diluted — 3-6 parallel points of equal weight
2. Mechanism unstated — conclusion present but "because X, therefore Y" is missing
3. Stance drift — opens as advocate, drifts to adviser, ends as lecturer
4. Correct but flat — everything true, reader shrugs "fair enough"

---
SCRIPT:
{script}
---

Output:
1. What is the ONE core claim? (if only one could survive)
2. Which failure mode(s) does it exhibit?
3. "The skeleton after the fix" in one sentence — what the core structure would be once repaired"""


def check_core(script: str, api_key: str) -> dict:
    """Check one-core resonance."""
    if not HAS_ANTHROPIC or not api_key or api_key == "your-anthropic-api-key-here":
        return {"result": "[No API key — core resonance check requires Claude]", "source": "none"}

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": CORE_PROMPT.format(script=script[:4000])}]
    )
    return {"result": response.content[0].text.strip(), "source": "claude"}


# ─────────────────────────────────────────────
# MAIN VALIDATOR
# ─────────────────────────────────────────────

def extract_hook_from_script(script_content: str) -> str:
    """Pull the HOOK section from a script."""
    hook_match = re.search(
        r'#\s*HOOK\s*\n(.*?)(?=\n#|\n\n|\Z)',
        script_content,
        re.IGNORECASE | re.DOTALL
    )
    if hook_match:
        return hook_match.group(1).strip()[:500]
    # Fallback: first 300 chars
    return script_content[:300]


def extract_hook_from_topic(topic: str, niche: str) -> str:
    """Generate a sample hook from just a topic for the gate check."""
    return f"Topic: {topic} — Niche: {niche}"


def run_full_validation(topic: str, niche: str, script_path: Optional[str] = None,
                        thumbnail: str = "", api_key: str = "") -> dict:
    """Run all 5 validation stages."""
    results = {}
    print_banner = True

    # Stage 1: Topic Gate (always runs)
    print("\n🚪 STAGE 1: TOPIC GATE")
    print("=" * 50)
    gate_result = run_topic_gate(topic, niche, api_key)
    results["topic_gate"] = gate_result
    print(gate_result["result"])

    # Load script if provided
    script_content = ""
    if script_path and os.path.exists(script_path):
        with open(script_path) as f:
            script_content = f.read()
        results["script_path"] = script_path
        results["hook"] = extract_hook_from_script(script_content)
    else:
        results["hook"] = topic  # Use topic as proxy

    # Stages 2-5 only if we have a script
    if script_content:
        # Stage 2: Density
        print("\n\n📊 STAGE 2: INFORMATION DENSITY")
        print("=" * 50)
        density = score_density(script_content, api_key)
        results["density"] = density
        print(density["result"])

        # Stage 3: Authenticity
        print("\n\n🔍 STAGE 3: AUTHENTICITY AUDIT")
        print("=" * 50)
        auth = audit_authenticity(script_content, api_key)
        results["authenticity"] = auth
        print(auth["result"])

        # Stage 4: Hook
        print("\n\n🪝 STAGE 4: HOOK CHECK")
        print("=" * 50)
        hook_check = check_hook(results["hook"], thumbnail, api_key)
        results["hook_check"] = hook_check
        print(hook_check["result"])

        # Stage 5: Core Resonance
        print("\n\n🎯 STAGE 5: ONE-CORE RESONANCE")
        print("=" * 50)
        core = check_core(script_content, api_key)
        results["core"] = core
        print(core["result"])
    else:
        print("\n⚠️  No script provided — stages 2-5 skipped (run with --script to validate a draft)")

    return results


def print_verdict(results: dict) -> str:
    """Synthesize all stages into a final verdict."""
    verdict = "\n" + "=" * 50
    verdict += "\n🏁 FINAL VERDICT\n"
    verdict += "=" * 50

    # Topic gate result
    gate_text = results.get("topic_gate", {}).get("result", "")
    gate_pass = "PASS" in gate_text.upper() and "FAIL" not in gate_text.upper().split("PASS")[0][-20:]
    verdict += f"\n🚪 Topic Gate: {'✅ PASS' if gate_pass else '❌ FAIL'}"

    if not gate_pass:
        verdict += "\n→ Topic fails the gate. Do not produce this video."
        verdict += "\n→ Adjust angle per the gate feedback and re-run."
        return verdict

    # If we have script stages
    if "density" not in results:
        verdict += "\n\n✅ Topic passes gate — ready for script generation."
        verdict += "\n→ Next: python3 scripts/script_writer.py --niche '...' --transcript path/to/transcript.txt"
        return verdict

    verdict += "\n✅ Topic passes gate."

    # Density
    density_text = results.get("density", {}).get("result", "")
    density_pass = "PASS" in density_text.upper() or "✅" in density_text
    verdict += f"\n📊 Density: {'✅ PASS' if density_pass else '⚠️ REVIEW NEEDED'}"

    # Authenticity
    auth_text = results.get("authenticity", {}).get("result", "")
    if "AUTHENTIC" in auth_text.upper():
        verdict += "\n🔍 Authenticity: ✅ PASS"
    elif "REWRITE" in auth_text.upper():
        verdict += "\n🔍 Authenticity: ❌ REWRITE REQUIRED"
    else:
        verdict += "\n🔍 Authenticity: ⚠️ REVIEW NEEDED"

    # Hook
    hook_text = results.get("hook_check", {}).get("result", "")
    hook_pass = "PASS" in hook_text.upper() or "✅" in hook_text
    verdict += f"\n🪝 Hook: {'✅ PASS' if hook_pass else '❌ FAIL'}"

    # Core
    core_text = results.get("core", {}).get("result", "")
    if "diluted" in core_text.lower() or "FAIL" in core_text.upper():
        verdict += "\n🎯 Core: ⚠️ REVIEW (diluted or unfocused)"
    else:
        verdict += "\n🎯 Core: ✅ CLEAR"

    # Overall
    all_pass = gate_pass and density_pass
    if all_pass:
        verdict += "\n\n✅ READY FOR PRODUCTION"
        verdict += "\n→ Next: python3 scripts/video_producer.py --script path/to/script.md --style ms_paint"
    else:
        verdict += "\n\n⚠️ NEEDS REVISION"
        verdict += "\n→ Fix flagged issues, re-run validator, then proceed."

    return verdict


def main():
    parser = argparse.ArgumentParser(description="Content Validator — SMTM Framework")
    parser.add_argument("--topic", help="Topic to validate (e.g., 'desk exercises for diabetics')")
    parser.add_argument("--niche", default="general", help="Niche context (e.g., 'senior health')")
    parser.add_argument("--script", help="Path to script .md to validate (runs all 5 stages)")
    parser.add_argument("--thumbnail", default="", help="Thumbnail text to check against hook")
    parser.add_argument("--output", default="../output/validations/", help="Output directory")
    parser.add_argument("--skip-stages", default="", help="Comma-separated stages to skip (1-5)")
    args = parser.parse_args()

    if not args.topic and not args.script:
        print("❌ Provide --topic and/or --script")
        print("\nExamples:")
        print("  # Validate a topic idea:")
        print("  python3 scripts/content_validator.py --topic 'desk exercises for diabetics' --niche 'senior health'")
        print("")
        print("  # Validate a full script:")
        print("  python3 scripts/content_validator.py --topic 'desk exercises' --script output/scripts/script_001.md")
        return

    config = load_config()
    api_key = config.get("anthropic", {}).get("api_key", "")
    if not api_key or api_key == "your-anthropic-api-key-here":
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if api_key:
            print(f"✅ Using ANTHROPIC_API_KEY from environment")

    if not api_key or api_key == "your-anthropic-api-key-here":
        print("⚠️  No Anthropic API key — running in fallback mode (limited checks)")
        print("   Set key in: config/config.yaml or export ANTHROPIC_API_KEY")
        print()

    topic = args.topic or "unknown"
    niche = args.niche or "general"

    print(f"\n🎬 Content Validator")
    print(f"   Topic: {topic}")
    print(f"   Niche: {niche}")
    if args.script:
        print(f"   Script: {args.script}")

    results = run_full_validation(
        topic=topic,
        niche=niche,
        script_path=args.script,
        thumbnail=args.thumbnail,
        api_key=api_key
    )

    verdict = print_verdict(results)
    print(verdict)
    results["verdict"] = verdict
    results["validated_at"] = datetime.now().isoformat()

    # Save validation report
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), args.output)
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    safe_topic = re.sub(r'[^a-z0-9]+', '_', topic.lower())[:40]
    report_path = os.path.join(output_dir, f"validation_{safe_topic}_{timestamp}.json")

    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n📋 Validation report: {report_path}")

    # Also print stage summaries as markdown
    md_path = report_path.replace(".json", ".md")
    with open(md_path, "w") as f:
        f.write(f"# Content Validation Report\n\n")
        f.write(f"**Topic:** {topic}\n")
        f.write(f"**Niche:** {niche}\n")
        f.write(f"**Validated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"\n---\n\n")
        for stage, data in results.items():
            if isinstance(data, dict) and "result" in data:
                f.write(f"## {stage.upper().replace('_', ' ')}\n\n")
                f.write(f"```\n{data['result']}\n```\n\n")
        f.write(f"---\n\n## VERDICT\n\n{verdict}\n")

    print(f"📄 Markdown report: {md_path}")


if __name__ == "__main__":
    main()
