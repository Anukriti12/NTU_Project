import argparse
from core import *
from demo import *
import numpy as np
import pandas as pd
import pickle

def ClassifyMalware(data):
    RFmodel = pickle.load(open('final_models/rf_final.pkl', 'rb'))
    predicted_value = RFmodel.predict(data)
    return predicted_value

def classify_with_api_calls(data_files):
	behavioral_profiles = [APIProfile(data_file) for data_file in data_files]
	feature_extractor = APIFeatureExtractor(behavioral_profiles, data_files)
	vectorized_data = feature_extractor.get_vectorized_data()

	dataset = pd.read_csv("dataset.csv")
	length = np.shape(dataset)[1]-1

	final_data=np.empty((0,151))
	for row in vectorized_data:
	    print(np.shape(row))
	    row = np.pad(row, (0,length-np.shape(row)[0]),'constant')
	    #print(row)
	    final_data = np.append(final_data, np.array([row]), axis=0)
	    print(final_data.shape)

	malware_group = ClassifyMalware(final_data)
	print('Done!!!!!! -   ', malware_group)


def main():
	parser = argparse.ArgumentParser(description='Classifying new Malware')
	parser.add_argument('-d', '--data-dir', default='data/', type=str)
	args = parser.parse_args()

	#Report loaded in memory
	data_files = load_directory_files(args.data_dir)
	classify_with_api_calls(data_files)

if __name__ == '__main__':
	print('Classifying.......')
	main()