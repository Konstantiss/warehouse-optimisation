import pandas as pd

inputs = pd.read_csv('warehouse_log_inputs.csv')
outputs = pd.read_csv('warehouse_log_outputs.csv')

NUM_OF_RACKS = 2
BAYS_PER_RACK = 10
SHELVES_PER_BAY = 4
PALLETS_PER_SHELF = 3
SHELF_HEIGHT = 1.8
BAY_WIDTH = 3
FORKLIFT_MOVE_SPEED = 1.2 #m/s
FORKLIFT_LIFT_SPEED = 0.5 #m/s
PALLET_WIDTH = 0.8

class Rack:
    def __init__(self, bays):
        self.bays = bays

class Bay:
    def __init__(self, shelves):
        self.shelves = shelves

    def add_pallet(self, pallet):
        if pallet.category == 'A':

            '''
            Category A items can be placed on the bottom shelves. 
            Here the bottom shelf is consider to be index 0.
            '''

            if len(self.shelves[0].pallets) < self.shelves[0].maxNumOfPallets:
                self.shelves[0].add_pallet(pallet)
            else:
                print("Error! Maximum number of pallets reached for this shelf.")
        elif pallet.category == 'B':

            '''
            Category B items can be placed on the bottom shelves. 
            Here the bottom shelf is consider to be the maxium index.
            '''

            if self.shelves[-1].numOfPallets < self.shelves[-1].maxNumOfPallets:
                self.shelves[-1].add_pallet(pallet)
            else:
                print("Error! Maximum number of pallets reached for this shelf.")
        else:
            for shelf in self.shelves:
                palletAdded = False
                if len(shelf.pallets) < shelf.maxNumOfPallets:
                    shelf.add_pallet(pallet)
                    palletAdded = True
                else:
                    print("Error! Maximum number of pallets reached for this shelf.")
                if palletAdded:
                    break

class Shelf:
    def __init__(self, pallets):
        self.numOfPallets = 0
        self.maxNumOfPallets = PALLETS_PER_SHELF
        self.pallets = pallets
    def add_pallet(self, pallet):
        self.pallets.append(pallet)
        self.numOfPallets += 1

class Europallet:
    def __init__(self, category):
        self.category = category

pallets = []

shelves = [Shelf(pallets) for i in range(SHELVES_PER_BAY)]

bays = [Bay(shelves) for i in range(BAYS_PER_RACK)]

racks = [Rack(bays) for i in range(NUM_OF_RACKS)]

pallet = Europallet(category='B')
racks[0].bays[0].add_pallet(pallet)

print('a')