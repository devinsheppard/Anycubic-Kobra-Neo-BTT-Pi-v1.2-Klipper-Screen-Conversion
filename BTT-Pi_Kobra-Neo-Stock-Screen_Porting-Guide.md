# BTT Pi + Anycubic Kobra Neo Stock Screen Porting Guide

## Step 1 — Before you start

### Clone your current SD card first

Before doing anything else, it is **strongly recommended** that you clone or image your current working SD card.

Why:
- this project is experimental
- you may need to undo overlay, build, and service changes
- it gives you a known-good rollback point if the screen project breaks boot or conflicts with your current setup

Good practice:
1. Shut the system down cleanly.
2. Remove the SD card.
3. Make a full image backup on another machine.
4. Label the backup clearly.
5. Do not continue until you know you can restore it.

### Project goal

The realistic goal is **not** “make the stock Kobra Neo screen behave exactly like the original Anycubic screen under Klipper.”

The realistic goal is:
- first, prove the stock LCD can be driven from the BTT Pi
- then, make it show useful content
- then, optionally add rotary/button input

### Important expectations

This project is based on the Anycubic Kobra Go/Neo stock LCD driver project, which is a Raspberry Pi-oriented fork for the stock ST7796 LCD. On BTT Pi, this is a **porting project**, not a known turnkey install.

---

## Step 2 — Enable SPI userspace access on BTT Pi

Edit:

```bash
sudo nano /boot/BoardEnv.txt
```

Add or edit the overlays line so it includes:

```ini
overlays=spidev1_2
```

Important:
- if you already have other overlays, keep them on the **same** `overlays=` line
- do not create multiple active `overlays=` lines unless you know the image handles that correctly
- avoid SPI1 overlay conflicts while testing

Save, then reboot:

```bash
sudo reboot
```

After reboot, verify:

```bash
ls -l /dev/spidev*
```

You want to see:

```text
/dev/spidev1.2
```

---

## Step 3 — Clone and do a first driver build test

Install tools:

```bash
sudo apt update
sudo apt install -y git cmake build-essential
```

Clone the original LCD driver repo:

```bash
cd ~
git clone https://github.com/jokubasver/Anycubic-Kobra-Go-Neo-LCD-Driver.git
cd Anycubic-Kobra-Go-Neo-LCD-Driver
```

Create build dir:

```bash
mkdir -p build
cd build
```

First BTT Pi build test:

```bash
cmake .. \
  -DGPIO_TFT_DATA_CONTROL=73 \
  -DGPIO_TFT_RESET_PIN=205

make -j$(nproc)
```

Run first manual test:

```bash
sudo ./fbcp-ili9341
```

Capture log if needed:

```bash
sudo ./fbcp-ili9341 2>&1 | tee ~/fbcp-first-test.log
```

---

## Step 4 — BTT Pi pin mapping used for this port

### Stock LCD signals expected by the original project

- 5V
- GND
- SCK
- MOSI
- CS
- RESET
- DC

### BTT Pi v1.2 mapping used as the starting point

| LCD signal | BTT Pi pin | BTT Pi signal |
|---|---:|---|
| 5V | 2 or 4 | 5V |
| GND | 6, 9, 14, 20, 25, 30, 34, or 39 | GND |
| SCK | 23 | PH6 / SPI1_CLK |
| MOSI | 19 | PH7 / SPI1_MOSI |
| CS | 24 | PG12 / GPIO204 |
| RESET | 22 | PG13 / GPIO205 |
| DC | 18 | PC9 / GPIO73 |

This is the **port target**, not proof that the original Raspberry Pi code already understands these values.

---

## Step 5 — If it builds but the screen stays blank

Do these in order:

1. Re-check your physical wiring.
2. Confirm `/dev/spidev1.2` still exists.
3. Try swapping DC and RESET build values:

```bash
rm -rf build
mkdir build
cd build

cmake .. \
  -DGPIO_TFT_DATA_CONTROL=205 \
  -DGPIO_TFT_RESET_PIN=73

make -j$(nproc)
sudo ./fbcp-ili9341
```

4. Capture logs and search for:
- `spidev`
- `spi`
- `gpio`
- `bcm_host`
- `dispmanx`
- `vc_`

If you see `bcm_host` or `dispmanx`, the blocker is probably the inherited Raspberry Pi display path rather than basic wiring.

---

## Step 6 — Inspect the source for Raspberry Pi-only assumptions

From the repo root, search:

```bash
grep -Rin "bcm_host\|dispmanx\|vc_dispmanx\|graphics_get_display_size\|spidev\|CE0\|CE1" .
```

Pay special attention to:
- `CMakeLists.txt`
- `gpu.cpp`
- `display.cpp`
- `st7796.cpp`

You are looking for:
- hardcoded `/dev/spidev0.0` or `/dev/spidev0.1`
- Pi-only APIs like `bcm_host`
- chip-select assumptions tied to Pi CE0/CE1 behavior

---

## Step 7 — First source edits to try

### Replace Pi-style SPI device paths

Search:

```bash
grep -Rin "/dev/spidev\|spidev[0-9]\.[0-9]" .
```

If the code hardcodes `/dev/spidev0.0` or `/dev/spidev0.1`, replace them with:

```text
/dev/spidev1.2
```

Quick patch:

```bash
grep -Ril "/dev/spidev0.0" . | xargs -r sed -i 's#/dev/spidev0.0#/dev/spidev1.2#g'
grep -Ril "/dev/spidev0.1" . | xargs -r sed -i 's#/dev/spidev0.1#/dev/spidev1.2#g'
```

### Rebuild and retest

```bash
rm -rf build
mkdir build
cd build

cmake .. \
  -DGPIO_TFT_DATA_CONTROL=73 \
  -DGPIO_TFT_RESET_PIN=205

make -j$(nproc)
sudo ./fbcp-ili9341 2>&1 | tee ~/fbcp-step7.log
```

---

## Step 8 — Panel-init tuning

If SPI open errors go away but the panel still stays blank, inspect `st7796.cpp`.

Look for:
- reset timing
- command/data handling
- init sequence timing
- color order / orientation handling

Conservative first tweak:
- modestly increase post-reset and post-sleep-exit delays
- do **not** rewrite the whole init table first

Back up first:

```bash
cp st7796.cpp st7796.cpp.bak
```

---

## Step 9 — Separate panel problems from capture-path problems

If logs show:
- `bcm_host`
- `dispmanx`
- `vc_dispmanx`
- `graphics_get_display_size`

then the code is probably failing in the **capture path**, not the LCD path.

That means panel tweaks alone will not finish the port.

If logs show:
- successful open of `/dev/spidev1.2`
- no Pi-only display-stack errors
- but the panel stays white or blank

then the remaining problem is more likely still on the panel path.

---

## Step 10 — Create a dummy test-frame path

If the inherited capture path is the blocker, bypass it and feed a fake image to the LCD write path.

Best first test:
- fill the full screen with one RGB565 color, such as red (`0xF800`)

Concept:

```cpp
for (int i = 0; i < width * height; ++i)
    framebuffer[i] = 0xF800;
```

If the screen reacts, that proves the LCD side is alive even if the Pi capture side is not.

---

## Step 11 — Replace the one-shot dummy frame with a repeating generated frame

Once a single fake frame works, make it alternate between two colors, for example red and green once per second.

Concept:

```cpp
static bool toggle = false;
toggle = !toggle;
uint16_t color = toggle ? 0xF800 : 0x07E0;
for (int i = 0; i < width * height; ++i)
    framebuffer[i] = color;
```

This proves redraws work, not just one startup frame.

---

## Step 12 — Replace the generated frame with a simple status layout

Once repeated redraw works, replace the flat fill with a simple structured layout.

Good first layout:
- black background
- red title bar
- green center box
- blue footer bar

This tells you:
- orientation correctness
- color correctness
- whether region-based drawing works

---

## Step 13 — Build a minimal custom status screen

Before attempting full Linux mirroring or KlipperScreen, build a minimal custom status page.

Recommended first screen:
- title: `KOBRA NEO`
- host line
- IP line
- printer state line
- nozzle temp line
- bed temp line
- footer: `BTT PI`

At first, fake values are fine.

---

## Step 14 — Replace fake values with real values

Add real data in this order:

1. local system data
   - hostname
   - IP address
   - time
2. Moonraker data
   - printer state
   - nozzle temp
   - bed temp
   - print percent
   - job name

Keep the draw code separate from the data-fetch code.

---

## Step 15 — Stabilize the update loop

Recommended redraw policy:
- redraw once per second, or every 2 seconds
- redraw immediately when key values change
- show fallback text when Moonraker is unavailable

Examples:
- `STATE: NO DATA`
- `MOONRAKER: OFFLINE`
- `IP: UNKNOWN`

---

## Step 16 — Rotary/button input phase

### Important

Do **not** try to solve rotary/button input before the display path is stable.

### Practical recommendation

Treat rotary/button support as **Phase 2**:
1. bring up the display first
2. prove the status screen works first
3. only then add encoder/button support

### Goal of this phase

Make the stock rotary/button usable for simple actions such as:
- page switching
- select / confirm
- back
- simple menu navigation

### Realistic target

A small custom menu or status-page selector is much more realistic than trying to recreate the full original Anycubic UI.

### Suggested first-use cases for the rotary/button

- rotate to switch pages
- press to select page
- hold to return to main page

### Why this order matters

If you add input before the display path is reliable, you won’t know whether a failure is caused by:
- display updates
- event handling
- encoder handling
- redraw timing

---

## Step 17 — Package it to start on boot

Create launcher script:

```bash
nano /home/biqu/Anycubic-Kobra-Go-Neo-LCD-Driver/start-lcd.sh
```

Contents:

```bash
#!/bin/bash
set -e
cd /home/biqu/Anycubic-Kobra-Go-Neo-LCD-Driver/build
exec /home/biqu/Anycubic-Kobra-Go-Neo-LCD-Driver/build/fbcp-ili9341
```

Make it executable:

```bash
chmod +x /home/biqu/Anycubic-Kobra-Go-Neo-LCD-Driver/start-lcd.sh
```

Create service:

```bash
sudo nano /etc/systemd/system/kobra-neo-lcd.service
```

Contents:

```ini
[Unit]
Description=Kobra Neo Stock LCD on BTT Pi
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=biqu
WorkingDirectory=/home/biqu/Anycubic-Kobra-Go-Neo-LCD-Driver/build
ExecStart=/home/biqu/Anycubic-Kobra-Go-Neo-LCD-Driver/start-lcd.sh
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable kobra-neo-lcd.service
sudo systemctl start kobra-neo-lcd.service
systemctl status kobra-neo-lcd.service
```

View service logs:

```bash
journalctl -u kobra-neo-lcd.service -n 100 --no-pager
```

---

## Step 18 — Recommended repo structure

Recommended layout:

```text
.
├── README.md
├── BTT-Pi_Kobra-Neo-Stock-Screen_Porting-Guide.md
├── BTT-Pi_Kobra-Neo-Stock-Screen_BTT-Changes-Only_CHANGELOG.md
├── start-lcd.sh
├── systemd/
│   └── kobra-neo-lcd.service
├── logs/
└── build/
```

---

## Step 19 — Recommended practical end goal

The most realistic and useful finished target is:

**custom boot-time Moonraker status screen on the stock Kobra Neo LCD, with optional rotary/button navigation for simple pages/actions**

That is much more achievable than trying to force full original-screen behavior or full KlipperScreen mirroring through the inherited Raspberry Pi display stack.
