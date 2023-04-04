# PFCands Plotting using RDataFrame

RDataFrame is a C++ class provided by the ROOT data analysis framework for interactive data analysis and manipulation. It provides a high-level interface for working with large datasets, allowing users to perform complex data processing and analysis tasks efficiently.

This script uses ROOT to plot the PFCands_pt and nPFCands variables from a ROOT file. It also requests a cut-flow report to print out.

To run this script, you need to have ROOT installed on your system.

## Usage

Get the code:

```
git clone git@github.com:cms-dpoa/cat-hackathon.git
cd cat-hackathon
```

Start the docker container:

```
docker run -it --rm -v $PWD:/workdir rootproject/root bash
```

In the container prompt:

```
cd ../workdir/analysis/rdataframe
python rdf_plot.py
exit
```

## Input

PFNanoAOD file from the `../../data` directory, hardcoded for now, to be configured to get the output of a production step


## How to use

1. Set the number of threads to use based on your system by modifying the argument to ROOT.ROOT.EnableImplicitMT() function.

2. Set the input file path by modifying the fname variable.
3. Set the histogram parameters by modifying the bins, low, and up variables for both histograms.
4. Run the script.
5. Output
The script will output two histograms in PNG format, PFCands_pt.png and nPFCands.png. It will also print out the cut-flow report. 
- PF_pt.png: PF candidate pt (plot)
- PF_n.png: N of PF candidates (plot)
- PF_n.txt: N of PF candidates (array)