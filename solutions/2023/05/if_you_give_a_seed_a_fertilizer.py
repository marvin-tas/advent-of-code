import sys
sys.path.append('../../../common')
from parser import *
from interval import *
    

class AlmanacManager:
    def __init__(self):
        self.almanac_maps = {}

    def add_almanac_map(self, almanac_map):
        self.almanac_maps[(almanac_map.source_name, almanac_map.destination_name)] = almanac_map

    def get_almanac_map(self, source_name, destination_name):
        return self.almanac_maps[(source_name, destination_name)]
        

class AlmanacMap:
    def __init__(self, source_name, destination_name):
        self.source_name = source_name
        self.destination_name = destination_name
        self.interval_shift_map = {}

    def add_interval_shift_function(self, interval, shift):
        self.interval_shift_map[interval] = shift

    def map_from_source_value(self, value):
        for interval in self.interval_shift_map:
            if interval.includes(value):
                return value + self.interval_shift_map[interval]
        return value

    def map_from_source_interval_set(self, interval_set):
        destination_interval_set = IntegerIntervalSet()
        source_interval_set_copy = interval_set.deep_copy()
        for interval in source_interval_set_copy.intervals:
            unmapped_values = IntegerIntervalSet()
            unmapped_values.add_interval(interval)
            for map_interval in self.interval_shift_map:
                intersection = interval.intersection(map_interval)
                if not intersection.is_empty():
                    unmapped_values.remove_interval(intersection)
                    shifted_interval = intersection.get_shifted_interval(self.interval_shift_map[map_interval])
                    destination_interval_set.add_interval(shifted_interval)
            for unmapped_interval in unmapped_values.intervals:
                destination_interval_set.add_interval(unmapped_interval)
        return destination_interval_set
    
def parse_seed_text(seed_list_text):
    return [int(seed_number) for seed_number in seed_list_text[6:].strip().split(' ')]

def parse_almanac_map_text(almanac_map_text):
    sd_parts = almanac_map_text[0].split(' ')[0].split("-to-")
    almanac_map = AlmanacMap(sd_parts[0], sd_parts[1])
    for map_definition_text in almanac_map_text[1:]:
        values = [int(value_text) for value_text in map_definition_text.split(' ')]
        interval = Interval(values[1], values[1] + values[2] - 1)
        shift = values[0] - values[1]
        almanac_map.add_interval_shift_function(interval, shift)
    return almanac_map

def get_map_definition_lines(puzzle_input):
    map_definition_start_lines = []
    map_definitions = []
    for line_n in range(len(puzzle_input)):
        if "map" in puzzle_input[line_n]:
            map_definition_start_lines.append(line_n)
            if len(map_definition_start_lines) != 1:
                map_definitions.append(puzzle_input[map_definition_start_lines[-2]:map_definition_start_lines[-1]-1])
    map_definitions.append(puzzle_input[map_definition_start_lines[-1]:])
    return map_definitions

puzzle_input = load_multi_line_input_as_string_list()
seed_ids = parse_seed_text(puzzle_input[0]) # part 1

almanac_manager = AlmanacManager()
map_definitions = get_map_definition_lines(puzzle_input)
for map_definition in map_definitions:
    almanac_manager.add_almanac_map(parse_almanac_map_text(map_definition))

seed_to_soil_map = almanac_manager.get_almanac_map("seed", "soil")
soil_to_fertilizer_map = almanac_manager.get_almanac_map("soil", "fertilizer")
fertilizer_to_water_map = almanac_manager.get_almanac_map("fertilizer", "water")
water_to_light_map = almanac_manager.get_almanac_map("water", "light")
light_to_temperature_map = almanac_manager.get_almanac_map("light", "temperature")
temperature_to_humidity_map = almanac_manager.get_almanac_map("temperature", "humidity")
humidity_to_location_map = almanac_manager.get_almanac_map("humidity", "location")

def get_location_for_seed_value(seed_id):
    soil_value = seed_to_soil_map.map_from_source_value(seed_id)
    fertilizer_value = soil_to_fertilizer_map.map_from_source_value(soil_value)
    water_value = fertilizer_to_water_map.map_from_source_value(fertilizer_value)
    light_value = water_to_light_map.map_from_source_value(water_value)
    temperature_value = light_to_temperature_map.map_from_source_value(light_value)
    humidity_value = temperature_to_humidity_map.map_from_source_value(temperature_value)
    return humidity_to_location_map.map_from_source_value(humidity_value)

# Instead of seed IDs - they represents ranges
seed_interval_set = IntegerIntervalSet()
for i in range(len(seed_ids)//2):
    seed_id_start = seed_ids[2 * i]
    seed_id_range = seed_ids[(2 * i) + 1]
    seed_interval_set.add_interval(Interval(seed_id_start, seed_id_start + seed_id_range - 1))

def get_location_for_seed_interval_set(seed_IS):
    soil_IS = seed_to_soil_map.map_from_source_interval_set(seed_IS)
    fertilizer_IS = soil_to_fertilizer_map.map_from_source_interval_set(soil_IS)
    water_IS = fertilizer_to_water_map.map_from_source_interval_set(fertilizer_IS)
    light_IS = water_to_light_map.map_from_source_interval_set(water_IS)
    temperature_IS = light_to_temperature_map.map_from_source_interval_set(light_IS)
    humidity_IS = temperature_to_humidity_map.map_from_source_interval_set(temperature_IS)
    return humidity_to_location_map.map_from_source_interval_set(humidity_IS)

min_location_for_seeds_part_1 = min([get_location_for_seed_value(seed_id) for seed_id in seed_ids])
min_location_for_seeds_part_2 = get_location_for_seed_interval_set(seed_interval_set).intervals[0].lower

print("Part 1: " + str(min_location_for_seeds_part_1))
print("Part 2: " + str(min_location_for_seeds_part_2))




