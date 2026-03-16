# Anycubic Kobra Neo Stock Screen on BTT Pi v1.2

This repo documents an experimental port of the **Anycubic Kobra Neo stock LCD** from its original **Raspberry Pi-oriented** setup to **BTT Pi v1.2 / CB1**.

The original Kobra Go/Neo LCD project is based on a Raspberry Pi path for the stock **ST7796 SPI TFT** and has Raspberry Pi-specific assumptions in its setup and software flow. This repo tracks the changes needed to adapt that work toward BTT Pi v1.2, starting with SPI overlay setup and pin remapping, then moving into source inspection and replacement of Raspberry Pi-only capture logic where needed. The original project also notes that the stock LCD is not touch by itself, so rotary/encoder support is treated here as a later phase after basic display bring-up. ([Kobra Go/Neo LCD Driver](https://github.com/jokubasver/Anycubic-Kobra-Go-Neo-LCD-Driver))

BIGTREETECH’s CB1/BTT Pi documentation uses **`/boot/BoardEnv.txt`** overlays such as **`spidev1_2`** to expose SPI devices to userspace, which is one of the main reasons the Raspberry Pi instructions do not carry over unchanged. ([BIGTREETECH CB1 docs](https://github.com/bigtreetech/docs/blob/master/docs/CB1.md))

## Important first recommendation

Before starting this project, **clone or image your current working SD card / system storage**.

This project involves:
- editing boot overlay settings
- testing SPI devices
- building and modifying display-driver code
- possibly changing service startup behavior

If the display path, boot config, or service configuration goes wrong, having a known-good backup makes recovery much easier.

## What this repo is for

This repo is organized around these goals:

1. Convert the stock-screen wiring/pin mapping from Raspberry Pi assumptions to BTT Pi v1.2.
2. Enable the needed SPI userspace device on BTT Pi.
3. Test whether the original LCD driver can be built and run on BTT Pi.
4. Separate **panel-path issues** from **Raspberry Pi-only capture-path issues**.
5. If needed, keep the working LCD/ST7796 path and replace the old Raspberry Pi capture path.
6. Move toward a practical end result such as a **custom Moonraker status screen**.
7. Add **rotary/button support** only after the display side is proven stable.

## Recommended roadmap

### Step 1 — Back up your current system first
Clone your working SD card or storage before you start.

### Step 2 — Enable BTT Pi SPI userspace overlay
Edit **`/boot/BoardEnv.txt`** and enable the SPI overlay needed for userspace access.

### Step 3 — Convert the pin mapping
Use the BTT Pi mapping rather than the Raspberry Pi numbering used by the original project.

### Step 4 — Build and manually test the LCD driver
Do not install it as a service first. Prove that it can compile and run manually.

### Step 5 — Determine whether the blocker is panel-side or capture-side
If the panel works with dummy frames, keep the LCD path and replace the old capture path.

### Step 6 — Build a minimal custom status screen
A custom Moonraker status display is the most realistic and useful near-term target.

### Step 7 — Add rotary/button support later
The stock LCD itself is not touch, so interactive control is a separate second phase.

## Files to read first

- **Pinout conversion** — maps Raspberry Pi assumptions to BTT Pi v1.2
- **Step 1 overlay/setup notes** — enables SPI userspace access on BTT Pi
- **Main porting guide** — full step-by-step guide from backup through deployment
- **BTT changes changelog** — separate list of changes from the original Raspberry Pi path

## Rotary / button support

The original stock-screen path is not a touch UI by itself. If you want the **rotary encoder / button** to be usable, treat that as a second phase after the display path is proven working. The ecosystem around the Kobra Go/Neo LCD includes encoder-focused work intended to make knob-based interaction possible, but that should come **after** LCD bring-up, not before. ([Encoder-support fork](https://github.com/MrBult/Anycubic-Kobra-Go-Neo-LCD-Driver))

Recommended order:
1. get the LCD to light and draw reliably
2. prove repeated frame updates work
3. build a minimal status screen
4. only then add rotary/button handling

## Best realistic end goal

The most practical target for this hardware path is:

**a boot-time custom Moonraker status screen on the stock Kobra Neo LCD, running from the BTT Pi**

That is more realistic than trying to fully mirror a Raspberry Pi/KlipperScreen stack originally built around older Raspberry Pi display assumptions.

## Related docs

- [Original Kobra Go/Neo LCD driver](https://github.com/jokubasver/Anycubic-Kobra-Go-Neo-LCD-Driver)
- [BIGTREETECH CB1 / BTT Pi documentation](https://github.com/bigtreetech/docs/blob/master/docs/CB1.md)

## Repo note

This README is intended to be the **front-page overview**.

It does **not** replace the more detailed technical docs unless you want it to. In most cases, the best structure is:
- keep this `README.md` as the front page
- keep the detailed guide as a separate markdown doc
- keep the BTT-only changelog as a separate markdown doc

That gives visitors a clean landing page while preserving the deeper step-by-step notes elsewhere in the repo.
