#!/usr/bin/env python3
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
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    docker = subprocess.Popen(
        ["docker-compose", "-f", compose_file, "up"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(30)
    success_count, failure_count = run_trials()
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
        "3.141.59-xenon",
        "3.141.59-vanadium",
        "3.141.59-uranium",
        "3.141.59-titanium",
        "3.141.59-selenium",
        "3.141.59-radium",
        "3.141.59-palladium",
        "3.141.59-oxygen",
        "3.141.59-neon",
        # "3.141.59-mercury",
        # "3.141.59-lithium",
        # "3.141.59-krypton",
        # "3.141.59-iron",
        # "3.141.59-hafnium",
        # "3.141.59-gold",
        # "3.141.59-fluorine",
        # "3.141.59-europium",
        # "3.141.59-dubnium",
        # "3.141.59-copernicium",
        # "3.141.59-bismuth",
        # "3.141.59-antimony",
    ]
    for version in versions:
        image = "selenium/standalone-chrome-debug:{}".format(version)
        subprocess.run(["docker", "pull", image], check=True)
    for version in versions:
        image = "selenium/standalone-chrome-debug:{}".format(version)
        modified_config = original_config.copy()
        modified_config["services"]["selenium"]["image"] = image
        with open(new_compose_file_name, "wb") as f:
            yaml.dump(modified_config, f)
        print(image)
        run_with_compose(new_compose_file_name)
        print(image)


if __name__ == "__main__":
    main()
