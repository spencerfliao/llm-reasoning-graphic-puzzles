import os
import pandas as pd


def load_data(file_path):
    # Load the tsv file into a pandas dataframe
    data = pd.read_csv(file_path, sep="\t")
    return data


def combine_data(data_list):
    # Combine the data into a single dataframe
    combined_data = pd.concat(data_list, axis=0)
    return combined_data


if __name__ == "__main__":
    # Load all files that are tsv from the data folder and combine them
    data_list = []
    data_dir = "./data/annotations"
    for file in os.listdir(data_dir):
        if file.endswith(".tsv"):
            data = load_data(os.path.join(data_dir, file))
            data_list.append(data)
    combined_data = combine_data(data_list)
    # Drop any rows with missing values
    combined_data.dropna(inplace=True)
    # Save the combined data to a new tsv file
    combined_data.to_csv("./data/combined_data.tsv", sep="\t", index=False)
