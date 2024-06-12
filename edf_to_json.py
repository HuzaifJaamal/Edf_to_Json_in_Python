import pyedflib
import json
from datetime import datetime

def convert_to_serializable(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def edf_to_json(edf_file_path, json_file_path):
    # Open the EDF file
    f = pyedflib.EdfReader(edf_file_path)
    
    # Get the header information
    header = f.getHeader()
    
    # Convert datetime objects in the header to strings
    for key, value in header.items():
        if isinstance(value, datetime):
            header[key] = value.isoformat()
    
    # Get the signal labels
    signal_labels = f.getSignalLabels()
    
    # Read all signals
    signals = {}
    for i in range(f.signals_in_file):
        signals[signal_labels[i]] = f.readSignal(i).tolist()
    
    # Construct the data dictionary
    data = {
        "header": header,
        "signals": signals
    }
    
    # Write to a JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4, default=convert_to_serializable)
    
    # Close the EDF file
    f._close()
    del f

if __name__ == "__main__":
    # Specify the paths directly in the code
    edf_file_path = 'data/ecgca102.edf'  # Path to the EDF file
    json_file_path = 'output.json'     # Path to the output JSON file
    
    edf_to_json(edf_file_path, json_file_path)
