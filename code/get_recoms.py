import json
import argparse
import pandas as pd


def convert_recom_to_json(input_tsv_file, output_jsonfile):
    file_rel = pd.read_csv(input_tsv_file, sep='\t', names=['pmid', 'target_pmid', 'relevance'])

    recom_number_dict = {}

    dataset = []
    for idx, row in file_rel.iterrows():
        try:
            pmid = int(row['pmid'])
            target_pmid = int(row['target_pmid'])
            relevance = int(row['relevance'])

            if pmid not in recom_number_dict:
                recom_number_dict[pmid] = 1
            else:
                recom_number = recom_number_dict[pmid] + 1
                recom_number_dict[pmid] = recom_number

            recom_number = recom_number_dict[pmid]

            data_dict = {
                "pmid": pmid,
                "recom_number": recom_number,
                "target_pmid": target_pmid,
                "relevance": relevance
            }

            dataset.append(data_dict)
        except Exception as e:
            print(f"Error processing row {idx}: {e}")
            continue

    with open(output_jsonfile, 'w') as jsonfile:
        for data in dataset:
            json.dump(data, jsonfile)
            jsonfile.write('\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Path to input RELISH Relevance TSV file")
    parser.add_argument("-o", "--output", type=str, help="Path to output RELISH Recommendations jsonl file")
    args = parser.parse_args()
    convert_recom_to_json(args.input, args.output)