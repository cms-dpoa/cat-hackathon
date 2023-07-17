# parameters: $1 runas, $2 number of events, $3 inputfile
# if running outside github actions, give any other 1st paramater than github i.e. commands.sh mywork (or omit the paramaters)
# defaults:
if [ -z "$1" ]; then runas=other; else runas=$1; fi
if [ -z "$2" ]; then nevents=20; else nevents=$2; fi
if [ -z "$3" ]; then inputfile=root://eospublic.cern.ch//eos/opendata/cms/Run2015D/DoubleEG/MINIAOD/08Jun2016-v1/10000/00387F48-342F-E611-AB5D-0CC47A4D76AC.root; else inputfile=$3; fi

set -e

# For the plain github action with docker, the area would be available in /mnt/vol
if [ $runas = github ]; then
   sudo chown $USER /mnt/vol
   ls -l /mnt/vol
fi

if [ $runas = reana ]; then
   echo REANA
fi

# Expect to be in /code
source /cvmfs/cms.cern.ch/cmsset_default.sh
# export SCRAM_ARCH=slc7_amd64_gcc700
# cmsrel CMSSW_10_6_30
# cd CMSSW_10_6_30/src/
eval $(scramv1 runtime -sh)
git cms-init --upstream-only -y
git config user.email "me@me.com"
git config user.name "me"
git cms-merge-topic 39040
git clone -b opendata https://github.com/DAZSLE/PFNano.git PhysicsTools/PFNano
scram b -j 4

cmsDriver.py --python_filename doubleeg_cfg.py --eventcontent NANOAOD --datatier NANOAOD \
   --fileout file:doubleeg_nanoaod.root --conditions 106X_dataRun2_v36 --step NANO \
   --filein $inputfile --era Run2_25ns,run2_nanoAOD_106X2015 --no_exec --data -n $nevents \
   --customise PhysicsTools/PFNano/pfnano_cff.PFnano_customizeData_onlyPF

cmsRun doubleeg_cfg.py

# Emulate creating root file
# cp data/doubleeg_nanoaod_eg.root output.root

if [ $runas = github ]; then
   cp *.root /mnt/vol/output.root
   echo ls -l /mnt/vol
   ls -l /mnt/vol
fi

if [ $runas = reana ]; then
   cp *.root output.root
   echo ls
   ls
fi