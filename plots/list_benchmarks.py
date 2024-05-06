import json

with open("benchmarks.json") as fd:
    contents = json.load(fd)

benchmarks = []
for benchmark in contents["benchmarks"]:
    name = benchmark.get("metadata", contents["metadata"])["name"]
    benchmarks.append(name)

benchmarks.sort()

print(len(benchmarks))
print(" ".join(benchmarks))
