# waxwing

Matplotlib utilities and color palettes for publication-ready figures.

Waxwing applies sensible defaults—clean spines, print-quality DPI, editable PDF fonts, bundled typefaces—so you spend less time fighting Matplotlib and more time on your figures.

## Installation

```bash
pip install waxwing
```

## Quick start

```python
import matplotlib.pyplot as plt
import waxwing

waxwing.set_default_styles()          # apply all defaults at once

fig, ax = plt.subplots()
ax.plot(x, y)
waxwing.style_axes(ax)                # trim spines, expand limits, offset axes
plt.savefig("figure.pdf")
```

## API

### `set_default_styles()`

Applies the full waxwing style in one call. Call once at the top of your script or notebook.

| Setting | Value |
|---|---|
| Font | Source Sans 3 Light |
| Figure size | 6.5 × 3 in (single column, papers) |
| Color palette | `matcha` |
| Screen DPI | 150 |
| Save DPI | 300 |
| Save bbox | tight |
| PDF/PS font type | 42 (editable in Illustrator) |
| Top/right spines | removed |
| Axis margins | 0 |

### `style_axes(ax=None, pad=10, trim_axes=True, encompass_data=True)`

Call once per axes after all data is plotted. Combines three operations:

- **trim spines** — clips left and bottom spines to the outermost tick marks
- **expand limits** — extends axis limits so all data falls within the outermost ticks, preserving Matplotlib's tick placement
- **offset axes** — moves spines outward from the data (`pad` points)

```python
fig, ax = plt.subplots()
ax.scatter(x, y)
waxwing.style_axes(ax)

# or with options:
waxwing.style_axes(ax, pad=5, encompass_data=False)
```

### `set_font(font_name, weight="book")`

Each weight is a distinct static font file — no Matplotlib weight-matching heuristics.

| Name | Style |
|---|---|
| `"Source Sans 3"` | Neutral sans-serif (default) |
| `"Noto Sans"` | Wide-coverage sans-serif |
| `"Source Serif 4"` | Optical-size serif |
| `"Literata"` | Literary serif |

Available weights: `"light"`, `"book"`, `"regular"`, `"medium"`

```python
waxwing.set_font("Literata", "medium")
waxwing.set_font("Source Serif 4")        # defaults to "book"
```

### `set_palette(palette)`

Sets the default color cycle. Accepts a palette name or any list of hex colors.

```python
waxwing.set_palette("wax")
waxwing.set_palette(["#e07a5f", "#3d405b", "#81b29a"])
```

### `set_figsize(w, h)`

```python
waxwing.set_figsize(3.25, 2.5)    # half-column width
waxwing.set_figsize(6.5, 4)
```

## Color palettes

All palettes live in `waxwing.palettes` and are plain Python lists of hex strings, so they work anywhere Matplotlib accepts a color sequence. YOu can also use them with seaborn.

![Color palettes](palettes.png)

```python
from waxwing import palettes

ax.plot(x, y, color=palettes.clay[1])
ax.set_prop_cycle(color=palettes.spring)

# seaborn:
sns.color_palette(palettes.savanna)

# reversed colormap:
palettes.waxwing[::-1]
```

### Categorical

| Palette | Colors | Character |
|---|---|---|
| `wax` | 6 | yellow, red, green, gold, blue, violet |
| `clay` | 5 | warm earth tones |
| `fruit` | 5 | vibrant warm hues |
| `matcha` | 5 | muted purples and pastels |
| `earth` | 5 | dark browns and teal |
| `lichen` | 8 | greens, ochre, and lavender |
| `solid` | 5 | bold primaries |
| `sport` | 5 | vivid cyan, purple, gold |

### Sequential (dark → light)

| Palette | Colors | Character |
|---|---|---|
| `waxwing` | 7 | warm taupe → off-white |
| `twilight` | 6 | navy → lavender → grey |
| `canopy` | 6 | forest green → cream |
| `glacier` | 6 | deep blue → near-white |

### Diverging

| Palette | Colors | Character |
|---|---|---|
| `savanna` | 6 | brown ↔ olive green |
| `heath` | 6 | warm brown ↔ cool green |
| `coastline` | 6 | slate blue ↔ mauve |

### Large categorical cycle: `spring`

`spring` contains 31 colors organized in five tonal cycles (vivid → pale → dark → mid → near-black, plus greys). It is designed to support figures with many series while maintaining visual coherence.

```python
ax.set_prop_cycle(color=palettes.spring)
```

## Requirements

- Python ≥ 3.8
- matplotlib

## Development

Creating image in readme of current color palettes:

```
python create_palettes.py
```

Adding a new font:

Only add fonts with licenses that allow distribution. 

1. Obtain the Variable font or each weight as separate ttf. I select 350 i.e. 'Book' as the default font weight, which is typically not provided but can be created from Variable fonts.
2. If needed, instance the font into a static .ttf:
```
pip install fonttools
fonttools varLib.instancer \
  SourceSans3-VariableFont_wght.ttf \
  wght=350 \
  -o SourceSans3-Book.ttf
```
3. Save copies under fonts/Name/static/[Name]-Light.ttf (or Medium, Regular, etc)
4. Update  `waxwing.py`: `_font_files` and `FontName` variables with Name and paths to the static font weight files

## Publishing to PyPI

### First release

1. Create an account-scoped API token at pypi.org → Account Settings → API tokens
2. Add a profile to `~/.pypirc`:
   ```ini
   [waxwing]
   repository = https://upload.pypi.org/legacy/
   username = __token__
   password = pypi-...
   ```
3. Build and upload:
   ```bash
   pip install build twine
   python -m build
   twine upload --repository waxwing dist/*
   ```
4. After the project exists on PyPI, replace the account-scoped token with a project-scoped one (pypi.org → Account Settings → API tokens → Add token, scope to `waxwing`), and update `~/.pypirc`

### Subsequent releases

1. Bump `version` in `pyproject.toml`
2. Delete the old `dist/` directory
3. `python -m build`
4. `twine upload --repository waxwing dist/*`

