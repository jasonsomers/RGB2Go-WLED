#!/usr/bin/env python3
"""Collect RGB2Go WLED firmware outputs into a release directory.

The WLED version number is intentionally discovered from the generated filename so
this script keeps working after a future roll-forward from 16.0.1 to 16.0.2+.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ENV_TO_RELEASE_NAME = {
    "matrix2go_esp32": "Matrix2Go",
    "solo2go_esp32": "Solo2Go",
    "solo2go_esp32_oled": "Solo2Go-OLED",
    "solo2go_esp32_eth": "Solo2Go-Eth",
    "solo2go_esp32_dmx": "Solo2Go-DMX",
    "solo2go_esp32_eth_dmx": "Solo2Go-Eth-DMX",
    "solo2go_esp32_diff": "Solo2Go-Diff",
    "duo2go_esp32": "Duo2Go_v2",
    "duo2go_esp32_dmx": "Duo2Go-DMX",
    "tetra2go_esp32": "Tetra2Go",
    "tetra2go_esp32_oled": "Tetra2Go-OLED",
    "tetra2go_esp32_diff": "Tetra2Go-Diff",
    "tetra2go_esp32_eth": "Tetra2Go-Eth",
    "octa2go_esp32": "Octa2Go",
    "octa2go_esp32_oled": "Octa2Go-OLED",
    "octa2go_esp32_eth": "Octa2Go-Eth",
}


def find_bin(env: str) -> Path:
    release_name = ENV_TO_RELEASE_NAME[env]
    matches = sorted(Path("build_output/release").glob(f"WLED_*_{release_name}.bin"))
    if len(matches) != 1:
        raise FileNotFoundError(
            f"{env}: expected one WLED_*_{release_name}.bin in build_output/release, found {len(matches)}"
        )
    return matches[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-list", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    envs = [line.strip() for line in Path(args.env_list).read_text().splitlines() if line.strip()]

    missing = []
    for env in envs:
        if env not in ENV_TO_RELEASE_NAME:
            missing.append(f"{env}: no release-name mapping")
            continue
        try:
            src = find_bin(env)
        except FileNotFoundError as exc:
            missing.append(str(exc))
            continue
        shutil.copy2(src, out / src.name)
        print(f"Collected {src.name}")

    if missing:
        raise SystemExit("Missing firmware outputs:\n" + "\n".join(missing))


if __name__ == "__main__":
    main()
