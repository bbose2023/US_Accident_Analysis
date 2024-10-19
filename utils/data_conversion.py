# Example MongoDB output
# fatalities_by_state = [
#     {'_id': {'State': 'Alabama', 'StateID': 1, 'Year': 2022}, 'total_fatalities': 913},
#     {'_id': {'State': 'Alaska', 'StateID': 2, 'Year': 2022}, 'total_fatalities': 75},
#     {'_id': {'State': 'Arizona', 'StateID': 4, 'Year': 2022}, 'total_fatalities': 1183}
# ]

# flattened_data = flatten_list_of_dicts(fatalities_by_state)

# Output - {'State': 'Alabama', 'StateID': 1, 'Year': 2022, 'total_fatalities': 913}
# {'State': 'Alaska', 'StateID': 2, 'Year': 2022, 'total_fatalities': 75}
# {'State': 'Arizona', 'StateID': 4, 'Year': 2022, 'total_fatalities': 1183}

def flatten_dict(d, parent_key='', sep=''):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def flatten_list_of_dicts(list_of_dicts):
    flattened_list = [flatten_dict(d) for d in list_of_dicts]
    return flattened_list