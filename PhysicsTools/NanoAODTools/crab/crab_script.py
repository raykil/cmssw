#!/usr/bin/env python3
import os, argparse, sys
#sys.path.insert(0, "/afs/crc.nd.edu/user/j/jkil/runiii-higgs-lfv/CMSSW_13_3_0/src")
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.utils.crabhelper import inputFiles, runsAndLumis

parser = argparse.ArgumentParser("")
parser.add_argument('-jobNum', '--jobNum', type=str, default='1', help="")
parser.add_argument('-y', '--year', type=str, default='2018')
parser.add_argument('-t', '--test', type=str, default='')
args = parser.parse_args()

looseElectron = "(Electron_pt > 10 && abs(Electron_eta) < 2.5 && !((abs(Electron_eta) < 1.566) && (abs(Electron_eta) > 1.442)) && Electron_mvaFall17V2noIso_WP90 && abs(Electron_dxy) < 0.5 && abs(Electron_dz) < 0.2)"
looseMuon = "(Muon_pt > 10 && abs(Muon_eta) < 2.4 && Muon_looseId && abs(Muon_dxy) < 0.5 && abs(Muon_dz) < 0.2)"
looseTau = "(Tau_pt > 30 && abs(Tau_eta) < 2.3 && Tau_idDeepTau2017v2p1VSjet >=8 && abs(Tau_dz) < 0.2)"

selections_em = "(Sum$(%s)>0 && Sum$(%s)>0)"%(looseElectron, looseMuon)
selections_etau = "(Sum$(%s)>0 && Sum$(%s)>0)"%(looseElectron, looseTau)
selections_mtau = "(Sum$(%s)>0 && Sum$(%s)>0)"%(looseMuon, looseTau)

if '2016' in args.year:
  Triggers = "(HLT_IsoMu24 | HLT_Ele27_WPTight_Gsf | HLT_Ele27_WPTight_Gsf | HLT_IsoTkMu24 | HLT_Ele32_WPTight_Gsf)"
  METFilters = "(Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_eeBadScFilter && Flag_BadPFMuonDzFilter)"
elif '2017' in args.year:
  Triggers = "(HLT_IsoMu27 | HLT_Ele27_WPTight_Gsf | HLT_Ele32_WPTight_Gsf_L1DoubleEG | HLT_Ele32_WPTight_Gsf)"
  METFilters = "(Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_eeBadScFilter && Flag_BadPFMuonDzFilter && Flag_ecalBadCalibFilter)"
elif '2018' in args.year:
  Triggers = "(HLT_IsoMu24 | HLT_Ele27_WPTight_Gsf | HLT_Ele32_WPTight_Gsf_L1DoubleEG | HLT_Ele32_WPTight_Gsf)"
  METFilters = "(Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_eeBadScFilter && Flag_BadPFMuonDzFilter && Flag_ecalBadCalibFilter)"

selections = "("+selections_em+"||"+selections_etau+"||"+selections_mtau+")&&"+METFilters+"&&(PV_npvsGood > 0)&&"+Triggers

testFile = ['root://cmsxrootd.fnal.gov/'+args.test]

print("RUNNING")
p = PostProcessor(".",
#              testFile,
              inputFiles(),
              selections,
              branchsel="keep_and_drop_in.txt",
              outputbranchsel="keep_and_drop_out.txt",
              modules=[],
              provenance=True,
#              maxEntries=100, #just read the first maxEntries events
              fwkJobReport=True,
              jsonInput=runsAndLumis()
              )

p.run()
print("DONE")

