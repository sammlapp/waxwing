import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from waxwing import palettes

palette_groups = [
    (
        "Categorical",
        [
            "spring",
            "wax",
            "clay",
            "fruit",
            "matcha",
            "earth",
            "lichen",
            "solid",
            "sport",
        ],
    ),
    ("Sequential", ["twilight", "canopy", "glacier", "waxwing"]),
    ("Diverging", ["savanna", "heath", "coastline"]),
]

# spring: show only first 5 colors
palette_overrides = {"spring": palettes.spring[:5]}

n_rows = sum(len(g[1]) for g in palette_groups)
row_h_in = 0.42
group_gap_in = 0.38
fig_height = n_rows * row_h_in + len(palette_groups) * group_gap_in + 0.3
fig_width = 9.0

fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=300)
ax.set_xlim(0, fig_width)
ax.set_ylim(0, fig_height)
ax.set_axis_off()
fig.patch.set_facecolor("white")

label_x = 1.65  # inches: left edge of swatches
swatch_w = 0.38  # inches per swatch
swatch_h = 0.26  # inches tall
label_col_x = 0.05  # name label x

y = fig_height - 0.15  # current y in inches, top-down

for group_name, names in palette_groups:
    y -= group_gap_in * 0.55
    ax.text(
        label_col_x,
        y,
        group_name,
        fontsize=9,
        fontweight="bold",
        color="#555",
        va="top",
        ha="left",
    )
    y -= group_gap_in * 0.55

    for name in names:
        colors = palette_overrides.get(name, getattr(palettes, name))
        n = len(colors)
        cy = y - swatch_h / 2  # vertical center of swatch row

        for i, c in enumerate(colors):
            x0 = label_x + i * (swatch_w + 0.04)
            rect = mpatches.FancyBboxPatch(
                (x0, cy - swatch_h / 2),
                swatch_w,
                swatch_h,
                boxstyle="round,pad=0.02",
                facecolor=c,
                edgecolor="none",
                clip_on=False,
            )
            ax.add_patch(rect)

        ax.text(label_col_x, cy, name, fontsize=9, va="center", ha="left", color="#222")

        count_x = label_x + n * (swatch_w + 0.04) + 0.08
        ax.text(
            count_x,
            cy,
            f"{n} colors",
            fontsize=7.5,
            va="center",
            ha="left",
            color="#aaa",
        )

        y -= row_h_in

plt.savefig("./palettes.png", dpi=300, bbox_inches="tight", facecolor="white")
print("saved")
