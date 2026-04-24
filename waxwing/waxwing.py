from pathlib import Path
from typing import Literal

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager

from . import palettes

# define default style
_style = f"""
axes.spines.top:   False
axes.spines.right: False
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
axes.linewidth:    0.5
xtick.minor.width: 0.5
ytick.minor.width: 0.5
"""

_weight_to_lineweight = {
    "light": 0.4,
    "book": 0.6,
    "regular": 0.8,
    "medium": 1,
}

_style_dir = Path(mpl.get_configdir()) / "stylelib"
_style_dir.mkdir(exist_ok=True)
(_style_dir / "waxwing.mplstyle").write_text(_style)


_fonts_dir = Path(__file__).parent / "fonts"

# {family_name: {weight: path}}
_font_files = {
    "Noto Sans": {
        "light": _fonts_dir / "Noto_Sans/static/NotoSans-Light.ttf",
        "book": _fonts_dir / "Noto_Sans/static/NotoSans-Book.ttf",
        "regular": _fonts_dir / "Noto_Sans/static/NotoSans-Regular.ttf",
        "medium": _fonts_dir / "Noto_Sans/static/NotoSans-Medium.ttf",
    },
    "Source Sans 3": {
        "light": _fonts_dir / "Source_Sans_3/static/SourceSans3-Light.ttf",
        "book": _fonts_dir / "Source_Sans_3/static/SourceSans3-Book.ttf",
        "regular": _fonts_dir / "Source_Sans_3/static/SourceSans3-Regular.ttf",
        "medium": _fonts_dir / "Source_Sans_3/static/SourceSans3-Medium.ttf",
    },
    "Source Serif 4": {
        "light": _fonts_dir / "Source_Serif_4/static/SourceSerif4-Light.ttf",
        "book": _fonts_dir / "Source_Serif_4/static/SourceSerif4-Book.ttf",
        "regular": _fonts_dir / "Source_Serif_4/static/SourceSerif4-Regular.ttf",
        "medium": _fonts_dir / "Source_Serif_4/static/SourceSerif4-Medium.ttf",
    },
    "Literata": {
        "light": _fonts_dir / "Literata/static/Literata-Light.ttf",
        "book": _fonts_dir / "Literata/static/Literata-Book.ttf",
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
FontWeight = Literal["light", "regular", "medium", "book"]


def set_font(
    font_name: FontName = "Source Sans 3",
    weight: FontWeight = "book",
    update_line_thickness: bool = True,
) -> None:
    """Set the global font family and weight for all plots.

    Points font.family directly at the exact static font file for that weight,
    bypassing Matplotlib's font matching heuristics entirely.

    Args:
        font_name: one of "Noto Sans", "Source Sans 3", "Source Serif 4", "Literata"
        weight: "light"=300, "regular"=400, "medium"=500, or "book"=350 (default "book")
        update_line_thickness: whether to update the line thickness of spines and ticks
            to match the new weight (default True)
    """
    if font_name not in _font_files:
        raise ValueError(
            f"Font '{font_name}' not found. Available fonts: {list(_font_files)}"
        )
    if weight not in ("light", "regular", "medium", "book"):
        raise ValueError(
            f"Weight must be 'light', 'regular', 'medium', or 'book', got '{weight}'"
        )

    plt.rcParams["font.family"] = f"{font_name} {weight.capitalize()}"
    if update_line_thickness:
        _set_spine_and_tick_thickness(weight)


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


def _move_axes_outward(ax=None, pad=10):
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

    return ax


def style_axes(ax=None, pad=10, trim_axes=True, encompass_data=True):
    """
    Trim axes to data and move outward from the data if pad>0.

    If encompass_data is True, also expand axis limits to ensure all data falls within the outermost ticks.
    Note: this can be buggy when using equal axis aspect (e.g. ax.set_aspect('equal'))

    Args:
        ax: the axes to style (default: current axes)
        pad: if >0, move axes outward from the data region by this many points (default: 10)
        trim_axes: whether to trim axes to the outermost ticks (default: True)
        encompass_data: whether to expand axis limits to ensure all data falls within the outer
    """

    if ax is None:
        ax = plt.gca()

    if pad > 0:
        _move_axes_outward(ax, pad=pad)
    if encompass_data:
        expand_limits(ax)
    if trim_axes:
        trim_spines(ax)
    return ax


def set_palette(palette):
    """Set the default color cycle for all plots to a waxwing palette

    Args:
        palette: either a list of colors or the name of a waxwing palette (e.g. "matcha")
    """
    if isinstance(palette, str):
        if palette not in palettes.__all__:
            raise ValueError(
                f"Palette '{palette}' not found. Available palettes: {palettes.__all__}"
            )
        palette = getattr(palettes, palette)
    plt.rcParams["axes.prop_cycle"] = mpl.cycler(color=palette)


def expand_limits(ax=None):
    """Adjust axis limits so that all data falls within the outermost ticks.

    Keeps Matplotlib's tick placement unchanged, but extends the limits to the
    first tick beyond the data range on each side, so no data is ever clipped
    beyond the last tick mark.

    Call after all data has been plotted and ticks are finalized.

    Args:
        ax: the axes to adjust (default: current axes)
    """
    if ax is None:
        ax = plt.gca()

    ax.figure.canvas.draw()  # ensure ticks and dataLim are computed

    # dataLim is the true data bounding box, unaffected by axis margins

    # x axis:
    ticks = ax.get_xticks()
    if len(ticks) > 2:
        # last tick at or below data min, first tick at or above data max
        lo_ticks = [t for t in ticks if t <= ax.dataLim.xmin]
        hi_ticks = [t for t in ticks if t >= ax.dataLim.xmax]
        new_lo = max(lo_ticks) if lo_ticks else ticks[0]
        new_hi = min(hi_ticks) if hi_ticks else ticks[-1]
        ax.set_xlim(new_lo, new_hi)

    # y axis:
    ticks = ax.get_yticks()
    if len(ticks) > 2:
        # last tick at or below data min, first tick at or above data max
        lo_ticks = [t for t in ticks if t <= ax.dataLim.ymin]
        hi_ticks = [t for t in ticks if t >= ax.dataLim.ymax]
        new_lo = max(lo_ticks) if lo_ticks else ticks[0]
        new_hi = min(hi_ticks) if hi_ticks else ticks[-1]
        ax.set_ylim(new_lo, new_hi)


def _set_spine_and_tick_thickness(weight):
    """Set the thickness of axes spines and ticks with name or number

    Args:
        weight: either a float line width (e.g. 0.5) or a named weight ("light",
        "regular", "medium", "book")
    """
    if isinstance(weight, str):
        if weight not in ("light", "regular", "medium", "book"):
            raise ValueError(
                f"Weight must be float or: 'light', 'regular', 'medium', or 'book', got '{weight}'"
            )
        weight = _weight_to_lineweight[weight]
    plt.rcParams["axes.linewidth"] = weight
    plt.rcParams["xtick.minor.width"] = weight
    plt.rcParams["ytick.minor.width"] = weight
    plt.rcParams["xtick.major.width"] = weight
    plt.rcParams["ytick.major.width"] = weight


def set_default_styles():
    mpl.style.reload_library()
    plt.style.use("waxwing")
    set_font("Source Sans 3", "light")
    set_figsize(6.5, 3)  # default figure size for papers

    # Ensure that fonts are editble when saving PDFs
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    set_palette("matcha")
