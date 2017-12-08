import util
import argparse
import os
args = util.parse(argparse.ArgumentParser())

#cache references
util.experiment["create_script"](util.experiment["run"], "generate_references", "python {0} -e \"{1}\"".format(os.path.join(util.src, "generate_references.py"), util.read_path(args.experiment)), util.experiment["matrix_registry"].keys())

#cache profile
util.experiment["create_script"](util.experiment["run"], "generate_profile", "python {0} -e \"{1}\"".format(os.path.join(util.src, "generate_profile.py"), util.read_path(args.experiment)), [])

#cache spmv_times
util.experiment["create_script"](util.experiment["run"], "generate_spmv_records", "python {0} -e \"{1}\"".format(os.path.join(util.src, "generate_spmv_records.py"), util.read_path(args.experiment)), util.experiment["matrix_registry"].keys())