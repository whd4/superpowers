# Whitt Reference Photos

> Visual identity reference assets used by AI image generators when producing scenes, portraits, or marketing visuals featuring Whitt Dwyer.
>
> Linked from [`preferences/whitt-preferences.md`](../../preferences/whitt-preferences.md) — see the "Visual Identity" section.

## Expected Files

| Filename | Composition | Use |
|----------|-------------|-----|
| `whitt-01.webp` | Head-and-shoulders, YSL editorial style, red brushstroke background | Default headshot, profile pics, avatar generation |
| `whitt-02.webp` | Full-body standing portrait, silver silk drape, "WHITT DWYER" overlay typography | Marketing visuals, scene generation, brand work |

## How they get here

These files are added manually by Whitt because binary uploads exceed the context window of single-turn AI tool calls. From WSL or Git Bash:

```bash
cd ~/Development/superpowers   # or wherever the repo is cloned
git checkout claude/add-preferences-system-gMVih
mkdir -p assets/whitt-reference
cp /path/to/whitt-01.webp assets/whitt-reference/whitt-01.webp
cp /path/to/whitt-02.webp assets/whitt-reference/whitt-02.webp
git add assets/whitt-reference/whitt-0{1,2}.webp
git commit -m "Add Whitt visual-identity reference photos"
git push -u origin claude/add-preferences-system-gMVih
```

## How they get used

- **Image-to-image generators (DALL-E, Midjourney with `--cref`, Stable Diffusion img2img, Sora references):** seed with one of these files for face consistency.
- **Text-only generators:** the text description in `preferences/whitt-preferences.md` → "Visual Identity" section is detailed enough for a strong likeness without seed images. Use that.
- **Brand work (Figma, Canva):** drop into the design as a reference layer, then trace or stylize.

## Style Lock

Every scene should preserve:

- Bald · full dark beard · sharp eyes · executive bearing
- All-black YSL-tailored suit · oxblood tie/pocket square · silver monogram pin
- Cinematic key-light from camera-left · deep shadow side · charcoal or silver silk background
- Optional: bold red brushstroke graphic across composition

Never: smiling teeth · casual wear · busy backgrounds · warm bright lighting · cartoon styling.
