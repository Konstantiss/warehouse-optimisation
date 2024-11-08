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
    def __init__(self):
        self.numOfPallets = 0
        self.maxNumOfPallets = PALLETS_PER_SHELF
        self.pallets = []
    def add_pallet(self, pallet):
        self.pallets.append(pallet)
        self.numOfPallets += 1
        print("Pallet of " + pallet.category + " added.")

class Bay:
    def __init__(self):
        self.shelves = [Shelf() for i in range(SHELVES_PER_BAY)]

    def add_pallet(self, pallet):
        if pallet.category == 'Category A':

            '''
            Category A items can be placed on the bottom shelves. 
            Here the bottom shelf is consider to be index 0.
            '''

            if len(self.shelves[0].pallets) < self.shelves[0].maxNumOfPallets:
                self.shelves[0].add_pallet(pallet)
            else:
                print("Error! Maximum number of pallets reached for this shelf.")
        elif pallet.category == 'Category B':

            '''
            Category B items can be placed on the bottom shelves. 
            Here the bottom shelf is consider to be the maximum index.
            '''

            if self.shelves[-1].numOfPallets < self.shelves[-1].maxNumOfPallets:
                self.shelves[-1].add_pallet(pallet)
            else:
                print("Error! Maximum number of pallets reached for this shelf.")
        else:
            for shelf in self.shelves:
                palletAdded = False
                if shelf.numOfPallets < shelf.maxNumOfPallets:
                    shelf.add_pallet(pallet)
                    palletAdded = True
                else:
                    print("Error! Maximum number of pallets reached for this shelf.")
                if palletAdded:
                    print("Pallet added.")
                    break

class Rack:
    def __init__(self):
        self.bays = [Bay() for i in range(BAYS_PER_RACK)]


racks = [Rack() for i in range(NUM_OF_RACKS)]

inputs['Date'] = pd.to_datetime(inputs['Date'], format="%d/%m/%Y")

for date, day_data in inputs.groupby(inputs['Date'].dt.date):
    for index, row in day_data.iterrows():
        rack = int(row['Rack'].split('Rack ')[1])
        bay = int(row['Bay'])
        category = row['Category']
        pallet = Europallet(category=category)
        racks[rack - 1].bays[bay - 1].add_pallet(pallet)
    print(f"Processed data for {date}")



