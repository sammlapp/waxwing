from matplotlib import font_manager
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib as mpl

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
"""

style_dir = Path(mpl.get_configdir()) / "stylelib"
style_dir.mkdir(exist_ok=True)
(style_dir / "waxwing.mplstyle").write_text(style)


# Path to font inside your repo
fonts = {
    "Noto Sans": Path(__file__).parent.parent
    / "fonts/Noto_Sans/NotoSans-VariableFont_wdth,wght.ttf",
    "Source Sans 3": Path(__file__).parent.parent
    / "fonts/Source_Sans_3/SourceSans3-VariableFont_wght.ttf",
    "Source Serif 4": Path(__file__).parent.parent
    / "fonts/Source_Serif_4/SourceSerif4-VariableFont_opsz,wght.ttf",
    "Literata": Path(__file__).parent.parent
    / "fonts/Literata/Literata-VariableFont_opsz,wght.ttf",
}
font_mpl_ids = {}

for font_name, font_path in fonts.items():
    # Register font with Matplotlib
    font_manager.fontManager.addfont(str(font_path))

    # Get the actual font name (important!)
    prop = font_manager.FontProperties(fname=str(font_path))
    font_mpl_ids[font_name] = prop.get_name()


def set_font(font_name):
    if font_name not in font_mpl_ids:
        raise ValueError(
            f"Font '{font_name}' not found. Available fonts: {list(font_mpl_ids.keys())}"
        )
    plt.rcParams["font.family"] = font_mpl_ids[font_name]


def list_fonts():
    return list(font_mpl_ids.keys())


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


def set_default_styles():
    mpl.style.reload_library()
    plt.style.use("waxwing")
    set_font("Source Sans 3")
    set_figsize(6.5, 3)  # default figure size for papers

    # Ensure that fonts are editble when saving PDFs
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
