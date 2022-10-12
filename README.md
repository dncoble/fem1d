# fem1d
Python wrapper for FEM1D program from J.N. Reddy. Use this to generate the problem data cards or alternatively solve straight from python. 
## How to use
### FEM1DProblemData
Initialize an `FEM1DProblemData` object with the list `nodes_per_element` pass the problem data as a dictionary to `**kwargs`. 
```
nodes_per_element = [2, 3, 2, 2]
problem_data = {...} # dictionary
fea_mesh = FEM1DProblemData(nodes_per_element, **problem_data)
fea_mesh.save_card('example.inp') # to produce the data card file
solution = fea_mesh.run() # to run the problem and get the output card as a string
```
Names and descriptions of the required problem data are given in the table below. Some data is generated automatically when the information is redundant.

### EulerBernoulliBeam
For Euler-Bernoulli beam problems, `EulerBernoulliBeam` implements `FEM1DProblemData` .
## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

I couldn't verify the license for FEM1D by J.N. Reddy, although the program is [freely available](https://highered.mheducation.com/sites/0072466855/student_view0/executables.html) on the McGraw Hill website. Before running the code, download the .exe and place it in [/fem1d](/fem1d).
