# RGB2Go GitHub Actions firmware builds

This repo can build RGB2Go WLED firmware on GitHub instead of using local/Hermes compute.

## Cost-control strategy

The workflow is intentionally **manual-only** by default. It does not compile all firmware on every push.

Use GitHub Actions only when firmware binaries are actually needed:

1. Open the repo on GitHub.
2. Go to **Actions**.
3. Select **Build RGB2Go WLED firmware**.
4. Click **Run workflow**.
5. Choose a small build set when possible.

Recommended build sets:

| Build set | Use when |
|---|---|
| `single` | One controller changed. Lowest GitHub minutes. |
| `changed-defaults` | Recent default/config work: Tetra2Go-Eth plus OLED builds. Good default. |
| `oled` | OLED display/usermod changes. |
| `ethernet` | Ethernet-related changes. |
| `dmx` | DMX-related changes. |
| `base` | Main non-OLED/non-Ethernet product builds. |
| `all` | Release candidate / final release only. |

The workflow builds environments sequentially in one job. This is slower wall-clock time than a large matrix, but it avoids repeating setup work in many jobs and is friendlier to GitHub free-minute limits.

## Outputs

Every run uploads a short-lived GitHub Actions artifact containing:

- selected `.bin` firmware files
- `SHA256SUMS.txt`
- a firmware `.tar.gz`
- build logs
- the selected environment list

Artifact retention is 14 days to avoid accumulating storage.

## Optional release upload

Set `upload_to_release=true` and provide a `release_tag` such as:

```text
v16.0.1-rgb2go
```

The workflow will create the release if needed and upload/replace:

- selected `.bin` files
- `SHA256SUMS.txt`
- firmware archive
- archive checksum

## Hermes/Codex usage model

To conserve Codex credits, Hermes should normally:

1. Edit source/config only.
2. Push changes.
3. Trigger or ask Jason to trigger the GitHub Action.
4. Monitor GitHub Actions logs/status.
5. Fix only if the GitHub build fails.
6. Update `wled-flasher` from released firmware only after GitHub produces verified binaries.

Local PlatformIO builds should be reserved for urgent debugging or when GitHub Actions is unavailable.
