"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    f"""Read near-Earth object information from a CSV file.

    Arguments:
        neo_csv_path {str}: A path to a CSV file containing data about near-Earth objects.
    
    Returns: 
        A collection of `NearEarthObject`s.
    """
    # TODO: Load NEO data from the given CSV file.
    neo_objects = []
    with open(neo_csv_path) as neo_input:
        reader = csv.DictReader(neo_input)
        for neo_object in reader:
            designation, name, diameter, hazardous = neo_object['pdes'], neo_object[
                'name'], neo_object['diameter'], neo_object['pha']
            if not name:
                name = None
            if not diameter:
                diameter = 'NaN'
            hazardous = True if hazardous == 'Y' else False
            neo_objects.append(
                NearEarthObject(
                    designation,
                    name,
                    float(diameter),
                    hazardous))
    return neo_objects


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    Arguments:
        neo_csv_path {str}: A path to a JSON file containing data about close approaches.

    Return:
        A collection of `CloseApproach`es.
    """
    cad_objects = []
    with open(cad_json_path) as cad:
        json_dict = json.load(cad)
        for cad in json_dict['data']:
            designation, time, dist, vel = cad[0], cad[3], cad[4], cad[7]
            cad_objects.append(
                CloseApproach(
                    designation,
                    time,
                    float(dist),
                    float(vel)))
    return cad_objects
