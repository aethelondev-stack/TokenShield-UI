import os
import sys
import json
import argparse

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from engine import UIEngine

def main():
    parser = argparse.ArgumentParser(description="Smart UI Grounding & Token Shield CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan screen and return structured JSON")
    scan_parser.add_argument("--source", default="bluestacks", choices=["bluestacks", "desktop", "file"])
    scan_parser.add_argument("--file", help="Path to local image file")

    # Click command
    click_parser = subparsers.add_parser("click", help="Click coordinates or D-Pad sequence")
    click_parser.add_argument("--coords", required=True, help="x,y coordinates (e.g. 375,280)")
    click_parser.add_argument("--method", default="tap", choices=["tap", "dpad"])
    click_parser.add_argument("--dpad", help="Comma separated steps (e.g. DPAD_UP,DPAD_RIGHT,DPAD_CENTER)")

    # Benchmark command
    bench_parser = subparsers.add_parser("benchmark", help="Run benchmark on a sample image")
    bench_parser.add_argument("--image", required=True, help="Path to image file")

    # Reset command
    subparsers.add_parser("reset", help="Reset circuit breaker")

    args = parser.parse_args()
    engine = UIEngine()

    if args.command == "scan":
        img = engine.capture(source=args.source, file_path=args.file)
        # Check circuit breaker
        can_proceed, msg = engine.breaker.check_and_update(img, "scan")
        if not can_proceed:
            print(json.dumps({"status": "CIRCUIT_BREAKER_TRIGGERED", "error": msg}, indent=2))
            sys.exit(1)

        result = engine.scan_screen(img)
        print(json.dumps(result, indent=2))

    elif args.command == "click":
        parts = list(map(int, args.coords.split(",")))
        dpad_steps = args.dpad.split(",") if args.dpad else None
        success, msg = engine.execute_action(parts, method=args.method, dpad_steps=dpad_steps)
        print(json.dumps({"success": success, "message": msg}))

    elif args.command == "benchmark":
        img = engine.capture(file_path=args.image)
        result = engine.scan_screen(img)
        cyan_focus = engine.detect_cyan_focus(img)
        cards = engine.detect_card_grid(img)
        
        print("=== BENCHMARK RESULTS ===")
        print(f"Image Size: {img.size}")
        print(f"Cyan Focus Detected: {cyan_focus}")
        print(f"Cards Detected: {len(cards)}")
        if cyan_focus and cards:
            fc_center = [(cyan_focus[0] + cyan_focus[2])//2, (cyan_focus[1] + cyan_focus[3])//2]
            # Test navigation to a target card
            target = cards[1]['center']
            dpad = engine.calculate_dpad_steps(fc_center, target)
            print(f"Navigation from Focus ({fc_center}) to Target ({target}): {dpad}")
        print(json.dumps(result, indent=2))

    elif args.command == "reset":
        engine.breaker.reset()
        print(json.dumps({"status": "Circuit breaker reset to normal."}))

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
