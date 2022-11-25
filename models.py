# ----------------------------------------------------------------------
# This program solves a simple Ising model with two coupling strengths J
# both set to 1, with no external magnetic field term h on any of the 
# three nodes.
#
# @author Travis Howard
# @date 25 Nov 2022
# ----------------------------------------------------------------------

import dimod
import neal
from dwave.system import DWaveSampler, EmbeddingComposite

# Define the system.
h = {0: 0, 1: 0, 2: 0}
J = {(0, 1): 1, (1, 2): 1}
offset = 0.0

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
    # Simlated Annealing with output saved to file.
    neal_sample_set = sim_anneal(h, J)
    print(neal_sample_set, file=open('neal_output.txt', 'w'))

    # D-Wave next. Time is used once `dwave_sampler` is called.
    # Also save output to file.
    dwave_sample_set = dwave_sampler(h, J, offset)
    print(dwave_sample_set, file=open('dwave_output.txt', 'w'))
