import pandas as pd
from entities import *
from constants import *
from functions import *

inputs = pd.read_csv('warehouse_log_inputs.csv')
outputs = pd.read_csv('warehouse_log_outputs.csv')
racks = [Rack(id=i) for i in range(NUM_OF_RACKS)]

inputs['Date'] = pd.to_datetime(inputs['Date'], format="%d/%m/%Y")
outputs['Date'] = pd.to_datetime(outputs['Date'], format="%d/%m/%Y")

add_preexisting_stock(racks, pallets_to_add=9)

total_placement_time, total_retrieval_time, total_placement_distance_covered, total_retrieval_distance_covered = simulate(
    racks, inputs, outputs)

print(f"Total placement time: {total_placement_time / 60} minutes")
print(f"Total retrieval time: {total_retrieval_time / 60} minutes")
print(f"Total placement distance covered: {total_placement_distance_covered} meters")
print(f"Total retrieval distance covered: {total_retrieval_distance_covered} meters")
print(f"Total distance covered: {total_placement_distance_covered + total_retrieval_distance_covered} meters")
