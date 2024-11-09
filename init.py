from audioop import reverse

import pandas as pd

NUM_OF_RACKS = 2
BAYS_PER_RACK = 10
SHELVES_PER_BAY = 4
PALLETS_PER_SHELF = 3
SHELF_HEIGHT = 1.8  # meters
BAY_WIDTH = 3  # meters
PALLET_WIDTH = 0.8  # meters
DROP_OFF_TO_AISLE_DISTANCE = 5  # meters
PICK_UP_TO_AISLE_DISTANCE = 5  # meters
FORKLIFT_MOVE_SPEED = 1.2  # meters/second
FORKLIFT_LIFT_SPEED = 0.5  # meters/second
PLACEMENT_TIME = 1  # second
RETRIEVAL_TIME = 1  # second


class Europallet:
    def __init__(self, category):
        self.category = category


class Shelf:
    def __init__(self, id):
        self.shelf_id = id
        self.numOfPallets = 0
        self.maxNumOfPallets = PALLETS_PER_SHELF
        self.pallets = []

    def add_pallet(self, pallet):
        self.pallets.append(pallet)
        self.numOfPallets += 1
        print("Pallet of " + pallet.category + " added.")

    def remove_pallet(self, pallet):
        self.pallets.remove(pallet)
        self.numOfPallets -= 1
        print("Pallet of " + pallet.category + " removed.")


class Bay:
    def __init__(self, id):
        self.bay_id = id
        self.shelves = [Shelf(id=i) for i in range(SHELVES_PER_BAY)]


class Rack:
    def __init__(self, id):
        self.rack_id = id
        self.bays = [Bay(id=i) for i in range(BAYS_PER_RACK)]


def add_pallet(rack, bay_id, pallet):
    if pallet.category == 'Category A' and len(rack.bays[bay_id].shelves[0].pallets) < rack.bays[bay_id].shelves[
        0].maxNumOfPallets:

        '''
        Category A items can be placed on the bottom shelves. 
        Here the bottom shelf is consider to be index 0.
        '''

        rack.bays[bay_id].shelves[0].add_pallet(pallet)
        placement_time, distance_covered = calculate_placement_time(bay_id, rack.bays[bay_id].shelves[0].shelf_id)
        return f"Placed pallet of {pallet.category} in rack {rack.rack_id + 1} bay {rack.bays[bay_id].bay_id + 1} bottom shelf.", placement_time, distance_covered

    elif pallet.category == 'Category B' and rack.bays[bay_id].shelves[-1].numOfPallets < rack.bays[bay_id].shelves[
        -1].maxNumOfPallets:

        '''
        Category B items can be placed on the bottom shelves. 
        Here the bottom shelf is consider to be the maximum index.
        '''

        rack.bays[bay_id].shelves[-1].add_pallet(pallet)
        placement_time, distance_covered = calculate_placement_time(bay_id, rack.bays[bay_id].shelves[-1].shelf_id)
        return f"Placed pallet of {pallet.category} in rack {rack.rack_id + 1} bay {rack.bays[bay_id].bay_id + 1} top shelf.", placement_time, distance_covered
    else:
        for shelf in rack.bays[bay_id].shelves:
            if shelf.numOfPallets < shelf.maxNumOfPallets:
                shelf.add_pallet(pallet)
                placement_time, distance_covered = calculate_placement_time(bay_id, shelf.shelf_id)
                return f"Placed pallet of {pallet.category} in rack {rack.rack_id + 1} bay {bay_id + 1} shelf {shelf.shelf_id + 1}.", placement_time, distance_covered

    return "No available space in bay."

def retrieve_pallet(racks, category):
    rack_ids = []
    bay_ids = []
    shelf_ids = []
    pallets = []
    for rack in racks:
        rack_id, bay_id, shelf_id, pallet = search_pallet_in_rack(rack, category)
        rack_ids.append(rack_id)
        bay_ids.append(bay_id)
        shelf_ids.append(shelf_id)
        pallets.append(pallet)

    rack_ids = [i for i in rack_ids if i is not None]
    bay_ids = [i for i in bay_ids if i is not None]
    shelf_ids = [i for i in shelf_ids if i is not None]
    pallets = [i for i in pallets if i is not None]

    if len(bay_ids) > 1: #If there are > 1 candidate pallets
        retrieval_times = []
        distances_covered = []
        for index in range(len(bay_ids)):
            retrieval_time, distance_covered = calculate_retrieval_time(bay_ids[index], shelf_ids[index])
            retrieval_times.append(retrieval_time)
            distances_covered.append(distance_covered)
        optimal_index = retrieval_times.index(min(retrieval_times))
        racks[optimal_index].bays[bay_ids[optimal_index]].shelves[shelf_ids[optimal_index]].remove_pallet(pallets[optimal_index])
        return retrieval_times[optimal_index], distances_covered[optimal_index]
    elif len(bay_ids) == 1:
        retrieval_time, distance_covered = calculate_retrieval_time(bay_ids[0], shelf_ids[0])
        racks[rack_ids[0]].bays[bay_ids[0]].shelves[shelf_ids[0]].remove_pallet(pallets[0])
        return retrieval_time, distance_covered
    else:
        return "Pallet not found."


def search_pallet_in_rack(rack, category):

    if category == 'Category A':
        '''
        Reverse loop the bay list because of the proximity to the pick-up area.
        '''
        for bay in reversed(rack.bays):
            for pallet in bay.shelves[0].pallets:
                if pallet.category == category:
                    print(f"Pallet found in bay {bay.bay_id + 1} bottom shelf")
                    return rack.rack_id, bay.bay_id, bay.shelves[0].shelf_id, pallet

    if category == 'Category B':
        for bay in reversed(rack.bays):
            for pallet in bay.shelves[-1].pallets:
                if pallet.category == category:
                    print(f"Pallet found in bay {bay.bay_id + 1} bottom shelf")
                    return rack.rack_id, bay.bay_id, bay.shelves[-1].shelf_id, pallet

    else:
        for bay in reversed(rack.bays):
            for shelf in bay.shelves:
                for pallet in shelf.pallets:
                    if pallet.category == category:
                        print(f"Pallet found in bay {bay.bay_id + 1} shelf {shelf.shelf_id + 1}")
                        return rack.rack_id, bay.bay_id, shelf.shelf_id, pallet

    return None, None, None, None

def calculate_placement_time(bay_id, shelf_id):
    distance_to_bay = DROP_OFF_TO_AISLE_DISTANCE + bay_id * BAY_WIDTH + BAY_WIDTH / 2
    move_time = distance_to_bay / FORKLIFT_MOVE_SPEED
    lift_time = (shelf_id * SHELF_HEIGHT) / FORKLIFT_LIFT_SPEED
    total_time = move_time + lift_time + PLACEMENT_TIME
    return total_time, distance_to_bay

def calculate_retrieval_time(bay_id, shelf_id):
    distance_to_bay = PICK_UP_TO_AISLE_DISTANCE + bay_id * BAY_WIDTH + BAY_WIDTH / 2
    move_time = distance_to_bay / FORKLIFT_MOVE_SPEED
    lift_time = (shelf_id * SHELF_HEIGHT) / FORKLIFT_LIFT_SPEED
    total_time = move_time + lift_time + RETRIEVAL_TIME
    return total_time, distance_to_bay

def add_preexisting_stock(racks, inputs, outputs):

    diff = inputs['Category'].value_counts()['Category A'] - outputs['Category'].value_counts()['Category A']
    if diff < 0:
        pallet_count = 0
        for rack in racks:
            for bay in reversed(rack.bays):
                for index in range(bay.shelves[0].maxNumOfPallets): #Fill the bottom shelves
                    if pallet_count == abs(diff):
                        break
                    else:
                        pallet = Europallet(category='Category A')
                        add_pallet(rack, bay.bay_id, pallet)
                        pallet_count += 1

    diff = inputs['Category'].value_counts()['Category B'] - outputs['Category'].value_counts()['Category B']

    if diff < 0:
        pallet_count = 0
        for rack in racks:
            for bay in reversed(rack.bays):
                for index in range(bay.shelves[-1].maxNumOfPallets):  # Fill the top shelves
                    if pallet_count == abs(diff):
                        break
                    else:
                        pallet = Europallet(category='Category B')
                        add_pallet(rack, bay.bay_id, pallet)
                        pallet_count += 1

    diff = inputs['Category'].value_counts()['Category C'] - outputs['Category'].value_counts()['Category C']

    if diff < 0:
        pallet_count = 0
        for rack in racks:
            for bay in reversed(rack.bays):
                for shelf in bay.shelves:
                    for index in range(shelf.maxNumOfPallets):
                        if pallet_count == abs(diff):
                            break
                        else:
                            pallet = Europallet(category='Category C')
                            add_pallet(rack, bay.bay_id, pallet)
                            pallet_count += 1

inputs = pd.read_csv('warehouse_log_inputs.csv')
outputs = pd.read_csv('warehouse_log_outputs.csv')
racks = [Rack(id=i) for i in range(NUM_OF_RACKS)]

inputs['Date'] = pd.to_datetime(inputs['Date'], format="%d/%m/%Y")

total_placement_time = 0
total_distance_covered = 0

add_preexisting_stock(racks, inputs, outputs)

for date, day_data in inputs.groupby(inputs['Date'].dt.date):
    day_placement_time = 0
    day_distance_covered = 0
    for index, row in day_data.iterrows():
        rack = int(row['Rack'].split('Rack ')[1])  # Get only the number from 'Rack X'
        bay = int(row['Bay'])
        category = row['Category']
        pallet = Europallet(category=category)
        day_placement_time += add_pallet(racks[rack - 1], bay - 1, pallet)[1]
        day_distance_covered += add_pallet(racks[rack - 1], bay - 1, pallet)[2]
    retrieve_pallet(racks, category='Category A')
    total_placement_time += day_placement_time
    total_distance_covered += day_distance_covered
    print(f"Processed data for {date}")
    break
