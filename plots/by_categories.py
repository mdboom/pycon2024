from matplotlib import pyplot as plt

import style


DATA = {
    "app": [32, 27],
    "micro": [50, 17],
    "toy": [21, 30],
    "overall": [32 + 50 + 21, 29],
}

OUTPUT = "by_categories.svg"


DATA = {
    "interpreter": [54, 38],
    "library": [11, 0],
    "gc": [7, 0],
    "memory": [4, 0],
    "kernel": [4, 0],
    "object": [3, 0],
    "libc": [1, 0],
    "overall": [32 + 50 + 21, 29],
}


OUTPUT = "by_perf_categories.svg"


SUBDATA = DATA.copy()
del SUBDATA["overall"]


fig, axs = plt.subplots(1, 2, figsize=(7, 3.5), layout="constrained")

COLORS = ["C4", "C3", "C6", "C7", "C1", "C0", "C2", "#bbbbbb"]

axs[0].pie(
    [v[0] for v in SUBDATA.values()],
    labels=[f"{k} ({v[0]})" for k, v in SUBDATA.items()],
    colors=COLORS[:-1],
)
axs[0].set_title("# benchmarks by top profiling category")

p = axs[1].bar(
    list(range(len(DATA))),
    [v[1] for v in DATA.values()],
    tick_label=list(DATA.keys()),
    # color=[f"C{i}" for i in range(len(SUBDATA))] + ["#888888"],
    color=COLORS,
)
axs[1].bar_label(p)
axs[1].set_title("3.12 vs. 3.10 by profiling category")
axs[1].set_ylabel("% speedup")
axs[1].set_ylim(0, 50)
axs[1].tick_params(axis="x", labelrotation=45)

plt.savefig(OUTPUT, transparent=True)
