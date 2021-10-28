# multilevel-critical-node-problem

Implementation of the multilelvel approach to the critical node problem outlined in the paper by A. Baggio et al: https://pubsonline.informs.org/doi/abs/10.1287/opre.2020.2014

Implemented with guboripy 9.1 and python 3.8.

## Using the algorithm

The algorithm is run via the main command module: run_MCNv2.py
Contained within this module are functions to run the algo on
individual random graph instances, or on sets of graph instances
that share characteristics such as density, |V|, or budget set.

Use the algorithm by changing the main() function of this module.
Examples of function use can be found commented out in main()

## Modules

MCNv2 algorithm utilises three modules containing MIPs:
Defend.py
AttackDefend.py
ProtectAttackDefend.py

## Data

Datasets found in Instances folder.

## Results

Results of this implementation (v2) for respective instances found in results_v2 folder, nested within folder bearing name of graph structure of dataset.

Summaries of results and benchmark comparisons against the results of Baggio et al can be found in results_summary.csv