import numpy as np

import aoc_helper
from SubField import SubField

# DEBUG = True
DEBUG = False

field = np.array([[tile for tile in line.strip()] for line in aoc_helper.ged_data(DEBUG)])

field_shape = field.shape

def get_all_tiles_in_subfields(_sub_fields: [SubField]) -> [tuple[int, int]]:
    tiles = []
    for _sub_field in _sub_fields:
        tiles += _sub_field.tiles
    return tiles

sub_fields = []
for row in range(field_shape[0]):
    for col in range(field_shape[1]):
        # print(row, col)
        field_coords = (row, col)
        field_type = field[*field_coords]
        sub_fields_of_same_type = list(filter(lambda x: x.field_type == field_type, sub_fields))

        # Sub-filed of this type does not exist, create it and continue to next tile
        if len(sub_fields_of_same_type) == 0:
            new_sub_field = SubField(field_type)
            new_sub_field.add_tile(field_coords)
            sub_fields.append(new_sub_field)
            continue

        # tile is not assigned to any sub-field, it might be added to existing one, or we have to create a new sub-field
        elif field_coords not in get_all_tiles_in_subfields(sub_fields_of_same_type):
            field_neighbours = SubField.get_neighbour(field_coords, field)

            #check if neighbours are in any same-type sub-field, add them to the subfield if so
            neighbour_subfields = []
            for sub_field in sub_fields_of_same_type:
                if set(field_neighbours).intersection(sub_field.tiles):
                    sub_field.add_tile(field_coords)
                    neighbour_subfields.append(sub_field)
            if len(neighbour_subfields) > 1:
                # two or more sub-field should be merged
                new_subfield = SubField.merge_subfields(neighbour_subfields)
                for neighbour_subfield in neighbour_subfields:
                    sub_fields.remove(neighbour_subfield)
                sub_fields.append(new_subfield)


            if len(neighbour_subfields) == 0:
                new_sub_field = SubField(field_type)
                new_sub_field.add_tile(field_coords)
                sub_fields.append(new_sub_field)

total_cost = 0
total_cost_with_discount = 0
for sub_field in sub_fields:
    # print(f"A region of {sub_field.field_type} plants with price {sub_field.area} * {sub_field.perimeter} = {sub_field.get_fence_cost()}.")
    # print(f"A region of {sub_field.field_type} plants with price {sub_field.area} * {sub_field.perimeter} = {sub_field.get_fence_cost(discount=True)} with discount.")
    total_cost += sub_field.get_fence_cost()
    total_cost_with_discount += sub_field.get_fence_cost(discount=True)
    # with open(f"output/{sub_field.field_type} -{sub_field.uuid}.txt", "w") as output_file:
    #     output_file.write(sub_field.get_string_representation(field_shape))

print(f"Total fence cost: {total_cost}")
print(f"Total fence cost with discount: {total_cost_with_discount}")