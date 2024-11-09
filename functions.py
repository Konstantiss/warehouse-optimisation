from entities import *
from constants import *


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

    if len(bay_ids) > 1:  # If there are > 1 candidate pallets
        retrieval_times = []
        distances_covered = []
        for index in range(len(bay_ids)):
            retrieval_time, distance_covered = calculate_retrieval_time(bay_ids[index], shelf_ids[index])
            retrieval_times.append(retrieval_time)
            distances_covered.append(distance_covered)
        optimal_index = retrieval_times.index(min(retrieval_times))
        racks[optimal_index].bays[bay_ids[optimal_index]].shelves[shelf_ids[optimal_index]].remove_pallet(
            pallets[optimal_index])
        return (
            f"Retrieved pallet of {pallets[optimal_index].category} from rack {racks[optimal_index].rack_id + 1} bay "
            f"{bay_ids[optimal_index] + 1} shelf {shelf_ids[optimal_index] + 1}."), \
            retrieval_times[optimal_index], distances_covered[optimal_index]
    elif len(bay_ids) == 1:
        retrieval_time, distance_covered = calculate_retrieval_time(bay_ids[0], shelf_ids[0])
        racks[rack_ids[0]].bays[bay_ids[0]].shelves[shelf_ids[0]].remove_pallet(pallets[0])
        return f"Retrieved pallet of {pallets[0].category} from rack {rack_ids[0] + 1} bay {bay_ids[0] + 1} shelf {shelf_ids[0] + 1}", retrieval_time, distance_covered
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


def add_preexisting_stock(racks, pallets_to_add):
    for rack in racks:
        pallet_count = 0
        for bay in reversed(rack.bays):
            if pallet_count == pallets_to_add:
                break
            else:
                pallet = Europallet(category='Category A')
                add_pallet(rack, bay.bay_id, pallet)
                pallet_count += 1

    for rack in racks:
        pallet_count = 0
        for bay in reversed(rack.bays):
            if pallet_count == pallets_to_add:
                break
            else:
                pallet = Europallet(category='Category B')
                add_pallet(rack, bay.bay_id, pallet)
                pallet_count += 1

    for rack in racks:
        pallet_count = 0
        for bay in reversed(rack.bays):
            if pallet_count == pallets_to_add:
                break
            else:
                pallet = Europallet(category='Category C')
                add_pallet(rack, bay.bay_id, pallet)
                pallet_count += 1


def simulate(racks, inputs, outputs):
    total_placement_time = 0
    total_retrieval_time = 0
    total_placement_distance_covered = 0
    total_retrieval_distance_covered = 0
    for date, inputs_day_data in inputs.groupby(inputs['Date'].dt.date):
        day_placement_time = 0
        day_retrieval_time = 0
        day_distance_covered_placement = 0
        day_distance_covered_retrieval = 0
        outputs_day_data = outputs[outputs['Date'] == inputs_day_data['Date'].iloc[0]]

        for index, row in inputs_day_data.iterrows():
            rack = int(row['Rack'].split('Rack ')[1])  # Get only the number from 'Rack X'
            bay = int(row['Bay'])
            category = row['Category']
            pallet = Europallet(category=category)
            _, placement_time, distance_covered = add_pallet(racks[rack - 1], bay - 1, pallet)
            day_placement_time += placement_time
            day_distance_covered_placement += distance_covered

        for index, row in outputs_day_data.iterrows():
            category = row['Category']
            _, retrieval_time, distance_covered = retrieve_pallet(racks, category)

            day_retrieval_time += retrieval_time
            day_distance_covered_retrieval += distance_covered

        total_placement_time += day_placement_time
        total_retrieval_time += day_retrieval_time
        total_placement_distance_covered += day_distance_covered_placement
        total_retrieval_distance_covered += day_distance_covered_retrieval
        print(f"Processed data for {date}")
    return total_placement_time, total_retrieval_time, total_placement_distance_covered, total_retrieval_distance_covered
