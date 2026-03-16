# Encoder Setup Guide for BTT Pi v1.2 + Anycubic Kobra Neo Stock Screen

## Purpose

This guide covers the **rotary encoder / push-button phase** of the project.

Do **not** start here first.

Bring up the LCD/display path first. Only move to encoder support **after** the stock screen is already proving it can display output on the BTT Pi.

---

## Important warning

The upstream encoder project used by the Kobra Go/Neo stock-screen ecosystem was written around a **Raspberry Pi-style GPIO approach**.

On **BTT Pi v1.2 / CB1**, the 40-pin header is **not software-compatible with normal Raspberry Pi GPIO numbering**.

That means:

- the upstream encoder project is the right **starting design**
- but you should treat BTT Pi encoder support as a **port**
- do **not** assume the stock upstream script will run unchanged on BTT Pi

---

## Step 1 — Clone your current SD card first

Before changing anything, it is strongly recommended that you **clone your current working SD card / boot media**.

Reason:
- encoder support is a second-phase feature
- the upstream encoder project is Raspberry Pi-oriented
- on BTT Pi, this is a porting task, not a known drop-in install

If something breaks, your clone gives you a clean rollback point.

---

## Step 2 — Finish the display path first

Do not continue to the encoder phase until all of these are already true:

- the stock Kobra Neo LCD is physically wired to the BTT Pi
- the display path is proven working
- your current LCD program starts successfully
- the screen reliably shows test frames or your custom status layout

If the screen itself is not working yet, stop here and finish the LCD bring-up first.

---

## Step 3 — Add the upstream encoder project to your repo

Use the upstream encoder project only as a starting point.

Recommended place in your repo:

```text
third_party/KlipperScreen-Encoder-Driver/
```

You can either:
- add it as a git submodule, or
- copy it in while keeping attribution/license information intact

Do **not** mix third-party source directly into your top-level project files.

---

## Step 4 — BTT Pi pin conversion for the encoder

The upstream encoder project assumes Raspberry Pi-style pins for:

- button / switch
- encoder A
- encoder B

For the BTT Pi v1.2 40-pin header, the cleanest conversion is:

- **Switch** -> physical pin **15** -> **GPIO74**
- **Encoder A** -> physical pin **13** -> **GPIO76**
- **Encoder B** -> physical pin **11** -> **GPIO78**
- **Ground** -> any ground pin

### Wiring summary

```text
Encoder switch -> BTT Pi pin 15 -> GPIO74
Encoder A      -> BTT Pi pin 13 -> GPIO76
Encoder B      -> BTT Pi pin 11 -> GPIO78
Encoder GND    -> any GND
```

This preserves the same physical-header concept while using the BTT Pi's actual GPIO numbering.

---

## Step 5 — Add a BTT-specific patched script in your repo

Do not overwrite the third-party script immediately.

Instead create your BTT-specific version separately, for example:

```text
patches/EncoderMouse-BTT.py
```

Why:
- keeps upstream code separate
- makes your changes easier to document
- makes future diffing much easier

---

## Step 6 — Install the Linux input dependency

The upstream encoder project uses Linux input-event injection.

Install the dependency it expects:

```bash
sudo python3 -m pip install evdev
```

---

## Step 7 — Understand what must be patched

The upstream encoder script was built around:
- Raspberry Pi assumptions
- Pi-style GPIO numbering
- a GPIO access model that may not work unchanged on BTT Pi / CB1

For BTT Pi, the BTT-specific script should be treated as a **port**.

At minimum, your BTT version should reflect:

- switch line = `74`
- encoder A line = `76`
- encoder B line = `78`

Recommended constants for the BTT version:

```python
PIN_BUTTON = 74
PIN_A = 76
PIN_B = 78
```

### Important note

This guide does **not** claim that the upstream Raspberry Pi script will work unchanged on BTT Pi.

It only documents the correct direction for the BTT mapping and how to structure the repo for a clean port.

---

## Step 8 — Create a dedicated systemd service for the BTT version

Use a BTT-specific service file rather than pointing a service at the unmodified upstream script.

Recommended service file path on the system:

```text
/etc/systemd/system/EncoderMouse.service
```

Recommended target script path:

```text
/home/biqu/Anycubic-Kobra-Neo-BTT-Pi-v1.2-Klipper-Screen-Conversion/patches/EncoderMouse-BTT.py
```

A starter service file is included separately in this repo package.

---

## Step 9 — Enable cursor support in KlipperScreen

If the encoder is meant to emulate pointer movement for KlipperScreen, make sure your `KlipperScreen.conf` contains:

```ini
show_cursor: True
```

---

## Step 10 — Test expected behavior

Once the BTT-patched version is installed and the service is running, the intended behavior should be:

- rotate encoder -> move pointer
- press button -> change movement mode or trigger input action, depending on your ported logic
- hold button -> optional click/selection behavior if you implement that in the BTT script

Do not assume all upstream behaviors are automatically preserved until the BTT-specific script is actually tested.

---

## Step 11 — Recommended files to commit

At minimum, commit:

```text
docs/ENCODER-SETUP.md
third_party/KlipperScreen-Encoder-Driver/
patches/EncoderMouse-BTT.py
```

Also recommended:

```text
docs/BTT-PI-CHANGES-CHANGELOG.md
docs/PORTING-GUIDE.md
```

---

## Step 12 — Honest status of this phase

What is solid:
- repo placement
- README/doc link paths
- BTT Pi pin mapping for switch/A/B
- service-file strategy
- second-phase sequencing after LCD bring-up

What is still porting work:
- the actual BTT-compatible encoder script
- exact GPIO library choice on BTT Pi
- validating click/hold/axis-toggle behavior on hardware

That means the next step after adding these repo files is to build the **BTT-specific encoder script** rather than assuming the upstream Raspberry Pi version is ready as-is.
