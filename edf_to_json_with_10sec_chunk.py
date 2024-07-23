""" import pyedflib
import json
from datetime import datetime

def convert_to_serializable(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def edf_to_json(edf_file_path, json_file_path, chunk_duration=5):
    # Open the EDF file
    f = pyedflib.EdfReader(edf_file_path)
    
    # Get the header information
    header = f.getHeader()
    
    # Convert datetime objects in the header to strings
    for key, value in header.items():
        if isinstance(value, datetime):
            header[key] = value.isoformat()
    
    # Get the signal labels and sample frequencies
    signal_labels = f.getSignalLabels()
    sample_frequencies = [f.getSampleFrequency(i) for i in range(f.signals_in_file)]
    
    # Calculate the number of samples per chunk
    samples_per_chunk = [int(freq * chunk_duration) for freq in sample_frequencies]
    
    # Construct the initial data dictionary
    data = {
        "header": header,
        "signals": []
    }
    
    # Write initial data structure to JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4, default=convert_to_serializable)
    
    # Read and write signals in chunks
    num_samples = f.getNSamples()[0]
    num_chunks = num_samples // samples_per_chunk[0]
    
    for chunk_idx in range(num_chunks):
        chunk_data = {}
        for i in range(f.signals_in_file):
            start_idx = chunk_idx * samples_per_chunk[i]
            end_idx = start_idx + samples_per_chunk[i]
            chunk_data[signal_labels[i]] = f.readSignal(i, start=start_idx, n=samples_per_chunk[i]).tolist()
        
        # Append chunk data to JSON file
        with open(json_file_path, 'r+') as json_file:
            data = json.load(json_file)
            data["signals"].append(chunk_data)
            json_file.seek(0)
            json.dump(data, json_file, indent=4, default=convert_to_serializable)
    
    # Close the EDF file
    f._close()
    del f

if __name__ == "__main__":
    # Specify the paths directly in the code
    edf_file_path = 'data/ecgca102.edf'  # Path to the EDF file
    json_file_path = 'output1.json'       # Path to the output JSON file
    
    edf_to_json(edf_file_path, json_file_path)
 """


import pyedflib
import json
from datetime import datetime

def convert_to_serializable(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def edf_to_json(edf_file_path, json_file_path, chunk_duration=10):
    # Open the EDF file
    f = pyedflib.EdfReader(edf_file_path)
    
    # Get the header information
    header = f.getHeader()
    
    # Convert datetime objects in the header to strings
    for key, value in header.items():
        if isinstance(value, datetime):
            header[key] = value.isoformat()
    
    # Get the signal labels and sample frequencies
    signal_labels = f.getSignalLabels()
    sample_frequencies = [f.getSampleFrequency(i) for i in range(f.signals_in_file)]
    
    # Calculate the number of samples per chunk
    samples_per_chunk = [int(freq * chunk_duration) for freq in sample_frequencies]
    
    # Read the first 5-second chunk of each signal
    chunk_data = {}
    for i in range(f.signals_in_file):
        chunk_data[signal_labels[i]] = f.readSignal(i, start=0, n=samples_per_chunk[i]).tolist()
    
    # Construct the data dictionary
    data = {
        "header": header,
        "signals": chunk_data
    }
    
    # Write the data to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4, default=convert_to_serializable)
    
    # Close the EDF file
    f._close()
    del f

if __name__ == "__main__":
    # Specify the paths directly in the code
    edf_file_path = 'data/ecgca102.edf'  # Path to the EDF file
    json_file_path = 'output1.json'       # Path to the output JSON file
    
    edf_to_json(edf_file_path, json_file_path)
