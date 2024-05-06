import style


import numpy as np
import json
from operator import itemgetter

from bench_runner import plot


import pyperf


names = sorted(
    [
        "nqueens",
        "richards",
        "comprehensions",
        "gc_collect",
        "json",
        "djangocms",
        "pylint",
        "docutils",
        "sqlglot",
    ],
    reverse=True,
)


def get_timing_data(contents) -> dict[str, np.ndarray]:
    data = {}

    for benchmark in contents["benchmarks"]:
        name = benchmark.get("metadata", contents["metadata"])["name"]
        if name in ["typing_runtime_protocols"]:
            continue
        # if name not in names:
        #    continue
        row = []
        for run in benchmark["runs"]:
            row.extend(run.get("values", []))
        data[name] = np.array(row, dtype=np.float64)

    return data


with open("310.json") as fd:
    base_contents = json.load(fd)
    base_data = get_timing_data(base_contents)


with open("312.json") as fd:
    head_contents = json.load(fd)
    head_data = get_timing_data(head_contents)


def get_combined_data(
    ref_data: dict[str, np.ndarray], head_data: dict[str, np.ndarray]
):
    def remove_outliers(values, m=2):
        return values[abs(values - np.mean(values)) < np.multiply(m, np.std(values))]

    def calculate_diffs(ref_values, head_values) -> tuple[np.ndarray | None, float]:
        sig, t_score = pyperf._utils.is_significant(ref_values, head_values)

        if not sig:
            return None, 0.0
        else:
            ref_values = remove_outliers(ref_values)
            head_values = remove_outliers(head_values)
            values = np.outer(ref_values, 1.0 / head_values).flatten()
            values.sort()
            return values, float(values.mean())

    combined_data = []
    for name, ref in ref_data.items():
        if len(ref) != 0 and name in head_data:
            head = head_data[name]
            if len(ref) == len(head):
                combined_data.append((name, *calculate_diffs(ref, head)))
    combined_data.sort(key=itemgetter(2))
    return combined_data


combined_data = get_combined_data(base_data, head_data)


plot.plot_diff(
    combined_data,
    "compare.svg",
    "3.12 vs. 3.10 benchmark timing distribution",
    ("slower", "faster"),
)
