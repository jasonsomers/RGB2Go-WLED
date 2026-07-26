# WLED 16.0.0 Customization Reference — Jason/RGB2Go

Compared vanilla WLED `v16.0.0` from GitHub against Jason's modified Google Drive archive.

Generated: 2026-07-26T00:43:45

## Scope / noise filtered

The modified archive contains generated/local-build material that is **not source customization**:

- `node_modules/` — 1008 dependency files, from `npm install` / build tooling.
- `.pio/` — empty PlatformIO build directory tree in this archive.
- `build_output/` — empty release/map/firmware directory tree in this archive.
- `package-lock.json` exists but matches vanilla.

After excluding those generated directories, there are **18 changed source-tree entries**:

```text
M	cmp/vanilla/package.json
A	cmp/modified/platformio_override.ini
M	cmp/vanilla/tools/wled-tools
M	cmp/vanilla/usermods/audioreactive/audio_reactive.cpp
M	cmp/vanilla/wled00/cfg.cpp
M	cmp/vanilla/wled00/data/welcome.htm
A	cmp/modified/wled00/html_cpal.h
A	cmp/modified/wled00/html_edit.h
A	cmp/modified/wled00/html_other.h
A	cmp/modified/wled00/html_pixart.h
A	cmp/modified/wled00/html_pixelforge.h
A	cmp/modified/wled00/html_pxmagic.h
A	cmp/modified/wled00/html_settings.h
A	cmp/modified/wled00/html_ui.h
A	cmp/modified/wled00/js_iro.h
A	cmp/modified/wled00/js_omggif.h
A	cmp/modified/wled00/my_config.h
M	cmp/vanilla/wled00/wled.h
```

## High-priority functional changes to carry forward

1. **Custom PlatformIO environments** in `platformio_override.ini` for RGB2Go/2Go boards.
2. **Ethernet boot workaround** in `wled00/cfg.cpp`: adds a 1-second delay before `initEthernet()` when `WLED_USE_ETHERNET` is enabled.
3. **AP behavior default** in `wled00/wled.h`: default AP behavior changed to `AP_BEHAVIOR_ALWAYS`.
4. **Audio-reactive defaults** in `usermods/audioreactive/audio_reactive.cpp`: decay time and I2S pins changed.
5. **RGB2Go branding on welcome page** in `wled00/data/welcome.htm` and regenerated web UI header blobs.
6. **Generated web UI headers** added under `wled00/html_*.h` and `wled00/js_*.h`, including PixelForge / Pixel Art / PxMagic pages.
7. Minor/local-tree changes: dependency ordering in `package.json`, executable bit removed from `tools/wled-tools`, empty/default `wled00/my_config.h` present.

## File-by-file changes

### `platformio_override.ini` — added

Adds 16 custom PlatformIO environments and sets the default build targets to:

```ini
default_envs = octa2go_esp32_eth, solo2go_esp32_eth, solo2go_esp32_eth_dmx, tetra2go_esp32_eth
```

Environment summary:

|env|release|pixel counts|data pins|total LEDs|ABL mA|order|usermod|eth|dmx|OLED|
|---|---|---|---|---|---|---|---|---|---|---|
|matrix2go_esp32|"Matrix2Go"|"256"|"2"|256|1000|"COL_ORDER_GRB"|audioreactive||||
|solo2go_esp32|"Solo2Go"|"100"|"2"|100|5000|"COL_ORDER_RGB"|audioreactive||||
|solo2go_esp32_oled|"Solo2Go-OLED"|"100"|"2"|100|5000|"COL_ORDER_RGB"|usermod_v2_four_line_display_ALT|||SSD1306_64|
|solo2go_esp32_eth|"Solo2Go-Eth"|"100"|"2"|100|5000|"COL_ORDER_RGB"||yes|||
|solo2go_esp32_dmx|"Solo2Go-DMX"||||||||yes||
|solo2go_esp32_eth_dmx|"Solo2Go-Eth-DMX"|||||||yes|yes||
|solo2go_esp32_diff|"Solo2Go-Diff"|"100,100,100,100,100"|"2,27,26,25,33"|500|25000|"COL_ORDER_RGB"|||||
|duo2go_esp32|"Duo2Go_v2"|"100,100"|"2,13"|200|10000|"COL_ORDER_RGB"|||||
|duo2go_esp32_dmx|"Duo2Go-DMX"||||||||yes||
|tetra2go_esp32|"Tetra2Go"|"100,100,100,100"|"2,13,12,14"|400|20000|"COL_ORDER_RGB"|audioreactive||||
|tetra2go_esp32_oled|"Tetra2Go-OLED"|"100,100,100,100"|"2,13,12,14"|400|20000|"COL_ORDER_RGB"|usermod_v2_four_line_display_ALT|||SSD1306_64|
|tetra2go_esp32_diff|"Tetra2Go-Diff"|"100,100,100,100,100,100,100,100"|"2,13,12,14,27,26,25,33"|800|40000|"COL_ORDER_RGB"|||||
|tetra2go_esp32_eth|"Tetra2Go-Eth"|"100,100,100,10"|"2,13,12,14"|400|20000|"COL_ORDER_RGB"||yes|||
|octa2go_esp32|"Octa2Go"|"100,100,100,100,100,100,100,100"|"2,13,12,14,4,16,32,33"|800|40000|"COL_ORDER_RGB"|audioreactive||||
|octa2go_esp32_eth|"Octa2Go-Eth"|"100,100,100,100,100,100,100,100"|"2,13,12,14,4,16,32,33"|800|40000|"COL_ORDER_RGB"||yes|||
|octa2go_esp32_oled|"Octa2Go-OLED"|"100,100,100,100,100,100,100,100"|"2,13,12,14,4,16,32,33"|800|40000|"COL_ORDER_RGB"|usermod_v2_four_line_display_ALT|yes||SSD1306_64|


Common patterns in those environments:

- ESP32 board: `esp32dev`
- Platform: `${esp32_idf_V4.platform}`
- Platform packages: `${esp32_idf_V4.platform_packages}`
- Build unflags: `${common.build_unflags}`
- Build flags include `${common.build_flags} ${esp32_idf_V4.build_flags}`
- Partitions: `${esp32.default_partitions}`
- Flash mode: `dio`
- Color order is mostly `COL_ORDER_RGB`; `matrix2go_esp32` uses `COL_ORDER_GRB`.
- Audio-reactive builds use `custom_usermods = audioreactive` plus `${esp32.AR_lib_deps}`.
- OLED builds use `custom_usermods = usermod_v2_four_line_display_ALT`, `FLD_TYPE=SSD1306_64`, `I2CSCLPIN=22`, `I2CSDAPIN=21`, plus `ESP Rotary` and `U8g2` libs.
- Ethernet builds define `WLED_USE_ETHERNET`; `tetra2go_esp32_eth`, `octa2go_esp32_eth`, and `octa2go_esp32_oled` also define `WLED_ETH_DEFAULT=WLED_ETH_ESP32DEUX` and `WLED_DISABLE_ESPNOW`.
- DMX builds define `WLED_ENABLE_DMX`.

Notable per-board pin/default sets:

- `matrix2go_esp32`: 256 LEDs on pin `2`, 1000 mA limit, GRB.
- `solo2go_esp32` / OLED / Ethernet: 100 LEDs on pin `2`, 5000 mA limit, RGB.
- `solo2go_esp32_diff`: five outputs on `2,27,26,25,33`, total 500 LEDs, 25000 mA.
- `duo2go_esp32`: two outputs on `2,13`, total 200 LEDs, 10000 mA.
- `tetra2go_esp32`: four outputs on `2,13,12,14`, total 400 LEDs, 20000 mA.
- `tetra2go_esp32_diff`: eight outputs on `2,13,12,14,27,26,25,33`, total 800 LEDs, 40000 mA.
- `tetra2go_esp32_eth`: four outputs on `2,13,12,14`, but `PIXEL_COUNTS="100,100,100,10"`; total remains 400 LEDs. Also disables relay and button pins with `RLYPIN=-1`, `BTNPIN=-1`.
- `octa2go_esp32` / Ethernet / OLED: eight outputs on `2,13,12,14,4,16,32,33`, total 800 LEDs, 40000 mA.

### `usermods/audioreactive/audio_reactive.cpp` — modified

Audio-reactive defaults changed:

```diff
-static uint16_t decayTime = 1400;
+static uint16_t decayTime = 80;

-int8_t i2ssdPin = 32;
+int8_t i2ssdPin = 25;

-int8_t i2swsPin = 15;
+int8_t i2swsPin = 26;

-int8_t i2sckPin = 14;
+int8_t i2sckPin = 27;
```

Meaning: faster decay response and RGB2Go-specific default I2S microphone/audio pins: SD=`25`, WS/LRCL=`26`, CK/BCLK=`27`.

### `wled00/cfg.cpp` — modified

Adds a boot delay before Ethernet initialization:

```diff
 #ifdef WLED_USE_ETHERNET
   JsonObject ethernet = doc[F("eth")];
   CJSON(ethernetType, ethernet["type"]);
   // NOTE: Ethernet configuration takes priority over other use of pins
+  delay(1000); // added JPS 6/2/2026 to fix boot isue in 0.16.0 when ethernet cable plugged in a boottime
   initEthernet();
 #endif
```

Carry-forward note: preserve this in future WLED merges unless upstream fixes the Ethernet cable-at-boot issue another way.

### `wled00/wled.h` — modified

Changes the default AP behavior:

```diff
-WLED_GLOBAL byte apBehavior _INIT(AP_BEHAVIOR_BOOT_NO_CONN);
+WLED_GLOBAL byte apBehavior _INIT(AP_BEHAVIOR_ALWAYS);
```

Meaning: WLED AP is open/available by default rather than only opening after no connection at boot.

### `wled00/data/welcome.htm` — modified

The vanilla WLED logo image was replaced with an RGB2Go-branded embedded PNG and styling:

```html
<img src="data:image/png;base64,..." style="width:300px;margin-bottom:12px;display:block;margin-left:auto;margin-right:auto;" alt="RGB2Go">
```

Text remains WLED-centered (`Welcome to WLED!`, `A versatile tool for controlling LEDs`, `Find out more at wled.me`).

### `wled00/html_*.h` and `wled00/js_*.h` — added generated web assets

These are autogenerated C/C++ header blobs from web UI files. They are source-tree additions in the archive, but the comments say not to edit them manually.

Added files and decoded contents:

- `wled00/html_cpal.h` — generated from `wled00/data/cpal/cpal.htm`; page title `WLED Palette Editor`.
- `wled00/html_edit.h` — generated from `wled00/data/edit.htm`; page title `WLED File Editor`.
- `wled00/html_other.h` — contains generated `usermod`, `msg`, `dmxmap`, `update`, `welcome`, `liveview`, `404`, `favicon`; decoded `welcome` includes RGB2Go image.
- `wled00/html_pixart.h` — new generated page `WLED Pixel Art Converter`; defines `WEB_BUILD_TIME 1780418974` and `PAGE_pixart_length = 7464`.
- `wled00/html_pixelforge.h` — new generated page `WLED PixelForge`; defines `WEB_BUILD_TIME 1780418974` and `PAGE_pixelforge_length = 11041`; includes/mentions `omggif`.
- `wled00/html_pxmagic.h` — new generated page `Pixel Magic Tool`; defines `WEB_BUILD_TIME 1780418974` and `PAGE_pxmagic_length = 8701`.
- `wled00/html_settings.h` — generated settings pages and common JS/CSS; decoded WiFi settings include RGB2Go content/branding.
- `wled00/html_ui.h` — generated main UI; decoded page title `WLED`; includes PixelForge references; defines `WEB_BUILD_TIME 1780418974` and `PAGE_index_length = 39668`.
- `wled00/js_iro.h` — generated `iro.js` color picker library blob.
- `wled00/js_omggif.h` — generated `pixelforge/omggif.js` blob.

Carry-forward note: the **real editable source** for these generated blobs is normally under `wled00/data/`. In this archive, the added generated headers are present, but the corresponding editable source files for PixelForge/PixArt/PxMagic are not present as plain files except `welcome.htm`. Preserve either these generated headers or, preferably, the original editable `wled00/data/...` source pages when moving to a future WLED version.

### `wled00/my_config.h` — added

Adds a default/sample-style `my_config.h` file. It does not define active custom settings; all shown config lines are comments. `WLED_USE_MY_CONFIG` remains commented out in `wled00/wled.h`, so this file is likely inert unless future build flags include it.

### `package.json` — modified

Only reorders dependencies:

```diff
-"web-resource-inliner": "^7.0.0",
-"nodemon": "^3.1.14"
+"nodemon": "^3.1.14",
+"web-resource-inliner": "^7.0.0"
```

No version changes. `package-lock.json` matches vanilla.

### `tools/wled-tools` — mode changed

File content is unchanged, but executable permission was removed:

```diff
-old mode 100755
-new mode 100644
```

Carry-forward note: likely accidental from Windows/archive handling. If this script should remain runnable on Linux/macOS, keep executable mode `100755`.

## Full patch artifacts

Generated alongside this document:

- `source-full.diff` — exact diff after excluding `node_modules`, `.pio`, and `build_output`.
- `source-diff-stat.txt` — compact stats.
- `source-name-status.txt` — changed file list.
- `key-diffs.txt` — readable hunks for the small hand-edited files.
- `full.diff` — raw complete diff including generated dependency files; very noisy.

## Suggested future-port checklist

When rebasing these customizations to a later WLED release, verify these items explicitly:

- [ ] Recreate/update `platformio_override.ini` environments for Matrix/Solo/Duo/Tetra/Octa variants.
- [ ] Confirm Ethernet builds still define the correct Ethernet type (`WLED_ETH_ESP32DEUX`) and `WLED_DISABLE_ESPNOW` where needed.
- [ ] Reapply or retest the `delay(1000)` Ethernet boot workaround.
- [ ] Reapply `AP_BEHAVIOR_ALWAYS` if that behavior is still desired.
- [ ] Reapply audio-reactive defaults: decay `80`, I2S pins `25/26/27`.
- [ ] Reapply RGB2Go welcome branding.
- [ ] Preserve or regenerate PixelForge / Pixel Art / PxMagic web pages and the generated header blobs.
- [ ] Decide whether `tools/wled-tools` should keep executable mode.
- [ ] Do not carry forward `node_modules`, `.pio`, or empty `build_output` directories into source control/reference archives.
