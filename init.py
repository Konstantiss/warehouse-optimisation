from unicodedata import category

import pandas as pd

inputs = pd.read_csv('warehouse_log_inputs.csv')
outputs = pd.read_csv('warehouse_log_outputs.csv')

NUM_OF_RACKS = 2
BAYS_PER_RACK = 10
SHELVES_PER_BAY = 4
PALLETS_PER_SHELF = 3
SHELF_HEIGHT = 1.8 #meters
BAY_WIDTH = 3 #meters
PALLET_WIDTH = 0.8 #meters
FORKLIFT_MOVE_SPEED = 1.2 #meters/second
FORKLIFT_LIFT_SPEED = 0.5 #meters/second
PLACEMENT_TIME = 1 #second

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

class Bay:
    def __init__(self, id):
        self.bay_id = id
        self.shelves = [Shelf(id=i) for i in range(SHELVES_PER_BAY)]

class Rack:
    def __init__(self, id):
        self.rack_id = id
        self.bays = [Bay(id=i) for i in range(BAYS_PER_RACK)]

def add_pallet(rack, bay_id, pallet):

    if pallet.category == 'Category A' and len(rack.bays[bay_id].shelves[0].pallets) < rack.bays[bay_id].shelves[0].maxNumOfPallets:

        '''
        Category A items can be placed on the bottom shelves. 
        Here the bottom shelf is consider to be index 0.
        '''
        rack.bays[bay_id].shelves[0].add_pallet(pallet)
        return f"Placed pallet of {pallet.category} in rack {rack.rack_id} bay {rack.bays[bay_id].bay_id} bottom shelf."

    elif pallet.category == 'Category B' and rack.bays[bay_id].shelves[-1].numOfPallets < rack.bays[bay_id].shelves[-1].maxNumOfPallets:

        '''
        Category B items can be placed on the bottom shelves. 
        Here the bottom shelf is consider to be the maximum index.
        '''
        rack.bays[bay_id].shelves[-1].add_pallet(pallet)
        return f"Placed pallet of {pallet.category} in rack {rack.rack_id} bay {rack.bays[bay_id].bay_id} top shelf."
    else:
        for shelf in rack.bays[bay_id].shelves:
            if shelf.numOfPallets < shelf.maxNumOfPallets:
                shelf.add_pallet(pallet)
                return f"Placed pallet of {pallet.category} in rack {rack.rack_id} bay {rack.bays[bay_id].bay_id} shelf {shelf.shelf_id}."

    return "No available space in bay."



racks = [Rack(id=i) for i in range(NUM_OF_RACKS)]

inputs['Date'] = pd.to_datetime(inputs['Date'], format="%d/%m/%Y")

for date, day_data in inputs.groupby(inputs['Date'].dt.date):
    for index, row in day_data.iterrows():
        rack = int(row['Rack'].split('Rack ')[1])
        bay = int(row['Bay'])
        category = row['Category']
        pallet = Europallet(category=category)
        add_pallet(racks[rack - 1], bay - 1, pallet)
    print(f"Processed data for {date}")



