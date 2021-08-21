import decimal
import math
import os
import re

import numpy
import pandas as pd
import matplotlib.pyplot as plt

from decimal import Decimal

import graphic

numbers = []

# reading file
with open("data.txt") as file:
    lines = file.read().splitlines()
    match = re.search("separator\s*=\s*\'(.*)\'", lines[0])
    separator = match.group(1)

    if separator is None:
        print("The separator was not found on the first line!")
        exit()

    data = " ".join(lines[1:]).strip()
    for value in data.split(separator):
        try:
            numbers.append(Decimal(value.replace(" ", "").replace(",", ".")))
        except decimal.InvalidOperation:
            print("The value: " + value + " is not a decimal")

observations = numpy.array(numbers)
mim_observed = numpy.min(observations)
max_observed = numpy.max(observations)

# rule of Sturges to get amount of class: k = 1 + 3.322 log10 n
sturges = Decimal(1 + 3.322 * math.log10(observations.size))
# get the total amplitude calculated by maximum amplitude - minimum amplitude
amplitude = max_observed - mim_observed
# get the amplitude of interval of classes calculated by: amplitude / k
interval = math.ceil(amplitude / sturges)

# round sturges
k = math.ceil(sturges)

# get all class based in interval
clazz = []

for index in range(k):
    value = mim_observed + index * interval
    clazz.append([value, value + interval])

# get the midpoint of classes
midpoint = []

point = (clazz[0][1] - clazz[0][0]) / 2
for index in range(k):
    midpoint.append(clazz[index][0] + point)

# get the absolute simple frequency
absolute_simple_frequency = []

for index in range(k):
    minInterval = clazz[index][0]
    maxInterval = clazz[index][1]

    value = observations[(observations >= minInterval) & (observations < maxInterval)]
    absolute_simple_frequency.append(len(value))

# get the relative simple frequency
relative_simple_frequency = []

for index in range(k):
    value = (absolute_simple_frequency[index] / observations.size)
    relative_simple_frequency.append(round(value, 2))

# get the simple accumulated frequency
simple_accumulated_frequency = []

for index in range(k):
    value = sum(absolute_simple_frequency[:index + 1])
    simple_accumulated_frequency.append(value)

# get the relative accumulated frequency
relative_accumulated_frequency = []

for index in range(k):
    value = (simple_accumulated_frequency[index] / observations.size)
    relative_accumulated_frequency.append(round(value, 2))

numpy.set_printoptions(precision=2)

frame = pd.DataFrame()
frame["Classe"] = [str(clazz[index][0]) + " |- " + str(clazz[index][1]) for index in range(k)]
frame["fi"] = absolute_simple_frequency
frame["xi"] = midpoint
frame["fri"] = relative_simple_frequency
frame["fri%"] = relative_simple_frequency * numpy.full(len(relative_accumulated_frequency), 100)
frame["Fi"] = simple_accumulated_frequency
frame["Fri"] = relative_accumulated_frequency
frame["Fri%"] = relative_accumulated_frequency * numpy.full(len(relative_accumulated_frequency), 100)

frame["Fri%"] = frame["Fri%"].round(decimals=2)
frame["fri%"] = frame["fri%"].round(decimals=2)

if not os.path.exists("images"):
    os.makedirs("images")

graphic.create_table(frame, col_width=2, cellLoc='center')
plt.savefig("images/frequency_table.png", dpi=600, transparent=True)

graphic.create_histogram(frame.index, frame["fi"], clazz,
                         x_label='Intervalo de classe',
                         y_label='Frequência',
                         font='x-large',
                         color='darkturquoise')

plt.savefig("images/frequency_histogram.png", transparent=True, dpi=600)
