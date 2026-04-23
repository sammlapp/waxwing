from matplotlib import font_manager
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib as mpl

from . import palettes

# define default style
style = f"""
axes.spines.top:   False
axes.spines.right: False
axes.xmargin:      0
axes.ymargin:      0
font.family:       sans-serif
font.size:         9
axes.labelsize:    9
axes.titlesize:    10
xtick.labelsize:   8
ytick.labelsize:   8
legend.fontsize:   8
figure.dpi:        150
savefig.dpi:       300
savefig.bbox:      tight
lines.linewidth:   0.8
"""

style_dir = Path(mpl.get_configdir()) / "stylelib"
style_dir.mkdir(exist_ok=True)
(style_dir / "waxwing.mplstyle").write_text(style)


from typing import Literal

_fonts_dir = Path(__file__).parent / "fonts"

# {family_name: {weight: path}}
_font_files = {
    "Noto Sans": {
        "light": _fonts_dir / "Noto_Sans/static/NotoSans-Light.ttf",
        "regular": _fonts_dir / "Noto_Sans/static/NotoSans-Regular.ttf",
        "medium": _fonts_dir / "Noto_Sans/static/NotoSans-Medium.ttf",
    },
    "Source Sans 3": {
        "light": _fonts_dir / "Source_Sans_3/static/SourceSans3-Light.ttf",
        "regular": _fonts_dir / "Source_Sans_3/static/SourceSans3-Regular.ttf",
        "medium": _fonts_dir / "Source_Sans_3/static/SourceSans3-Medium.ttf",
    },
    "Source Serif 4": {
        "light": _fonts_dir / "Source_Serif_4/static/SourceSerif4-Light.ttf",
        "regular": _fonts_dir / "Source_Serif_4/static/SourceSerif4-Regular.ttf",
        "medium": _fonts_dir / "Source_Serif_4/static/SourceSerif4-Medium.ttf",
    },
    "Literata": {
        "light": _fonts_dir / "Literata/static/Literata-Light.ttf",
        "regular": _fonts_dir / "Literata/static/Literata-Regular.ttf",
        "medium": _fonts_dir / "Literata/static/Literata-Medium.ttf",
    },
}

# Register each weight file under a unique synthetic family name so that
# font.family alone unambiguously selects the exact file (no weight heuristics).
# e.g. "Source Sans 3 Light", "Source Sans 3 Regular", "Source Sans 3 Medium"
for _family, _weights in _font_files.items():
    for _weight_name, _path in _weights.items():
        font_manager.fontManager.addfont(str(_path))
        # Find the entry just added and rename it to the synthetic family name
        _synthetic = f"{_family} {_weight_name.capitalize()}"
        for _entry in font_manager.fontManager.ttflist:
            if _entry.fname == str(_path):
                object.__setattr__(_entry, "name", _synthetic)
                break

FontName = Literal["Noto Sans", "Source Sans 3", "Source Serif 4", "Literata"]
FontWeight = Literal["light", "regular", "medium"]


def set_font(font_name: FontName, weight: FontWeight = "regular") -> None:
    """Set the global font family and weight for all plots.

    Points font.family directly at the exact static font file for that weight,
    bypassing Matplotlib's font matching heuristics entirely.

    Args:
        font_name: one of "Noto Sans", "Source Sans 3", "Source Serif 4", "Literata"
        weight: "light", "regular", or "medium" (default "regular")
    """
    if font_name not in _font_files:
        raise ValueError(
            f"Font '{font_name}' not found. Available fonts: {list(_font_files)}"
        )
    if weight not in ("light", "regular", "medium"):
        raise ValueError(
            f"Weight must be 'light', 'regular', or 'medium', got '{weight}'"
        )

    plt.rcParams["font.family"] = f"{font_name} {weight.capitalize()}"


def list_fonts() -> list[str]:
    return list(_font_files.keys())


def set_figsize(w, h):
    plt.rcParams["figure.figsize"] = [w, h]


def trim_spines(ax=None, keep_right=False, keep_top=False):
    """
    Clip the left and bottom spines so they end  at the outermost tick marks

    By defaut, also removes the top and right spines

    Call after all data and ticks are finalized:
        fig, ax = plt.subplots()
        ax.plot(...)
        trim_spines(ax)          # single axes
        trim_spines()            # trims plt.gca()

    Args:
        ax: the axes to trim (default: current axes)
        keep_right: whether to keep the right spine (default: False)
        keep_top: whether to keep the top spine (default: False)

    """
    if ax is None:
        ax = plt.gca()

    ax.figure.canvas.draw()  # force tick positions to be computed

    # remove top and right spines
    if not keep_top:
        ax.spines["top"].set_visible(False)
    if not keep_right:
        ax.spines["right"].set_visible(False)

    for axis, spine_name in [("x", "bottom"), ("y", "left")]:
        spine = ax.spines[spine_name]
        if not spine.get_visible():
            continue

        ticks = ax.get_xticks() if axis == "x" else ax.get_yticks()
        lim = ax.get_xlim() if axis == "x" else ax.get_ylim()

        # Keep only ticks that fall within the current axis limits
        visible = [t for t in ticks if lim[0] <= t <= lim[1]]
        if len(visible) >= 2:
            spine.set_bounds(visible[0], visible[-1])


def move_axes_outward(ax=None, pad=10):
    """
    Move axes outward from the data region (Tufte-inspired styling).

    Parameters
    ----------
    ax : matplotlib Axes, optional
        Axis to modify. If None, uses current axis.
    pad : float
        Padding in points (visual offset of spines).
    """
    if ax is None:
        ax = plt.gca()

    # move each visible axis outward
    for spine in ax.spines.values():
        if spine.get_visible():
            spine.set_position(("outward", pad))

    # Keep ticks only on visible spines
    # ax.yaxis.set_ticks_position("left")
    # ax.xaxis.set_ticks_position("bottom")

    # Subtle tick styling (important for “breathing room” effect)
    # ax.tick_params(direction="out", length=4, width=0.8)#, colors="#5e5246")

    return ax


def style_axes(ax=None, pad=10):
    """
    Trim axes to data and move outward from the data"""

    if ax is None:
        ax = plt.gca()
    trim_spines(ax)
    move_axes_outward(ax, pad=pad)
    return ax


def set_palette(palette):
    if isinstance(palette, str):
        if palette not in palettes.__all__:
            raise ValueError(
                f"Palette '{palette}' not found. Available palettes: {palettes.__all__}"
            )
        palette = getattr(palettes, palette)
    plt.rcParams["axes.prop_cycle"] = mpl.cycler(color=palette)


def set_default_styles():
    mpl.style.reload_library()
    plt.style.use("waxwing")
    set_font("Source Sans 3", "light")
    set_figsize(6.5, 3)  # default figure size for papers

    # Ensure that fonts are editble when saving PDFs
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    set_palette("matcha")
