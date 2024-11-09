from constants import *

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