import style

from matplotlib import pyplot as plt

fig, (left, right) = plt.subplots(1, 2, layout="constrained")

left.pie([90, 10])
left.set_title("Code")

right.pie([10, 90])
right.set_title("Time")

plt.savefig("runtime.svg", transparent=True)
