# NanoHEMSkim
This is a repository to produce skimmed NanoAOD files for X -> et/mt analysis. First, you need to setup a fresh CMSSW_13_3_0 and clone the PhysicsTools/NanoAODTools package in this branch. 

# Get sample/dataset paths
To produce json files of sample/dataset paths:
```bash
python3 get_sample_list.py
```
# Local run
To test locally before submitting to CRAB, uncomment and put your input files to the testFile list in ```crab_script.py``` and replae all ```inputFiles()``` to ```testFile```. Then do
```bash
python crab_script.py --year {which year}
```
# Submit CRAB jobs
Set up the CRAB env
```bash
source /cvmfs/cms.cern.ch/common/crab-setup.sh
```
Then create a dir for crab workspaces
```bash
mkdir workspace
```
and search for all occurance of ```kho2``` in ```crab_cfg.py``` and replace with your username or paths accordingly. To submit jobs, do, for example,
```bash
python crab_cfg.py NanoAODUL_2017_data.json 
```
## Monitoring
To monitor job status, go to ```https://monit-grafana.cern.ch```, look for "CMS Tasks Monitoring GlobalView" and type in your username and correct time range.

## Resubmit CRAB jobs
Jobs will fail! To resubmit failed CRAB jobs, do
```bash
python resubmit.py -f
```
which also creates a json file named ```finishedJobs.json``` that contains a list of the finished jobs. The option ```-f``` creates a new ```finishedJobs.json``` for a new patch of CRAB jobs. Omit ```-f``` if ```finishedJobs.json``` was already created for the patch of jobs.
