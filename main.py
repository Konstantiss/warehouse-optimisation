import pandas as pd
from entities import *
from constants import *
from functions import *

inputs = pd.read_csv('warehouse_log_inputs.csv')
outputs = pd.read_csv('warehouse_log_outputs.csv')

inputs['Date'] = pd.to_datetime(inputs['Date'], format="%d/%m/%Y")
outputs['Date'] = pd.to_datetime(outputs['Date'], format="%d/%m/%Y")

racks = [Rack(id=i) for i in range(NUM_OF_RACKS)]

total_placement_time_initial, total_retrieval_time_initial, total_placement_distance_covered_initial, total_retrieval_distance_covered_initial = simulate_with_initial_placement(
    racks, inputs, outputs)


racks = [Rack(id=i) for i in range(NUM_OF_RACKS)]

total_placement_time_optimized, total_retrieval_time_optimized, total_placement_distance_covered_optimized, total_retrieval_distance_covered_optimized = simulate_with_optimized_placement(
    racks, inputs, outputs)

print("\n\n")

print(f"Total placement time with initial placement: {total_placement_time_initial / 60} minutes")
print(f"Total retrieval time with initial placement: {total_retrieval_time_initial / 60} minutes")
print(f"Total time with initial placement: {total_placement_time_initial / 60 + total_retrieval_time_initial / 60} minutes")
print(f"Total placement distance covered with initial placement: {total_placement_distance_covered_initial} meters")
print(f"Total retrieval distance covered with initial placement: {total_retrieval_distance_covered_initial} meters")
print(f"Total distance covered with initial placement: {total_placement_distance_covered_initial + total_retrieval_distance_covered_initial} meters")

print("\n\n")

print(f"Total placement time with optimized placement: {total_placement_time_optimized / 60} minutes")
print(f"Total retrieval time with optimized placement: {total_retrieval_time_optimized / 60} minutes")
print(f"Total time with optimized placement: {total_placement_time_optimized / 60 + total_retrieval_time_optimized / 60} minutes")
print(f"Total placement distance covered with optimized placement: {total_placement_distance_covered_optimized} meters")
print(f"Total retrieval distance covered with optimized placement: {total_retrieval_distance_covered_optimized} meters")
print(f"Total distance covered with optimized placement: {total_placement_distance_covered_optimized + total_retrieval_distance_covered_optimized} meters")