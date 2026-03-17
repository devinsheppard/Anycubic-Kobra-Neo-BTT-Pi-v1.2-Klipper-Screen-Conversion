#!/usr/bin/env python3
"""
EncoderMouse-BTT.py

Placeholder script for the Anycubic Kobra Neo BTT Pi Klipper Screen conversion.
Replace this file later with the real encoder/mouse handling code.
"""

import time
import signal
import sys

running = True


def handle_exit(signum, frame):
    global running
    running = False


signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)


def main():
    print("EncoderMouse-BTT placeholder started.")
    print("Replace this file with the real encoder support script later.")

    while running:
        time.sleep(1)

    print("EncoderMouse-BTT placeholder stopped.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"EncoderMouse-BTT placeholder crashed: {exc}", file=sys.stderr)
        sys.exit(1)