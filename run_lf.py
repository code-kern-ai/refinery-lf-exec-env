#!/usr/bin/env python3

import sys
import requests
import json
import spacy
from spacy.tokens import DocBin
from itertools import islice
import inspect
from collections import defaultdict


def run_classification(record_dict_list):
    lf_results_by_record_id = {}
    for record_dict in record_dict_list:
        label_name = lf(record_dict["data"])
        if label_name is not None:
            lf_results_by_record_id[record_dict["id"]] = [1.0, label_name]
    return lf_results_by_record_id


def run_extraction(record_dict_list):
    lf_results_by_record_id = defaultdict(list)
    for record_dict in record_dict_list:
        for label_name, start_idx, end_idx in lf(record_dict["data"]):
            lf_results_by_record_id[record_dict["id"]].append(
                [1.0, label_name, start_idx, end_idx]
            )
    lf_results_by_record_id = dict(lf_results_by_record_id)
    return lf_results_by_record_id


def run_checks(progress):
    if progress:
        print(
            f"Tokenization is still in progress. Currently {progress}% done.",
            flush=True,
        )
        print("Function will run with reduced set.", flush=True)


# https://www.delftstack.com/howto/python/python-split-list-into-chunks/#split-list-in-python-to-chunks-using-the-lambda-islice-method
def chunk_data(lst, chunk_size):
    lst = iter(lst)
    return iter(lambda: tuple(islice(lst, chunk_size)), ())


def load_data_dict(record):
    if record["bytes"][:2] == "\\x":
        record["bytes"] = record["bytes"][2:]
    else:
        raise ValueError("Unknown byte format in DocBin. Please contact the support.")

    byte = bytes.fromhex(record["bytes"])
    doc_bin_loaded = DocBin().from_bytes(byte)
    docs = list(doc_bin_loaded.get_docs(vocab))
    data_dict = {}
    for (col, doc) in zip(record["columns"], docs):
        data_dict[col] = doc

    for key in record:
        if key in ["record_id", "bytes", "columns"]:
            continue
        data_dict[key] = record[key]
    return data_dict


def parse_data_to_record_dict(record_chunk):
    result = []
    for r in record_chunk:
        result.append({"id": r["record_id"], "data": load_data_dict(r)})
    return result


if __name__ == "__main__":
    _, progress, iso2_code, payload_url = sys.argv
    run_checks(progress)
    print("Preparing data for labeling function.", flush=True)
    # This import statement will always be highlighted as a potential error, as during devtime,
    # the script `labeling_functions` does not exist. It will be inserted at runtime
    from labeling_functions import lf

    vocab = spacy.blank(iso2_code).vocab

    with open("docbin_full.json", "r") as infile:
        docbin_data = json.load(infile)

    is_extraction = inspect.isgeneratorfunction(lf)
    print("Running labeling function.", flush=True)
    workload = len(docbin_data)
    lf_results_by_record_id = {}
    chunk_size = 100
    for idx, chunk in enumerate(chunk_data(docbin_data, chunk_size)):
        record_dict_list = parse_data_to_record_dict(chunk)
        if is_extraction:
            lf_results_by_record_id.update(run_extraction(record_dict_list))
        else:
            lf_results_by_record_id.update(run_classification(record_dict_list))
        progress = (idx * chunk_size) / workload
        print("progress: ", progress, flush=True)

    print("Finished execution.", flush=True)
    requests.put(payload_url, json=lf_results_by_record_id)
