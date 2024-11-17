import CRABClient
from CRABAPI.RawCommand import crabCommand
import json, glob, argparse, os
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fresh', action='store_true', help='Fresh patch of crab jobs')
args = parser.parse_args()

list_of_jobs = glob.glob('//afs/cern.ch/user/j/jkil/CMSSW_13_3_0/src/PhysicsTools/NanoAODTools/crab/workspace/*')

list_of_submit_fail_jobs = []
if args.fresh:
  list_of_finished_jobs = []
else:
  with open('finishedJobs.json') as f:
    list_of_finished_jobs = json.load(f)

for job in list_of_jobs:
  if job in list_of_finished_jobs:
    continue
  else:
    res = crabCommand('status', dir = job)
    #if res['status']=='COMPLETED':
      #list_of_finished_jobs.append(job)
    if res['dbStatus']=='SUBMITFAILED' or res['jobList'] == {}:
      list_of_submit_fail_jobs.append(job)
      input("Press any key to delete "+job)
      os.system("rm -rf "+job)
    elif any(['failed' in i for i in res['jobList']]):
      res = crabCommand('resubmit', dir = job)
#    elif all(['finished' in i for i in res['jobList']]):
#      list_of_finished_jobs.append(job)
with open('finishedJobs.json', 'w') as f: 
  json.dump(list_of_finished_jobs, f)
with open('unsubmittedJobs.json', 'a') as f: 
  f.write(str(list_of_submit_fail_jobs))
#  json.dump(list_of_submit_fail_jobs, f)

