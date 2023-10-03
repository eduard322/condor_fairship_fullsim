import numpy as np
import ROOT

# Create the NumPy array with string data
array = np.array([f"abc_{i}" for i in range(10)])

# Create a dictionary to hold the data
data_dict = {"strings": array}

# Create the ROOT DataFrame using MakeNumpyDataFrame method
rdf = ROOT.RDF.MakeNumpyDataFrame(data_dict)

# Print the DataFrame to check the contents (optional)
rdf.Display()
