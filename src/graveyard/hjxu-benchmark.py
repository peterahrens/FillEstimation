from util import *
import numpy as np
import json

matrices = ["freeFlyingRobot_5"]
oski_kwargs= {"delta": 0.1}
asx_kwargs= {"epsilon": 0.5, "delta": 0.01}

reference = benchmark("reference", matrices)
oski = benchmark("oski", matrices, **oski_kwargs)
asx = benchmark("asx", matrices, **asx_kwargs)

print("       Reference Time: %g" % np.mean(reference))
print("            OSKI Time: %g" % np.mean(oski))
print("             ASX Time: %g" % np.mean(asx))
print("     ASX/OSKI Speedup: %g" % np.mean(oski/asx))
print("ASX/Reference Speedup: %g" % np.mean(reference/asx))

trials = 100;
references = get_references(matrices)
asx = fill_estimates("asx", matrices, results = True, trials = trials, **asx_kwargs)
oski = fill_estimates("oski", matrices, results = True, trials = trials, **asx_kwargs)
for matrix in matrices:
    asx_outfile = 'asx_' + matrix
    oski_outfile = 'oski_' + matrix
    reference_outfile = 'ref_' + matrix
    with open(asx_outfile, 'w') as asx_out:
        # asx_out.write(str(asx))
        json.dump(asx, asx_out)
    with open(oski_outfile, 'w') as oski_out:
       #  oski_out.write(str(oski))
        json.dump(oski, oski_out)
    with open(reference_outfile, 'w') as ref:
        ref.write(str(references))

get_errors(asx, references)
get_errors(oski, references)

asx = np.concatenate([result["errors"] for result in asx], axis = 0)
oski = np.concatenate([result["errors"] for result in oski], axis = 0)
print("       Over %d trials..." % trials)
print(" Median asx max error: %g" % np.median(asx))
print("Median oski max error: %g" % np.median(oski))
print("   Mean asx max error: %g" % np.mean(asx))
print("  Mean oski max error: %g" % np.mean(oski))
