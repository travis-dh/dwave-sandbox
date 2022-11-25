# dwave-sandbox: A place for toying with D-Wave samplers.
A repository is required for a developer to continue getting their free monthly minute to submit requests to D-Wave. The repository here thus serves as a sandbox.

Inside is a Python script `models.py` which has a simple Ising model of three nodes.

### The Ising model
This Ising model has no external magnetic field presence, so each node has $h_{i} = 0$. The coupling strengths, however, are both $J_{ij}=1$. To change either of these terms, simply modify the `h` and/or `J` dictionaries.

### Running the script
A D-Wave account with a working API token (and D-Wave time!) is needed. First, install the dependencies by running `pip install -r requirements.txt`, then run `python models.py` to generate output `.txt` files containing the reponse data from the samplers.