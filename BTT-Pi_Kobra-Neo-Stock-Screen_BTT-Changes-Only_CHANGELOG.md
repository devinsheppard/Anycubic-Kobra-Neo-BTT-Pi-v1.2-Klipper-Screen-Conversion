# BTT Pi Changes-Only Changelog

This file documents the changes needed when adapting the original Raspberry Pi-oriented Anycubic Kobra Go/Neo stock LCD project to **BTT Pi v1.2 / CB1-style hardware and software**.

## Summary

The original project is written for a Raspberry Pi-style environment. This BTT Pi port changes the board assumptions, SPI exposure method, GPIO mapping, deployment conventions, and overall project strategy.

---

## 1. Boot/overlay configuration change

### Original Raspberry Pi-style assumption
- Raspberry Pi-oriented boot configuration and SPI assumptions.

### BTT Pi change
- Use **`/boot/BoardEnv.txt`** instead of Raspberry Pi `config.txt` conventions.
- Expose SPI to userspace with:

```ini
overlays=spidev1_2
```

### Why
BTT Pi / CB1 uses a different boot overlay model than standard Raspberry Pi instructions.

---

## 2. SPI device path change

### Original assumption
- Pi-style device paths such as `/dev/spidev0.0` or `/dev/spidev0.1` may be assumed.

### BTT Pi change
- Use:

```text
/dev/spidev1.2
```

### Why
This matches the SPI userspace exposure chosen for the BTT Pi port.

---

## 3. GPIO / pin mapping change

### Original assumption
- Raspberry Pi GPIO numbering and Raspberry Pi header assumptions.

### BTT Pi change
Use this BTT Pi v1.2 mapping as the starting point:

| LCD signal | BTT Pi pin | BTT Pi signal |
|---|---:|---|
| 5V | 2 or 4 | 5V |
| GND | 6, 9, 14, 20, 25, 30, 34, or 39 | GND |
| SCK | 23 | PH6 / SPI1_CLK |
| MOSI | 19 | PH7 / SPI1_MOSI |
| CS | 24 | PG12 / GPIO204 |
| RESET | 22 | PG13 / GPIO205 |
| DC | 18 | PC9 / GPIO73 |

### Build values used for initial BTT Pi test

```bash
cmake .. \
  -DGPIO_TFT_DATA_CONTROL=73 \
  -DGPIO_TFT_RESET_PIN=205
```

### Alternate test if needed

```bash
cmake .. \
  -DGPIO_TFT_DATA_CONTROL=205 \
  -DGPIO_TFT_RESET_PIN=73
```

---

## 4. Strategy change: from “drop-in install” to “porting project”

### Original assumption
- The original repo is oriented around a Raspberry Pi target.

### BTT Pi change
- Treat the project as a **porting effort**.
- Separate the work into:
  1. SPI/display bring-up
  2. source cleanup
  3. panel-only tests
  4. replacement of the capture path if needed

### Why
BTT Pi is not a drop-in Raspberry Pi replacement for this project’s software assumptions.

---

## 5. Capture-path handling change

### Original assumption
- The inherited framebuffer/capture path comes from a Raspberry Pi-centered `fbcp-ili9341` architecture.

### BTT Pi change
- If the inherited capture path fails, bypass it.
- Test the LCD with:
  - dummy full-screen frames
  - repeating generated frames
  - simple custom status layouts

### Why
This separates:
- “Can the LCD be driven?”
from
- “Can the inherited Raspberry Pi capture code still work here?”

---

## 6. UI goal change

### Original assumption
- The original project aims to repurpose the stock LCD as part of a Raspberry Pi-driven display setup.

### BTT Pi change
- Prefer this practical goal:

**custom Moonraker status screen on the stock Kobra Neo LCD**

instead of trying to force full original-screen behavior or full KlipperScreen mirroring first.

### Why
This is the most realistic high-value result on BTT Pi.

---

## 7. Rotary/button change

### Original assumption
- Display first; control/input is a separate problem.

### BTT Pi change
- Make rotary/button support **Phase 2**.
- First stabilize the display.
- Then add encoder/button handling for simple actions such as:
  - page switching
  - select/confirm
  - back

### Why
This keeps display failures separate from input failures.

---

## 8. Deployment change

### Original assumption
- Original service model is based around the original project’s intended environment.

### BTT Pi change
- Use a clean BTT Pi deployment layout with:
  - project under `/home/biqu/...`
  - launcher script
  - dedicated `systemd` service
  - optional log directory

Recommended service name:

```text
kobra-neo-lcd.service
```

---

## 9. Recommended safety addition

### New BTT Pi project recommendation
Before starting the port:
- clone or image your current SD card

### Why
This is experimental work and gives you a known-good rollback point.

---

## 10. Recommended final milestone

The recommended practical milestone for this BTT Pi port is:

**boot-time custom stock-screen status display with optional rotary/button navigation**

That is the cleanest realistic endpoint for the project.
