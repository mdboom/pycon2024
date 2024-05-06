import json
from pathlib import Path


from bench_runner import hpt


import numpy as np


CATEGORIES = {
    "app": [
        "2to3",
        "coverage",
        "dask",
        "djangocms",
        "dulwich_log",
        "flaskblogging",
        "mypy2",
        "pylint",
        "aiohttp",
        "chameleon",
        "django_template",
        "docutils",
        "genshi_text",
        "genshi_xml",
        "gunicorn",
        "html5lib",
        "mako",
        "pycparser",
        "pyflate",
        "sqlalchemy_declarative",
        "sqlalchemy_imperative",
        "sqlglot_normalize",
        "sqlglot_optimize",
        "sqlglot_parse",
        "sqlglot_transpile",
        "sqlite_synth",
        "sympy_expand",
        "sympy_integrate",
        "sympy_str",
        "sympy_sum",
        "thrift",
        "tornado_http",
    ],
    "micro": [
        "async_generators",
        "async_tree_cpu_io_mixed",
        "async_tree_cpu_io_mixed_tg",
        "async_tree_io",
        "async_tree_io_tg",
        "async_tree_memoization",
        "async_tree_memoization_tg",
        "async_tree_none",
        "async_tree_none_tg",
        "asyncio_tcp",
        "asyncio_tcp_ssl",
        "asyncio_websockets",
        "bench_mp_pool",
        "bench_thread_pool",
        "comprehensions",
        "coroutines",
        "create_gc_cycles",
        "deepcopy",
        "deepcopy_memo",
        "deepcopy_reduce",
        "gc_traversal",
        "generators",
        "json",
        "json_dumps",
        "json_loads",
        "logging_format",
        "logging_silent",
        "logging_simple",
        "pathlib",
        "pickle",
        "pickle_dict" "pickle_list",
        "pickle_pure_python",
        "pprint_pformat",
        "pprint_safe_repr",
        "python_startup",
        "python_startup_no_site",
        "regex_compile",
        "regex_dna",
        "regex_effbot",
        "regex_v8",
        "tomli_loads",
        "typing_runtime_protocols",
        "unpack_sequence",
        "unpickle",
        "unpickle_list",
        "unpickle_pure_python",
        "xml_etree_generate",
        "xml_etree_iterparse",
        "xml_etree_parse",
        "xml_etree_process",
    ],
    "toy": [
        "chaos",
        "crypto_pyaes",
        "deltablue",
        "fannkuch",
        "float",
        "go",
        "hexiom",
        "mdp",
        "meteor_contest",
        "nbody",
        "nqueens",
        "pidigits",
        "raytrace",
        "richards",
        "richards_super",
        "scimark_fft",
        "scimark_monte_carlo",
        "scimark_sor",
        "scimark_sparse_mat_mult",
        "spectral_norm",
        "telco",
    ],
}


CATEGORIES = {
    "interpreter": [
        "2to3",
        "aiohttp",
        "async_tree",
        "async_tree_cpu_io_mixed",
        "async_tree_memoization",
        "chameleon",
        "chaos",
        "comprehensions",
        "concurrent_imap",
        "coroutines",
        "crypto_pyaes",
        "dask",
        "deepcopy",
        "deltablue",
        "django_template",
        "djangocms",
        "docutils",
        "dulwich_log",
        "fannkuch",
        "float",
        "generators",
        "genshi",
        "go",
        "gunicorn",
        "hexiom",
        "html5lib",
        "logging",
        "mako",
        "mypy2",
        "nbody",
        "nqueens",
        "pickle_pure_python",
        "pprint",
        "pycparser",
        "pyflate",
        "pylint",
        "raytrace",
        "regex_compile",
        "richards",
        "richards_super",
        "scimark",
        "spectral_norm",
        "sqlglot",
        "sqlglot_optimize",
        "sqlglot_parse",
        "sqlglot_transpile",
        "sympy",
        "thrift",
        "tomli_loads",
        "tornado_http",
        "typing_runtime_protocols",
        "unpack_sequence",
        "unpickle_pure_python",
        "xml_etree",
    ],
    "memory": ["async_generators", "json_dumps", "unpickle", "unpickle_list"],
    "gc": [
        "async_tree_cpu_io_mixed_tg",
        "async_tree_io",
        "async_tree_io_tg",
        "async_tree_memoization_tg",
        "async_tree_tg",
        "gc_collect",
        "gc_traversal",
    ],
    "kernel": ["asyncio_tcp", "pathlib", "python_startup", "python_startup_no_site"],
    "libc": ["asyncio_tcp_ssl"],
    "library": [
        "asyncio_websockets",
        "json",
        "json_loads",
        "pickle",
        "pickle_dict",
        "pickle_list",
        "regex_dna",
        "regex_effbot",
        "regex_v8",
        "sqlite_synth",
        "telco",
    ],
    "unknown": ["coverage"],
    "tuple": ["mdp"],
    "miscobj": ["meteor_contest"],
    "int": ["pidigits"],
}


INPUTS = ["310.json", "312.json"]

for key, val in CATEGORIES.items():
    for input in INPUTS:
        input = Path(input)
        with open(input) as fd:
            contents = json.load(fd)
        contents["benchmarks"] = [
            bm for bm in contents["benchmarks"] if bm["metadata"]["name"] in val
        ]
        with open(f"{input.stem}-{key}.json", "w") as fd:
            json.dump(contents, fd)


def get_timing_data(contents) -> dict[str, np.ndarray]:
    data = {}

    for benchmark in contents["benchmarks"]:
        name = benchmark.get("metadata", contents["metadata"])["name"]
        row = []
        for run in benchmark["runs"]:
            row.extend(run.get("values", []))
        data[name] = np.array(row, dtype=np.float64)

    return data


for key, val in CATEGORIES.items():
    print(key, len(val))
    print(hpt.make_report(f"310-{key}.json", f"312-{key}.json"))

    with open(f"310-{key}.json") as fd:
        base_contents = json.load(fd)
    with open(f"312-{key}.json") as fd:
        head_contents = json.load(fd)

    base_data = get_timing_data(base_contents)
    head_data = get_timing_data(head_contents)

print(hpt.make_report(f"310.json", f"312.json"))
