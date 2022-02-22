"""
Quantum AND gate implemented through D-WAVE Leap API

"""

import dimod
import traceback
import pdb
import sys

from dwave.system import EmbeddingComposite
from dwave.system import DWaveSampler

import dwave.inspector


def main():
    # some WIP code that maybe raises an exception
    j01 = 3.5
    j02 = 10.0
    j12 = 10.0
    h0 = -5.
    h1 = -2.
    h2 = -3.
    linear = {1: h0, 2: h1, 3: h2}
    quadratic = {(1, 2): j01, (1, 3): j02, (2, 3): j12}
    # j01*x1*x2 + j02*x1*x3 + j12*x2*x3- x1 - 2*x2 - 3*x3

    # Formulate a QUBO problem as a Binary Quadratic Model
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, -0.0, dimod.BINARY)

    # Use the D-Wave sampler. For a normal sampler, use
    sampler = EmbeddingComposite(DWaveSampler(solver={'qpu':True}))

    # Sample the BQM based on the number of "num_reads" and get the probabilities.
    response = sampler.sample(bqm, num_reads=shots)

    # print('************ Method 2 - Binary Quadratic Model - Results ************** \n')
    for res in response.data(['sample', 'energy', 'num_occurrences']):
        print('|s1 = {} | s2 = {} | s3 = {} | Energy = {} | Probability  = {} %'.format(
            res.sample[1], res.sample[2], res.sample[3],
            res.energy,
            res.num_occurrences * 100 / shots))


    return 0


if __name__ == "__main__":
    try:
        shots = 1500
        ret = main()
    except:
        traceback.print_exc()
        pdb.post_mortem()
    sys.exit(ret)
