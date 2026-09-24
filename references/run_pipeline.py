#!/usr/bin/env python3
"""
YouTube Automation Pipeline — Master Orchestrator
Run this to execute the full pipeline from niche research → script → video.

Usage:
  python3 run_pipeline.py --step all --niche "ancient humans"
  python3 run_pipeline.py --step research
  python3 run_pipeline.py --step scripts --niche "senior health"
  python3 run_pipeline.py --step video --script path/to/script.md
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.content_validator import main as validate_main
from scripts.niche_researcher import main as niche_main
from scripts.script_writer import main as script_main
from scripts.video_producer import main as video_main
import argparse

STEPS = {
    "validate": "Content Validation (topic gate → density → authenticity → hook → core)",
    "research": "Niche Research (Claude + VidIQ analysis)",
    "scripts": "Script Generation (Claude + TurboScribe)",
    "video": "Video Production (Higgsfield images + voice)",
    "all": "Full Pipeline (validate → research → scripts → video)",
}

def print_banner():
    banner = r"""
╔═══════════════════════════════════════════════════╗
║   YouTube Automation Pipeline                    ║
║   Niche → Script → Video → Upload              ║
╚═══════════════════════════════════════════════════╝
"""
    print(banner)

def main():
    parser = argparse.ArgumentParser(description="YouTube Automation Pipeline")
    parser.add_argument("--step", default="all",
                        choices=["validate", "research", "scripts", "video", "all"],
                        help="Which step to run")
    parser.add_argument("--niche", help="Niche for script generation")
    parser.add_argument("--video-type", default="shorts 60sec",
                        help="Video type: 'shorts 60sec', 'long-form 10min', 'how-to 5min'")
    parser.add_argument("--channels", help="Comma-separated YouTube channel URLs for research")
    parser.add_argument("--script", help="Path to script for video production")
    parser.add_argument("--transcript", help="Path to transcript .txt file")
    parser.add_argument("--video-url", help="YouTube URL to transcribe")
    parser.add_argument("--style", default="ms_paint",
                        choices=["ms_paint", "cinematic", "anime", "photorealistic"])
    parser.add_argument("--count", type=int, default=3,
                        help="Number of script variations to generate")
    parser.add_argument("--guide", action="store_true",
                        help="Print manual research guide and exit")

    args = parser.parse_args()

    print_banner()

    # Guide mode
    if args.guide:
        from scripts.niche_researcher import manual_research_guide
        print(manual_research_guide())
        return

    # Full pipeline
    if args.step == "all":
        print("🚀 Running FULL pipeline\n")

        # Step 1: Research
        print("=" * 50)
        print("STEP 1: NICHE RESEARCH")
        print("=" * 50)
        if args.channels:
            sys.argv = ["niche_researcher", "--channels", args.channels]
        else:
            sys.argv = ["niche_researcher", "--guide"]
        niche_main()

        if not args.niche:
            print("\n⚠️ Pass --niche to generate scripts")
            return

        # Step 2: Scripts
        print("\n" + "=" * 50)
        print("STEP 2: SCRIPT GENERATION")
        print("=" * 50)
        script_args = ["script_writer",
                       "--niche", args.niche,
                       "--type", args.video_type,
                       "--count", str(args.count)]
        if args.transcript:
            script_args += ["--transcript", args.transcript]
        if args.video_url:
            script_args += ["--video-url", args.video_url]
        sys.argv = script_args
        script_main()

        # Step 3: Video
        print("\n" + "=" * 50)
        print("STEP 3: VIDEO PRODUCTION")
        print("=" * 50)
        # Find the most recent script
        script_dir = os.path.join(os.path.dirname(__file__), "output", "scripts")
        scripts = sorted([f for f in os.listdir(script_dir) if f.endswith(".md")],
                        reverse=True) if os.path.exists(script_dir) else []
        if scripts:
            script_path = os.path.join(script_dir, scripts[0])
            sys.argv = ["video_producer",
                        "--script", script_path,
                        "--style", args.style]
            video_main()
        else:
            print("⚠️ No scripts found — generate scripts first with --step scripts")

        print("\n✅ Pipeline complete!")
        print("   Check: output/scripts/ and output/videos/")
        return

    # Individual steps
    if args.step == "validate":
        if not args.topic and not args.script:
            print("❌ --topic or --script required for validation")
            return
        sys.argv = ["content_validator"]
        if args.topic:
            sys.argv += ["--topic", args.topic]
        if args.niche:
            sys.argv += ["--niche", args.niche]
        if args.script:
            sys.argv += ["--script", args.script]
        validate_main()

    elif args.step == "research":
        sys.argv = ["niche_researcher"]
        if args.channels:
            sys.argv += ["--channels", args.channels]
        niche_main()

    elif args.step == "scripts":
        if not args.niche:
            print("❌ --niche required for script generation")
            return
        sys.argv = ["script_writer",
                    "--niche", args.niche,
                    "--type", args.video_type,
                    "--count", str(args.count)]
        if args.transcript:
            sys.argv += ["--transcript", args.transcript]
        if args.video_url:
            sys.argv += ["--video-url", args.video_url]
        script_main()

    elif args.step == "video":
        if not args.script:
            print("❌ --script required for video production")
            return
        sys.argv = ["video_producer",
                    "--script", args.script,
                    "--style", args.style]
        video_main()

if __name__ == "__main__":
    main()
