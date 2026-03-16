# GitHub Link Snippet Guide (Encoder guide moved to `guides/`)

This version matches your updated repo layout where:

- `README.md` is at the repo root
- `docs/` contains the changelog
- `guides/` contains the porting guide, pinout conversion, and `ENCODER-SETUP.md`

---

## Current expected structure

```text
README.md
docs/
  BTT-Pi_Kobra-Neo-Stock-Screen_BTT-Changes-Only_CHANGELOG.md
guides/
  BTT-Pi_Kobra-Neo-Stock-Screen_Porting-Guide.md
  BTT-Pi-v1.2_Kobra-Neo-Stock-Screen_Pinout-Conversion.md
  ENCODER-SETUP.md
```

---

## 1) If you are editing the root `README.md`

Use this block:

```md
## Documentation

- [Full porting guide](guides/BTT-Pi_Kobra-Neo-Stock-Screen_Porting-Guide.md)
- [Pinout conversion](guides/BTT-Pi-v1.2_Kobra-Neo-Stock-Screen_Pinout-Conversion.md)
- [BTT Pi changes from the original Raspberry Pi guide](docs/BTT-Pi_Kobra-Neo-Stock-Screen_BTT-Changes-Only_CHANGELOG.md)
- [Encoder setup guide](guides/ENCODER-SETUP.md)
```

This is the block that should go in the front-page `README.md`.

---

## 2) If you are editing a file inside the `guides/` folder

Use this block:

```md
## Related documentation

- [Full porting guide](BTT-Pi_Kobra-Neo-Stock-Screen_Porting-Guide.md)
- [Pinout conversion](BTT-Pi-v1.2_Kobra-Neo-Stock-Screen_Pinout-Conversion.md)
- [BTT Pi changes from the original Raspberry Pi guide](../docs/BTT-Pi_Kobra-Neo-Stock-Screen_BTT-Changes-Only_CHANGELOG.md)
- [Encoder setup guide](ENCODER-SETUP.md)
```

### Correct encoder sentence for a file inside `guides/`

```md
The original stock-screen path is not a touch UI by itself. If you want the rotary encoder / button to be usable, treat that as a second phase after the display path is proven working. The ecosystem around the Kobra Go/Neo LCD includes encoder-focused work intended to make knob-based interaction possible, but that should come after LCD bring-up, not before. ([Encoder setup guide](ENCODER-SETUP.md))
```

---

## 3) If you are editing a file inside the `docs/` folder

Use this block:

```md
## Related documentation

- [Full porting guide](../guides/BTT-Pi_Kobra-Neo-Stock-Screen_Porting-Guide.md)
- [Pinout conversion](../guides/BTT-Pi-v1.2_Kobra-Neo-Stock-Screen_Pinout-Conversion.md)
- [BTT Pi changes from the original Raspberry Pi guide](BTT-Pi_Kobra-Neo-Stock-Screen_BTT-Changes-Only_CHANGELOG.md)
- [Encoder setup guide](../guides/ENCODER-SETUP.md)
```

---

## Why this version should work now

Because `ENCODER-SETUP.md` is now in `guides/`:

- from root `README.md`, the correct path is `guides/ENCODER-SETUP.md`
- from another file inside `guides/`, the correct path is `ENCODER-SETUP.md`
- from a file inside `docs/`, the correct path is `../guides/ENCODER-SETUP.md`

GitHub resolves relative links from the location of the file you are currently viewing, not from the repo root.

---

## Recommended placement in README.md

Put the documentation block:

- near the top of the root `README.md`
- directly under your short intro/description
- before long setup or background sections

Example:

```md
# Anycubic Kobra Neo BTT Pi v1.2 Klipper Screen Conversion

Short description here.

## Documentation

- [Full porting guide](guides/BTT-Pi_Kobra-Neo-Stock-Screen_Porting-Guide.md)
- [Pinout conversion](guides/BTT-Pi-v1.2_Kobra-Neo-Stock-Screen_Pinout-Conversion.md)
- [BTT Pi changes from the original Raspberry Pi guide](docs/BTT-Pi_Kobra-Neo-Stock-Screen_BTT-Changes-Only_CHANGELOG.md)
- [Encoder setup guide](guides/ENCODER-SETUP.md)

## Overview

Rest of README continues here.
```
