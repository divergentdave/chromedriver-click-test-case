#!/usr/bin/env python3
import copy
import time
import subprocess
import sys

from ruamel.yaml import YAML


def run_trials():
    test_args = ["docker", "exec", "-it", "test-case-web", "python", "test.py"]
    success_count = 0
    failure_count = 0
    for i in range(100):
        result = subprocess.run(test_args)
        if result.returncode == 0:
            success_count += 1
        else:
            failure_count += 1
    return success_count, failure_count


def run_with_compose(compose_file="docker-compose.yml"):
    sys.stdout.flush()
    subprocess.run(
        ["docker-compose", "-f", compose_file, "build"],
        check=True,
    )
    docker = subprocess.Popen(
        ["docker-compose", "-f", compose_file, "up"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(30)
    success_count, failure_count = run_trials()
    subprocess.run([
        "docker",
        "exec",
        "-it",
        "test-case-selenium",
        "chromedriver",
        "--version",
    ])
    docker.terminate()
    docker.wait()
    sys.stdout.flush()
    print("{} successes, {} failures".format(success_count, failure_count))


def main():
    yaml = YAML(typ="rt")
    with open("docker-compose.yml", "rb") as f:
        original_config = yaml.load(f)
    new_compose_file_name = "docker-compose.modified.yml"
    versions = [
        "77.0.3865.40",
        "77.0.3865.10",
    ]
    for version in versions:
        modified_config = copy.deepcopy(original_config)
        del modified_config["services"]["selenium"]["image"]
        modified_config["services"]["selenium"]["build"] = {
            "context": "selenium",
            "args": {
                "CHROME_DRIVER_VERSION": version,
            },
        }
        with open(new_compose_file_name, "wb") as f:
            yaml.dump(modified_config, f)
        run_with_compose(new_compose_file_name)


if __name__ == "__main__":
    main()
