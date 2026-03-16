# Quick Wiring: Anycubic Kobra Neo Stock Screen on BTT Pi v1.2

This is the short version of the wiring conversion from the Raspberry Pi-based Kobra Go/Neo LCD driver to **BTT Pi v1.2**.

## Stock LCD signals

The stock Anycubic Kobra Neo / Kobra Go screen uses these signals:

- 5V
- GND
- SCK
- MOSI
- CS
- RESET
- DC

## Original Raspberry Pi mapping used by the LCD driver

- 5V -> Pi physical pin 2 or 4
- GND -> Pi physical pin 6
- SCK -> Pi physical pin 23
- MOSI -> Pi physical pin 19
- CS -> Pi physical pin 24
- RESET -> Pi physical pin 22
- DC -> Pi physical pin 18

## Converted BTT Pi v1.2 mapping

Use this as the starting hardware map on BTT Pi v1.2:

- **5V** -> BTT Pi physical pin **2** or **4**
- **GND** -> BTT Pi physical pin **6**
- **SCK** -> BTT Pi physical pin **23** = **PH6 / GPIO230 / SPI1_CLK**
- **MOSI** -> BTT Pi physical pin **19** = **PH7 / GPIO231 / SPI1_MOSI**
- **CS** -> BTT Pi physical pin **24** = **PG12 / GPIO204**
- **RESET** -> BTT Pi physical pin **22** = **PG13 / GPIO205**
- **DC** -> BTT Pi physical pin **18** = **PC9 / GPIO73**

## Important note

This is a **hardware pin conversion**, not proof of full software compatibility.

The existing Kobra Go/Neo LCD driver was written for Raspberry Pi, so on BTT Pi v1.2 you should expect:

- manual GPIO remapping
- SPI enable/config changes
- possible driver edits or build flag changes

## Recommended repo structure

You can add this file to your repo as a short note and keep the full document for detail.

Suggested placement:

- `README-addition.md` -> quick summary
- `docs/BTT-Pi-v1.2_Kobra-Neo-Stock-Screen_Pinout-Conversion.md` -> full detail
