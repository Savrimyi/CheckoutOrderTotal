import re
import json

valid_unit_types = ['each', 'per pound']

class Item():
    def __init__(self, name, price_per_unit, unit_type):
        #Validate input before initializing
        self.validate_parameters(name, price_per_unit, unit_type)
        self.name = name
        self.price_per_unit = price_per_unit
        self.unit_type = unit_type
        self.special_price = None
        self.markdown = 0

    def validate_parameters(self, name, price_per_unit, unit_type):
        if not type(name) == str: raise(ValueError)
        if not (type(price_per_unit) == int or type(price_per_unit) == float) or price_per_unit < 0: raise(ValueError)
        if not unit_type in valid_unit_types: raise(ValueError)

    def get_price(self):
        return self.price_per_unit - self.markdown

    def update_price(self, new_price):
        self.validate_parameters(self.name, new_price, self.unit_type)
        self.price_per_unit = new_price
        self.markdown = 0

    def markdown_price(self, markdown):
        if markdown is None or markdown < 0: raise(ValueError)
        self.markdown = markdown

    def get_special_price(self):
        return self.special_price

    def set_special_price(self, special):

        if special is None or \
        re.search(r'^buy \d+ items, get \d+ at %\d+ off', special.lower()) or \
        re.search(r'^buy \d+ get \d+ (free|half off)', special.lower()) or \
        re.search(r'^\d+ for \$\d+', special.lower()) or \
        re.search(r'^buy \d+, get \d+ of equal or lesser value for %\d+ off', special.lower()):
            if re.search(r'%\d+ off', special.lower()):
                percentage = re.search(r'%\d+ off', special.lower()).group().strip('%').strip(' off')
                if int(percentage) > 100 or int(percentage) < 0:
                    raise(ValueError)
            self.special_price = special
        else:
            raise(ValueError)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.name == other.name and \
                self.price_per_unit == other.price_per_unit and \
                self.unit_type == other.unit_type and \
                self.special_price == other.special_price