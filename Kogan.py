'''
This program finds the average cubic weight for all products in the "Air Conditioners" category list in the Kogan API.
Cubic weight is calculated by multiplying the length, height and width of the parcel. The result is then multiplied
by the industry standard cubic weight conversion factor of 250.
Author - Samuel O'Halloran
'''

import requests

URL = "http://wp8m3he1wt.s3-website-ap-southeast-2.amazonaws.com"
# Conversion factor.
CON_FACT = 250
# Used to convert size dimensions from centimeters to meters.
CON_TO_MET = 1000000


def main():

    end_point = '/api/products/1'
    total_size: float = 0
    total_units: int = 0

    # Search pages for 'Air Conditioners'
    while True:
        try:
            response = requests.get(URL + end_point).json()
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            break
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            break
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            break
        except requests.exceptions.RequestException as err:
            print("Something went wrong:", err)
            break

        for obj in response['objects']:
            if str(obj['category']) == "Air Conditioners":
                length = obj['size']['length']
                height = obj['size']['height']
                width = obj['size']['width']
                size = round(length * width * height, 5)
                # Omit any listing that have negative values.
                if size >= 0:
                    total_units += 1
                    total_size += size
        end_point = response['next']
        # Break if no more pages
        if end_point is None:
            break

    total_weight = total_size * CON_FACT / CON_TO_MET
    average_weight = total_weight / total_units
    print('The average weight of all listings in the "Air Conditioners" category is ', round(average_weight, 4), 'kg.', sep='')

if __name__ == '__main__':
    main()