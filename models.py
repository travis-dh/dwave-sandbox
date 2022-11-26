# ----------------------------------------------------------------------
# This program solves a simple Ising model with two coupling strengths J
# both set to 1, with no external magnetic field term h on any of the 
# three nodes.
#
# @author Travis Howard
# @date 25 Nov 2022
# ----------------------------------------------------------------------

import os
import dimod
import neal
import numpy as np
from dwave.system import DWaveSampler, EmbeddingComposite

# Define the system.
J = {(0, 1): 1, (1, 2): 1}
offset = 0.0

# Hard-coded values to test "near zero" case
h_vals = [0, 10**(-18), 10**(-16), 10**(-14), 10**(-12),
          10**(-9), 10**(-6), 10**(-5), 10**(-4), 2*10**(-3)]

# This list will keep `dict`-type entries to help with 
# instantiating Binary Quadratic Models
h = []

for val in h_vals:
    h.append({key: val for key in np.arange(3)})

def sim_anneal(h, J, num_reads=10):
    '''
    Run a neal.SimulatedAnnealingSampler given coupling
    strengths and external magnetic field contributions.

    :param h: External magnetic field(s).
    :param J: Coupling strength(s).
    :param num_reads: The number of samples taken.
    :returns: A structured type which contains data of 
              the sampler's response. 
    '''
    neal_sampler = neal.SimulatedAnnealingSampler()
    neal_sampleset = neal_sampler.sample_ising(h, J, num_reads=num_reads)
    return neal_sampleset

def dwave_sampler(h, J, offset, num_reads=5000, label='models.py'):
    '''
    Run samples on a D-Wave computer with minor-embedding given
    a binary quadratic model from coupling strengths and external
    magnetic field contributions.

    :param h: External magnetic field(s).
    :param J: Coupling strength(s).
    :param offset: An energy term which serves as a constant.
    :param num_reads: The number of samples taken.
    :returns: A structured type which constains data of 
              the sampler's response.
    '''
    bqm = dimod.BinaryQuadraticModel(h, J, offset, 'SPIN')

    sampler = EmbeddingComposite(DWaveSampler())
    # This is where time gets used. Exercise caution!
    sampleset = sampler.sample(bqm, num_reads=num_reads, label=label)
    return sampleset

if __name__ == '__main__':
    # Remove old files
    path = os.getcwd() + '/output/'
    [os.remove(os.path.join(path, f)) for f in os.listdir(path) if f.endswith('.csv')]

    '''
    Samples are taken here. Each entry in `h` is in a `dict` format
    which is passable to a dimod/D-Wave sampler: an entry in
    `h`, called `val`, has the Ising Model nodes as its keys and the
    external magnetic field contributions as key values (see `h_vals`
    above for the values each node will share at a given iteration).
    '''
    for i, val in enumerate(h):
        # Simulated annealing -> to df -> to .csv
        neal_sample_set = sim_anneal(val, J)
        df = neal_sample_set.to_pandas_dataframe()
        df.to_csv(f'{path}/neal_output_{i+1}.csv')

        # D-Wave sampler -> to df -> to .csv
        # TIME WILL BE USED HERE FOR A WHOLE BATCH!
        dwave_sample_set = dwave_sampler(val, J, offset, label=f'models_CALL_{i+1}.py')
        fd = dwave_sample_set.to_pandas_dataframe()
        fd.to_csv(f'{path}/dwave_output_{i+1}.csv')