# WLED 16.0.1 Jason/RGB2Go Custom Roll-forward

Generated: 2026-07-26T00:55:01

Base: WLED v16.0.1 from `https://github.com/wled/WLED/archive/refs/tags/v16.0.1.tar.gz`

## Port decision

I checked WLED 16.0.0 -> 16.0.1 changes in the files Jason had changed. Nothing looked like a blocker:

- `wled00/cfg.cpp`: no upstream change in the Ethernet init block; safe to reapply delay.
- `wled00/wled.h`: upstream changed default colors elsewhere; Jason's AP behavior line was unchanged upstream; safe to reapply while preserving upstream color fix.
- `usermods/audioreactive/audio_reactive.cpp`: upstream did change this file, but not Jason's decay/I2S default lines; I patched only Jason's specific defaults and preserved upstream 16.0.1 fixes.
- Web UI source changed in 16.0.1, so I did **not** blindly copy Jason's generated `html_*.h/js_*.h` blobs. I copied Jason's editable `wled00/data/welcome.htm` branding change, then regenerated the web UI headers using WLED 16.0.1's build tool so 16.0.1 UI fixes are retained.

## Applied changes

- Added Jason's `platformio_override.ini` board environments.
- Added `wled00/my_config.h` from the customized 16.0.0 tree.
- Reapplied RGB2Go welcome page logo change in `wled00/data/welcome.htm`.
- Rebuilt/generated:
  - `wled00/html_cpal.h`
  - `wled00/html_edit.h`
  - `wled00/html_other.h`
  - `wled00/html_pixart.h`
  - `wled00/html_pixelforge.h`
  - `wled00/html_pxmagic.h`
  - `wled00/html_settings.h`
  - `wled00/html_ui.h`
  - `wled00/js_iro.h`
  - `wled00/js_omggif.h`
- Reapplied audio-reactive defaults:
  - `decayTime = 80`
  - I2S SD pin `25`
  - I2S WS/LRCL pin `26`
  - I2S CK/BCLK pin `27`
- Reapplied Ethernet boot workaround:
  - `delay(1000)` before `initEthernet()` under `WLED_USE_ETHERNET`.
- Reapplied default AP behavior:
  - `AP_BEHAVIOR_ALWAYS`.

## Deliberately not carried forward

These were present in the 16.0.0 custom archive but looked nonfunctional or potentially harmful:

- `package.json` dependency order-only change was not reapplied; version remains `16.0.1` and dependencies are upstream 16.0.1.
- `tools/wled-tools` executable-bit loss was not reapplied; keeping the script executable is safer.
- `node_modules/`, `.pio/`, and transient build folders are not included in the source package.

## Verification performed

Commands run successfully:

```bash
npm ci
npm run build
npm test
pio run -e solo2go_esp32_eth
pio run
```

Results:

- Node tests: 16 passed, 0 failed.
- PlatformIO default custom environments: 4 succeeded.
  - `solo2go_esp32_eth`
  - `solo2go_esp32_eth_dmx`
  - `tetra2go_esp32_eth`
  - `octa2go_esp32_eth`

Firmware outputs produced:

- `WLED_16.0.1_Solo2Go-Eth.bin`
- `WLED_16.0.1_Solo2Go-Eth-DMX.bin`
- `WLED_16.0.1_Tetra2Go-Eth.bin`
- `WLED_16.0.1_Octa2Go-Eth.bin`

Warnings seen were existing-style build warnings, mainly `DEFAULT_LED_COUNT` macro redefinition from build flags and third-party shadow warnings; no errors.

## Diff files

- `WLED-16.0.1-Jason-RGB2Go-name-status.txt`
- `WLED-16.0.1-Jason-RGB2Go-diff-stat.txt`
- `WLED-16.0.1-Jason-RGB2Go-full.diff`
