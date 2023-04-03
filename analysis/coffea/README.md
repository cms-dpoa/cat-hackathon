# Coffea analyser

Simple plotting step for testing purposes.

## Usage

Get the code:

```
git clone git@github.com:cms-dpoa/cat-hackathon.git
cd cat-hackathon
```

Start the docker container:

```
docker run -it --rm -v $PWD:/workdir coffeateam/coffea-base bash
```

In the container prompt:

```
cd /workdir/analysis/coffea
python coffea_plot.py
```

## Input

PFNanoAOD file from the `../../data` directory, hardcoded for now, to be configured to get the output of a production step

## Output

- PF_pt.png: PF candidate pt (plot)
- PF_n.png: N of PF candidates (plot)
- PF_n.txt: N of PF candidates (array)





