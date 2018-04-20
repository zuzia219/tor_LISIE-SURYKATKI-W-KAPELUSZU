import pandas as pd
import numpy as np
import json

transactions = '../DATA/braincode-dataset-tx.json'
views = '../DATA/braincode-dataset-items_no_c.json'


def read_views():
    data = []
    json_to_dict = {'ttimestamp':[], 
		   'offer_id':[],
		   'category_id':[],
		   'latitude':[],
		   'longitude':[]}
    with open (views) as f:
        for line in f:
            json_line = json.loads(line)
            json_offer = json_line['offer']
            json_location = json_line['location']
            json_to_dict['ttimestamp'].append(json_line['ttimestamp'])

            json_to_dict['offer_id'].append(json_offer['id'])
            if 'category_id' in json_offer.keys():
                 json_to_dict['category_id'].append(json_offer['category_id'])
            else:
                json_to_dict['category_id'].append(['np.nan'])

            json_to_dict['latitude'].append(json_location['latitude'])
            json_to_dict['longitude'].append(json_location['longitude'])

        df = pd.DataFrame(json_to_dict)

    return df

def read_transactions():
    data = []
    json_to_dict = {'ttimestamp':[], 
		   'offer_id':[],
		   'category_id':[],
		   'latitude':[],
		   'longitude':[],
		   'item_quantity':[]}
    with open (transactions) as f:
        for line in f:
            json_line = json.loads(line)
            json_offer = json_line['offer']
            json_location = json_line['location']
            json_to_dict['ttimestamp'].append(json_line['ttimestamp'])

            json_to_dict['offer_id'].append(json_offer['id'])
            if 'category_id' in json_offer.keys():
                 json_to_dict['category_id'].append(json_offer['category_id'])
            else:
                json_to_dict['category_id'].append(['np.nan'])

            json_to_dict['latitude'].append(json_location['latitude'])
            json_to_dict['longitude'].append(json_location['longitude'])

            json_to_dict['item_quantity'].append(json_line['item_quantity'])

        df = pd.DataFrame(json_to_dict)

    return df


