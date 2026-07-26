# RGB2Go WLED Custom Build

Private RGB2Go customization of WLED, currently rolled forward to WLED `16.0.1`.

## Current release

- Source base: WLED `v16.0.1`
- RGB2Go release tag: `v16.0.1-rgb2go`
- Default PlatformIO environments from `platformio_override.ini`:
  - `octa2go_esp32_eth`
  - `solo2go_esp32_eth`
  - `solo2go_esp32_eth_dmx`
  - `tetra2go_esp32_eth`

## Key customizations

- RGB2Go PlatformIO board environments for Matrix/Solo/Duo/Tetra/Octa variants.
- RGB2Go welcome-page branding.
- Audio-reactive defaults: decay `80`, I2S pins `25/26/27`.
- Ethernet boot workaround: `delay(1000)` before Ethernet init.
- Default AP behavior set to `AP_BEHAVIOR_ALWAYS`.

See `docs/rgb2go/` for detailed roll-forward notes and the original 16.0.0 customization reference.

## Build verification

This `16.0.1` roll-forward was verified with:

```bash
npm ci
npm run build
npm test
pio run
```

Node tests passed and the four default custom PlatformIO environments built successfully.
