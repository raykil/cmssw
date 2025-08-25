"""
Usage: python3 crab_cfg.py NanoAODUL_2017_MC.json
Accessing CEPH: xrdfs root://hactar01.crc.nd.edu ls /store/user/jkil
"""

from CRABClient.UserUtilities import config
import sys
import json

config = config()
config.section_("General")
config.General.requestName = 'NanoPost'
config.General.transferLogs = True
config.General.workArea = '/afs/cern.ch/user/j/jkil/CMSSW_13_3_0/src/PhysicsTools/NanoAODTools/crab/workspace'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py', 'keep_and_drop_in.txt', 'keep_and_drop_out.txt']

config.section_("Data")
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/jkil/LFV/skims/20250728'
config.Data.publication = False
config.Data.outputDatasetTag = 'NanoTestPost'

config.section_("Site")
config.Site.storageSite = "T3_US_NotreDame"   # "T2_CH_CERN"

if __name__ == '__main__':
    from CRABAPI.RawCommand import crabCommand

    f = open(sys.argv[1]) 
    year = sys.argv[1].split('_')[1]
    isMC = 1 if 'MC' in sys.argv[1] else 0
    samples = json.load(f)
    print(f'isMC {isMC} year {year}')

    for sample_shorthand, sample in samples.items():
        print("Submitting Jobs for "+sample_shorthand)
        assert (len(sample) == 1), "Multiple VERs of samples are imported! Pick one!"
        config.Data.outLFNDirBase = f"/store/user/jkil/{year}" # must be in /store/user/<username> format for eos!
        config.Data.inputDataset = sample[0]
        config.General.requestName = sample_shorthand+'_'+year
        config.Data.outputDatasetTag = sample_shorthand
        config.JobType.scriptArgs = ['year=%s'%year]
        crabCommand('submit', config=config)