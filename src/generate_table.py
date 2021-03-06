import util
import argparse
import os
import json
import csv
import time
import sys

tic = time.time()

args = util.parse(argparse.ArgumentParser())

if "table_matrices" in util.experiment:
  table = os.path.join(util.experiment["experiment"], "table")
  util.make_path(table)
  path = os.path.join(util.experiment["experiment"], "table", "table.csv")

  with open(path, 'w') as f:
    writer = None

    for matrix in util.experiment["table_matrices"]:
      row = {}

      row["matrix"] = matrix
      row["matrix_name"] = util.matrix_name(matrix)
      row["matrix_domain"] = util.matrix_domain(matrix)
      row["matrix_size"] = util.matrix_size(matrix)
      row["matrix_nnz"] = util.matrix_nnz(matrix)
      row["matrix_n"] = util.matrix_n(matrix)
      row["matrix_m"] = util.matrix_m(matrix)
      row["normal_spmv_time"] = util.get_spmv_record(matrix)[0][0]

      with open(os.path.join(table, "{}.json".format(matrix)), 'r') as g:
        results = json.load(g)
        row.update(results)

      if not writer:
        writer = csv.DictWriter(f, fieldnames=sorted(row.keys()))
        writer.writeheader()
      writer.writerow(row)

toc = time.time()
sys.stderr.write("generate_table() = {}\n".format(toc - tic))
