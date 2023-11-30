import sys
sys.path.append('../../../common')
from parser import *

def check_microchips_match_puzzle_requirements(current_bot, microchip_lower, microchip_higher):
    if microchip_lower.chip_id == 17 and microchip_higher.chip_id == 61:
        print("Part 1: " + str(current_bot.bot_id))

class Microchip:

    def __init__(self, chip_id):
        self.chip_id = chip_id

    def __eq__(self, other):
        return self.chip_id == other.chip_id

    def __hash__(self):
        return hash(self.chip_id)

    def __lt__(self, other):
        return True if self.chip_id < other.chip_id else False

class InputInstruction:

    def __init__(self, chip_id, receiving_bot_id):
        self.chip_id = chip_id
        self.receiving_bot_id = receiving_bot_id

class BotInstruction:

    def __init__(self, sending_bot_id, receiving_low_id, receiving_high_id):
        self.sending_bot_id = sending_bot_id
        self.receiving_low_id = receiving_low_id
        self.receiving_high_id = receiving_high_id

class Bot:

    def __init__(self, bot_id, bot_instruction):
        self.bot_id = bot_id
        self.bot_instruction = bot_instruction
        self.current_microchips = set()

    def __eq__(self, other):
        return self.bot_id == other.bot_id

    def __hash__(self):
        return hash(self.bot_id)

    def __str__(self):
        return "[" + str(self.bot_id) + "]"

    def can_execute_instruction(self):
        return len(self.current_microchips) == 2

    def add_microchip(self, microchip):
        self.current_microchips.add(microchip)

    def remove_microchip(self, microchip):
        self.current_microchips.remove(microchip)
        
    def get_sorted_microchips(self):
        return sorted(list(self.current_microchips))

class Output:
    def __init__(self, output_id):
        self.output_id = output_id
        self.microchips = []

    def add_microchip(self, microchip):
        self.microchips.append(microchip)

class InstructionParser:

    def __init__(self):
        self.bot_instructions = []
        self.input_instructions = []

    def store_all_instructions(self, input_args_list):
        for instruction_args in input_args_list:
            self.store_instruction(instruction_args)

    def store_instruction(self, input_args):
        if input_args[0] == "bot":
            self.store_bot_instruction(input_args)
        elif input_args[0] == "value":
            self.store_input_instruction(input_args)

    def store_bot_instruction(self, input_args):
        instruction = BotInstruction(int(input_args[1]), int(input_args[6]), int(input_args[11]))
        self.bot_instructions.append(instruction)
        
    def store_input_instruction(self, input_args):
        instruction = InputInstruction(int(input_args[1]), int(input_args[5]))
        self.input_instructions.append(instruction)

class FactoryManager:

    def __init__(self):
        self.bots_ready = set()
        self.bots = {}

    def add_bots_by_instructions(self, bot_instruction_list):
        for bot_instruction in bot_instruction_list:
            self.add_bot_by_instruction(bot_instruction)

    def add_bot_by_instruction(self, bot_instruction):
        bot = Bot(bot_instruction.sending_bot_id, bot_instruction)
        self.bots[bot.bot_id] = bot

    def execute_all_input_instructions(self, input_instructions_list):
        for input_instruction in input_instructions_list:
            bot = self.bots[input_instruction.receiving_bot_id]
            microchip = Microchip(input_instruction.chip_id)
            bot.add_microchip(microchip)
            if bot.can_execute_instruction():
                self.bots_ready.add(bot)

    def add_bot_to_execution_queue_if_ready(self, bot):
        if bot.can_execute_instruction():
            self.bots_ready.add(bot)

    def execute_bot_instruction(self, bot):
        if not bot.can_execute_instruction():
            raise("Bot cannot execute it's instruction")
        bot_instruction = bot.bot_instruction
        receiving_low_bot = self.bots[bot_instruction.receiving_low_bot_id]
        receiving_high_bot = self.bots[bot_instruction.receiving_high_bot_id]
        microchips = bot.get_sorted_microchips()
        microchip_lower = microchips[0]
        microchip_higher = microchips[1]
        check_microchips_match_puzzle_requirements(bot, microchip_lower, microchip_higher)
        bot.remove_microchip(microchip_lower)
        bot.remove_microchip(microchip_higher)
        receiving_low_bot.add_microchip(microchip_lower)
        receiving_high_bot.add_microchip(microchip_higher)
        self.bots_ready.remove(bot)
        self.add_bot_to_execution_queue_if_ready(receiving_low_bot)
        self.add_bot_to_execution_queue_if_ready(receiving_high_bot)
        
    def run_warehouse_bots(self):
        while len(self.bots_ready) > 0:
            current_bot = list(self.bots_ready)[0]
            self.execute_bot_instruction(current_bot)

puzzle_input = load_multi_line_input_separated_by_spaces()
ip = InstructionParser()
ip.store_all_instructions(puzzle_input)
fm = FactoryManager()
fm.add_bots_by_instructions(ip.bot_instructions)
fm.execute_all_input_instructions(ip.input_instructions)
fm.run_warehouse_bots()
