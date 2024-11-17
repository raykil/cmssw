#from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config#, getUsernameFromSiteDB
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
#config.Data.inputDataset = '/GluGlu_LFV_HToEMu_M125_TuneCP5_13TeV_PSweights_powheg_pythia8/RunIISummer20UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
#config.Data.splitting = 'LumiBased'
#config.Data.unitsPerJob = 250
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
#config.Data.splitting = 'EventAwareLumiBased'
#config.Data.totalUnits = 10

config.Data.outLFNDirBase = '/store/user/jkil/NanoPost_'
#config.Data.outLFNDirBase = '/store/user/%s/NanoPost' % (
#    getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'NanoTestPost'
config.section_("Site")
#config.Site.storageSite = "T2_US_Wisconsin"
config.Site.storageSite = "T3_US_NotreDame"

#config.Site.storageSite = "T2_CH_CERN"
# config.section_("User")
#config.User.voGroup = 'dcms'

if __name__ == '__main__':
    f=open(sys.argv[1]) 
    year = sys.argv[1].split('_')[1]
    isMC = 1 if 'MC' in sys.argv[1] else 0
    samples = json.load(f)
    print(f'isMC {isMC} year {year}')
    from CRABAPI.RawCommand import crabCommand
#    if not isMC:
#      config.Data.splitting = 'LumiBased'
#      config.Data.unitsPerJob = 250
#      if '2016' in year:
#        config.Data.lumiMask = 'Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
#      elif year=='2017':
#        config.Data.lumiMask = 'Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'
#      elif year=='2018':
#        config.Data.lumiMask = 'Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
#      config.JobType.inputFiles.append(config.Data.lumiMask)
    for sample_shorthand, sample in samples.items():
        print("Submitting Jobs for "+sample_shorthand)
        assert (len(sample) == 1), "Multiple VERs of samples are imported! Pick one!"
        config.Data.outLFNDirBase = '/store/user/jkil/NanoPost_'+year+'_v9'
        config.Data.inputDataset = sample[0]
        config.General.requestName = sample_shorthand+'_'+year
        config.Data.outputDatasetTag = sample_shorthand
        config.JobType.scriptArgs = ['year=%s'%year]
        crabCommand('submit', config=config)#, dryrun=True)

