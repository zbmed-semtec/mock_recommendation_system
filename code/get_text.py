import json
import argparse
import pandas as pd


def convert_text_to_json(input_tsv_file, output_jsonfile):
    file_text = pd.read_csv(input_tsv_file, sep='\t',names=['pmid', 'title', 'abstract'])

    dataset = []
    for _, row in file_text.iterrows():
        try:
            data_dict = {
            "pmid" : int(row['pmid']),
            "title": row['title'],
            "abstract": row['abstract']
            }
        except:
            continue
        dataset.append(data_dict)

    with open (output_jsonfile, 'w') as jsonfile:
        for data in dataset:
            json.dump(data, jsonfile)
            jsonfile.write('\n')



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Path to input RELISH Text TSV file")
    parser.add_argument("-o", "--output", type=str, help="Path to output RELISH Text jsonl file")
    args = parser.parse_args()
    convert_text_to_json(args.input, args.output)
