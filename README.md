# Tomopy Reconstruction Demo for ALS at ALCF

This tutorial demonstrates how to perform remote tomography reconstructions using Tomopy for ALS data on Polaris at ALCF using [Globus Flows](https://www.globus.org/globus-flows-service).  In this example, Globus flows will launch the application on Polaris and then transfer results from the Eagle filesystem to the Home filesystem at ALCF or a user substituted transfer endpoint at their institution.

This tutorial can be run from anywhere, it only requires a local installation of Globus software (described below) and access to a Globus Compute Endpoint setup by the user on Polaris that has access to tomopy (described in the notebook).

## Tomopy on Polaris

Tomopy has been installed in a conda environment on Polaris at this path which is accessible to members of the IRIBeta allocation: `/eagle/IRIBeta/als/env/tomopy`.

## Local Setup

This tutorial can be run from anywhere.  The only requirement is a local environment, such as a conda environment, that has python 3.11 installed along with the globus packages `globus_compute_sdk` and `globus_cli`.  If you have a local installation of conda you can set up an environment that can run the demo notebook with these steps:

```bash
conda create -n globus_env python==3.11
conda activate globus_env
pip install globus_compute_sdk globus_cli
```

Note that the tomopy environment on Polaris contains python 3.11. It is therefore necessary for this environment on your local machine to have a python version close to this version.

## Tutorial

Proceed with the tutorial in the [notebook](Tomopy_for_ALS.ipynb).