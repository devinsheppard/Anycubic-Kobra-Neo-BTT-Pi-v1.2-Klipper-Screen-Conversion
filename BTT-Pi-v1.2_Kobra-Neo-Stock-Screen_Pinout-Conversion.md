# Anycubic Kobra Neo Stock Screen to BTT Pi v1.2 Pinout Conversion

This document converts the Raspberry Pi wiring used by the `Anycubic-Kobra-Go-Neo-LCD-Driver` project to likely equivalent pins on **BTT Pi v1.2**.

## Scope

- **Purpose:** repurpose the stock Anycubic Kobra Neo LCD so it can be driven by a host running KlipperScreen-style software.
- **Board target:** **BTT Pi v1.2**.
- **Important:** this is a **physical wiring** conversion, not only a software/config change.
- **Important:** the existing LCD driver project is written for Raspberry Pi assumptions, so the **pin mapping below is the hardware starting point only**. Software changes will likely still be needed.

## Stock Anycubic Kobra Neo LCD signals

The Kobra Go/Neo LCD driver project documents these display-side signals:

| LCD signal | Function |
|---|---|
| 5V | Power |
| GND | Ground |
| SCK | SPI clock |
| MOSI | SPI data from host to display |
| CS | Chip select |
| RESET | LCD reset |
| DC | Data/command select |

Notes:
- The driver project states that the LCD uses **SPI**.
- The project notes that **DC is marked as MISO on the mainboard side**, but is used by the driver as **DC**, not as true SPI MISO.
- The project ignores the rotary encoder pins because KlipperScreen uses touch input.

## Original Raspberry Pi mapping from the LCD driver project

| LCD signal | Raspberry Pi mapping |
|---|---|
| 5V | 5V |
| GND | GND |
| SCK | GPIO 11 / SPI SCLK |
| MOSI | GPIO 10 / SPI MOSI |
| CS | GPIO 8 / SPI CE0 |
| RESET | GPIO 25 |
| DC | GPIO 24 |

## Likely BTT Pi v1.2 conversion

The BTT Pi v1.2 / CB1 family does **not** use Raspberry Pi GPIO numbering, so the Raspberry Pi guide cannot be followed directly.

### Recommended starting map

| LCD signal | Raspberry Pi target in the original guide | BTT Pi v1.2 physical pin | BTT Pi v1.2 signal name | Notes |
|---|---|---:|---|---|
| 5V | 5V | 2 or 4 | 5V | Power |
| GND | GND | 6, 9, 14, 20, 25, 30, 34, or 39 | GND | Ground |
| SCK | GPIO11 / SPI SCLK | 23 | PH6 / GPIO230 / SPI1_CLK | Use as SPI clock |
| MOSI | GPIO10 / SPI MOSI | 19 | PH7 / GPIO231 / SPI1_MOSI | Use as SPI MOSI |
| CS | GPIO8 / SPI CE0 | 24 | PG12 / GPIO204 | Suggested manual CS GPIO |
| RESET | GPIO25 | 22 | PG13 / GPIO205 | Suggested reset GPIO |
| DC | GPIO24 | 18 | PC9 / GPIO73 | Suggested data/command GPIO |

## What this means in plain English

If you are following the original Raspberry Pi LCD project:

- Raspberry Pi **pin 19 (MOSI)** becomes **BTT Pi pin 19**
- Raspberry Pi **pin 23 (SCLK)** becomes **BTT Pi pin 23**
- Raspberry Pi **pin 24 (CE0/CS)** does **not** translate by numbering alone; use **BTT Pi pin 24 as a normal GPIO-based chip select candidate**
- Raspberry Pi **GPIO24 (used for DC in the project)** becomes **BTT Pi pin 18 / PC9 / GPIO73**
- Raspberry Pi **GPIO25 (used for RESET in the project)** becomes **BTT Pi pin 22 / PG13 / GPIO205**

## Practical wiring summary

### LCD -> BTT Pi v1.2

| LCD | BTT Pi v1.2 |
|---|---|
| 5V | pin 2 or 4 |
| GND | pin 6 |
| SCK | pin 23 |
| MOSI | pin 19 |
| CS | pin 24 |
| RESET | pin 22 |
| DC | pin 18 |

## Software caveats

This is the biggest risk area.

1. The LCD driver project is a Raspberry Pi-oriented fork of `fbcp-ili9341`.
2. BTT Pi v1.2 uses a different GPIO model and different board setup than a standard Raspberry Pi.
3. Even if the wiring is correct, you will likely need to:
   - enable SPI on the BTT Pi OS using its own board configuration method
   - remap GPIO references in the driver/build config
   - adjust any Raspberry Pi-specific setup steps and services

## Confidence / uncertainty

### High confidence
- The Kobra Go/Neo LCD project expects these LCD signals: `5V`, `GND`, `SCK`, `MOSI`, `CS`, `RESET`, `DC`.
- BTT Pi v1.2 / CB1 family does not use Raspberry Pi GPIO numbering.
- BTT Pi exposes `SPI1_CLK` and `SPI1_MOSI` on physical pins `23` and `19`.

### Moderate confidence
- `pin 24 / PG12 / GPIO204` is a sensible **manual CS** candidate.
- `pin 22 / PG13 / GPIO205` is a sensible **RESET** candidate.
- `pin 18 / PC9 / GPIO73` is a sensible **DC** candidate.

### Lower confidence
- The unmodified Raspberry Pi LCD driver will compile and run cleanly on BTT Pi v1.2 without porting.

## Suggested repo note

Recommended wording for this project:

> This pinout conversion provides the likely physical wiring needed to connect the stock Anycubic Kobra Neo LCD to a BTT Pi v1.2. It does **not** guarantee that the original Raspberry Pi-targeted LCD driver will run unchanged on BTT Pi v1.2. Driver and board-config changes may still be required.

## Sources

- Anycubic Kobra Go/Neo LCD Driver project: https://github.com/jokubasver/Anycubic-Kobra-Go-Neo-LCD-Driver
- BIGTREETECH CB1 repository / pinout documentation: https://github.com/bigtreetech/CB1
- BIGTREETECH BTT-Pi repository: https://github.com/bigtreetech/BTT-Pi
- CB1 discussion noting custom 40-pin IO naming: https://github.com/bigtreetech/CB1/discussions/47
