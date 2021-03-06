"""All single flight related functionalities and representations"""

from flight_genie.utils import (
    get_value_by_key_in_pairs_list,
    get_numerical_value,
    month_day_from_date,
    weekday_from_date,
    country_from_airport,
    city_code_from_airport,
    days_in_range,
)


class Flight(object):
    """Simple representation of a flight. Just containing properties"""

    PARAMETERS = (
        'date',
        'dayofmonth',
        'weekday',
        'outbounddate',
        'outbounddayofmonth',
        'outboundweekday',
        'inbounddate',
        'inbounddayofmonth',
        'inboundweekday',
        'originairport',
        'origincitycode',
        'origincountry',
        'destinationairport',
        'destinationcitycode',
        'destinationcountry',
        'carriercode',
        'carriertype',
        'adults',
        'children',
        'daystodeparture',
        'dayslengthofstay',
        'priceusd',
        'platform',
        'isota'
    )

    def __init__(self, pairs_list):
        """Sets the flight properties from a list of pairs"""
        self.__pairs_list = pairs_list

    @classmethod
    def get_from_core_data(cls, pairs_list):
        """Get a full flight from the core data

        Infers the values of some parameters. See README for more details
        """
        full_pairs_list = []
        current_parameters = [p[0] for p in pairs_list]
        for param in cls.PARAMETERS:
            if param in current_parameters:
                param_val = get_value_by_key_in_pairs_list(pairs_list, param)
            else:
                inferring_dict = cls.INFERRING_FUNCTIONS[param]
                core_vals = (get_value_by_key_in_pairs_list(pairs_list, c)
                             for c in inferring_dict['core'])
                param_val = inferring_dict['function'](*[v for v in core_vals])
            full_pairs_list.append((param, param_val))
        return cls(full_pairs_list)

    def get_attribute(self, attr_name):
        """Gets the value of a atributed labels attr_name"""
        return get_value_by_key_in_pairs_list(self.__pairs_list, attr_name)

    def to_numerical_list(self, excluded_attributes=[]):
        """Return an array of numbers by a certain order"""
        return [get_numerical_value(pair[1])
                for pair in self.__pairs_list if
                pair[0] not in excluded_attributes]

    def to_string_list(self, excluded_attributes=[]):
        """Return an array of strings by a certain order."""
        return [str(v) for v in self.to_numerical_list(excluded_attributes)]

    def get_travellers_count(self):
        """Return the number of adults + children for the purchase"""
        return (float(self.get_attribute("adults")) +
                float(self.get_attribute("children")))

    def get_price_per_ticket(self):
        """Get the price for a single ticket in the purchase"""
        return (float(self.get_attribute('priceusd')) /
                self.get_travellers_count())

    def __str__(self):
        """A good representation as a string"""
        to_append = ''
        for pair in self.__pairs_list:
            to_append += '{}: {} '.format(pair[0], pair[1])
        return to_append

    INFERRING_FUNCTIONS = {
        'dayofmonth': {
            'core': ['date'],
            'function': month_day_from_date
        },
        'weekday': {
            'core': ['date'],
            'function': weekday_from_date
        },
        'outbounddayofmonth': {
            'core': ['outbounddate'],
            'function': month_day_from_date
        },
        'outboundweekday': {
            'core': ['outbounddate'],
            'function': weekday_from_date
        },
        'inbounddayofmonth': {
            'core': ['inbounddate'],
            'function': month_day_from_date
        },
        'inboundweekday': {
            'core': ['inbounddate'],
            'function': weekday_from_date
        },
        'origincitycode': {
            'core': ['originairport'],
            'function': city_code_from_airport
        },
        'origincountry': {
            'core': ['originairport'],
            'function': country_from_airport
        },
        'destinationcitycode': {
            'core': ['destinationairport'],
            'function': city_code_from_airport
        },
        'destinationcountry': {
            'core': ['destinationairport'],
            'function': country_from_airport
        },
        'daystodeparture': {
            'core': ['date', 'outbounddate'],
            'function': days_in_range
        },
        'dayslengthofstay': {
            'core': ['outbounddate', 'inbounddate'],
            'function': days_in_range
        },
    }
