#!/usr/bin/env python3
"""Resolve RGB2Go PlatformIO environments for low-cost GitHub Actions builds."""
from __future__ import annotations

import argparse
from pathlib import Path

ALL_ENVS = [
    "matrix2go_esp32",
    "solo2go_esp32",
    "solo2go_esp32_oled",
    "solo2go_esp32_eth",
    "solo2go_esp32_dmx",
    "solo2go_esp32_eth_dmx",
    "solo2go_esp32_diff",
    "duo2go_esp32",
    "duo2go_esp32_dmx",
    "tetra2go_esp32",
    "tetra2go_esp32_oled",
    "tetra2go_esp32_diff",
    "tetra2go_esp32_eth",
    "octa2go_esp32",
    "octa2go_esp32_oled",
    "octa2go_esp32_eth",
]

SETS = {
    # Low-cost default for routine config changes we have been making recently.
    "changed-defaults": [
        "tetra2go_esp32_eth",
        "solo2go_esp32_oled",
        "tetra2go_esp32_oled",
        "octa2go_esp32_oled",
    ],
    "all": ALL_ENVS,
    "oled": [
        "solo2go_esp32_oled",
        "tetra2go_esp32_oled",
        "octa2go_esp32_oled",
    ],
    "ethernet": [
        "solo2go_esp32_eth",
        "solo2go_esp32_eth_dmx",
        "tetra2go_esp32_eth",
        "octa2go_esp32_eth",
    ],
    "dmx": [
        "solo2go_esp32_dmx",
        "solo2go_esp32_eth_dmx",
        "duo2go_esp32_dmx",
    ],
    "base": [
        "matrix2go_esp32",
        "solo2go_esp32",
        "duo2go_esp32",
        "tetra2go_esp32",
        "octa2go_esp32",
    ],
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", required=True, choices=[*SETS.keys(), "single"])
    parser.add_argument("--single", default="")
    parser.add_argument("--github-output", default="")
    args = parser.parse_args()

    if args.set == "single":
        env = args.single.strip()
        if env not in ALL_ENVS:
            raise SystemExit(f"Unknown or missing RGB2Go env for build_set=single: {env!r}")
        envs = [env]
    else:
        envs = SETS[args.set]

    dist = Path("dist")
    dist.mkdir(exist_ok=True)
    Path("dist/envs.txt").write_text("\n".join(envs) + "\n")

    print("Selected environments:")
    for env in envs:
        print(f"- {env}")

    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as fh:
            fh.write(f"count={len(envs)}\n")
            fh.write(f"envs={','.join(envs)}\n")


if __name__ == "__main__":
    main()
