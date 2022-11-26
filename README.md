# dwave-sandbox: A place for toying with D-Wave samplers.
A repository is required for a developer to continue getting their free monthly minute to submit requests to D-Wave. The repository here thus serves as a sandbox.

Inside is a Python script `models.py` which has several simple Ising models to be solved using the [D-Wave OCEAN SDK](https://docs.ocean.dwavesys.com/en/stable/index.html).

### The Ising models
There are a total of ten Ising models defined in `models.py`. Each Ising model has three nodes, with both coupling strengths $J_{ij}=1$. The external magnetic field contributions, however, depend on the trial $i$, $i \in [1, 10]$ such that each node shares 
$h_{1} = 0, \hspace{0.25cm} h_{2} = 10^{-18}, \hspace{0.25cm}  h_{3} = 10^{-16},$ and so on for the corresponding values in `h_vals`.
```python
h_vals = [0, 10**(-18), 10**(-16), 10**(-14), 10**(-12),
          10**(-9), 10**(-6), 10**(-5), 10**(-4), 2*10**(-3)]
```

### Running the script
A D-Wave account with a working API token (and D-Wave time!) is needed. First, install the dependencies by running `pip install -r requirements.txt`, then run `python models.py` to generate `.csv` files to a folder named "output".

Note that this repository makes *several* requests while iterating over the different values of $h_{i}$, not a single request.
