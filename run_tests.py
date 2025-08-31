#!/usr/bin/env python3
"""
Simple test runner script for the Playwright AI Test Framework.
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_command(command):
    """Run a command and return the result."""
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    return result.returncode == 0


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run Playwright AI tests")
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests only")
    parser.add_argument("--web", action="store_true", help="Run web UI tests")
    parser.add_argument("--chat", action="store_true", help="Run chat functionality tests")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--headless", action="store_true", default=True, help="Run in headless mode")
    parser.add_argument("--browser", default="chromium", choices=["chromium", "firefox", "webkit"], help="Browser to use")
    parser.add_argument("--env", default="local", choices=["local", "staging", "production"], help="Environment to test")
    parser.add_argument("--report", action="store_true", help="Generate HTML report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Build pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add markers based on arguments
    markers = []
    if args.smoke:
        markers.append("smoke")
    if args.web:
        markers.append("web")
    if args.chat:
        markers.append("chat")
    if args.performance:
        markers.append("performance")
    
    if markers:
        cmd.extend(["-m", " or ".join(markers)])
    
    # Add other options
    if args.verbose:
        cmd.append("-v")
    
    if args.report:
        cmd.extend(["--html=reports/report.html", "--self-contained-html"])
    
    # Set environment variables
    import os
    os.environ["TEST_ENV"] = args.env
    os.environ["BROWSER_NAME"] = args.browser
    os.environ["HEADLESS"] = str(args.headless).lower()
    
    # Ensure reports directory exists
    Path("reports").mkdir(exist_ok=True)
    
    print(f"Running tests with environment: {args.env}")
    print(f"Browser: {args.browser} (headless: {args.headless})")
    
    # Run the tests
    success = run_command(cmd)
    
    if success:
        print("\n✅ All tests passed!")
        if args.report:
            print("📊 HTML report generated: reports/report.html")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
