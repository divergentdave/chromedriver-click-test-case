#!/usr/bin/env python3
import copy
import os
import sys
import time
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_trials():
    test_args = [os.path.join(BASE_DIR, "test.py")]
    env = os.environ.copy()
    env["PATH"] += ":./chrome-linux"
    success_count = 0
    failure_count = 0
    for i in range(100):
        result = subprocess.run(test_args, env=env)
        if result.returncode == 0:
            success_count += 1
        else:
            failure_count += 1
    return success_count, failure_count


def run_with_server():
    server = subprocess.Popen(
        [os.path.join(BASE_DIR, "./server.py")],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(5)
    success_count, failure_count = run_trials()
    server.terminate()
    server.wait()
    print("{} successes, {} failures".format(success_count, failure_count))
    return failure_count == 0


def main():
    if run_with_server():
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
