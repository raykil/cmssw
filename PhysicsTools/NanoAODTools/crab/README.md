# NANOAOD Skims for LFV

This directory contains scripts that produce skimmed NanoAOD files for $X\rightarrow e\mu, e\tau, \mu\tau$ analysis. Input files are located in [CMS DAS](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookLocatingDataSamples#CliDas), and the output files are saved in [CEPH](https://crcresearch.github.io/ndcmsT3/resources/ndcms/#ceph-space). You need to setup a fresh CMSSW_13_3_0 and clone the PhysicsTools/NanoAODTools package in this branch.

### Step 0: Setup
0. If GRID certificate is not set up, follow the instructions in [WorkBookStartingGrid](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookStartingGrid).

1. Set up the CMSSW environment with the following commands:
```bash
voms-proxy-init --rfc --voms cms -valid 192:00
conda deactivate
cd ~/CMSSW_13_3_0/src
cmsenv
```
2. Then, set up the CRAB environment with the following commands:
```bash
cd PhysicsTools/NanoAODTools/crab
source /cvmfs/cms.cern.ch/common/crab-setup.sh
mkdir workspace
export CMSSW_BASE=/afs/cern.ch/user/$(whoami | cut -c1)/$(whoami)/CMSSW_13_3_0
cp -r ../python/postprocessing/ $CMSSW_BASE/python/PhysicsTools/NanoAODTools
```

### Step 1: Getting samples
Run the following command to produce json files of sample names for each year and type (data or mc):
```bash
python3 get_sample_list.py
```

### Step 2: Submitting jobs
Submit jobs via the following command:
``` bash
python3 crab_cfg.py {json name}     # Ex) python3 crab_cfg.py NanoAODUL_2017_MC.json
```

As of 2025.07.30, the results are stored in ceph `/store/user/jkil/LFV/skims/<yyyymmdd>/<sample_year>/`.
To access the ceph directories, use the following command:
```bash
xrdfs hactar01.crc.nd.edu ls /store/user/<username>
```

### Step 3: Monitoring
To monitor job status, visit [Grafana](https://monit-grafana.cern.ch/d/cmsTMGlobal/cms-tasks-monitoring-globalview?orgId=11) (https://monit-grafana.cern.ch > "CMS Tasks Monitoring GlobalView"). Type in the user name in "Select User" (upper left). Also adjust the timeframe accordingly (upper right).

### Step 4: Resubmitting jobs
Jobs will fail! To resubmit failed CRAB jobs, do
```bash
python3 resubmit.py -f
```