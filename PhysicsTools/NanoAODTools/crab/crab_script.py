#!/usr/bin/env python3
import os, argparse
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.utils.crabhelper import inputFiles, runsAndLumis

parser = argparse.ArgumentParser("")
parser.add_argument('-jobNum', '--jobNum', type=str, default='1', help="")
parser.add_argument('-y', '--year', type=str, default='2018')
args = parser.parse_args()

looseElectron = "(Electron_pt > 10 && abs(Electron_eta) < 2.5 && !((abs(Electron_eta) < 1.566) && (abs(Electron_eta) > 1.442)) && Electron_mvaFall17V2noIso_WP90 && abs(Electron_dxy) < 0.5 && abs(Electron_dz) < 0.2)"
looseMuon = "(Muon_pt > 10 && abs(Muon_eta) < 2.4 && Muon_looseId && abs(Muon_dxy) < 0.5 && abs(Muon_dz) < 0.2)"
looseTau = "(Tau_pt > 30 && abs(Tau_eta) < 2.3 && Tau_idDeepTau2017v2p1VSjet >=8 && abs(Tau_dz) < 0.2)"

selections_em = "(Sum$(%s)>0 && Sum$(%s)>0)"%(looseElectron, looseMuon)
selections_etau = "(Sum$(%s)>0 && Sum$(%s)>0)"%(looseElectron, looseTau)
selections_mtau = "(Sum$(%s)>0 && Sum$(%s)>0)"%(looseMuon, looseTau)

Triggers = "(HLT_IsoMu24 | HLT_Ele27_WPTight_Gsf | HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL | HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ | HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL | HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ | HLT_Ele32_WPTight_Gsf_L1DoubleEG | HLT_Ele32_WPTight_Gsf)"
METFilters = "(Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_eeBadScFilter && Flag_BadPFMuonDzFilter)"

if '2016' in args.year:
  Triggers = Triggers.replace("HLT_Ele32_WPTight_Gsf_L1DoubleEG",  "HLT_Ele27_WPTight_Gsf | HLT_IsoTkMu24")
else:
  METFilters = METFilters.replace(")",  "&& Flag_ecalBadCalibFilter)")
if '2017' in args.year:
  Triggers = Triggers.replace("HLT_IsoMu24", "HLT_IsoMu27")
selections = "("+selections_em+"||"+selections_etau+"||"+selections_mtau+")&&"+METFilters+"&&(PV_npvsGood > 0)&&"+Triggers

testFile = ['root://cmsxrootd.fnal.gov//store/mc/RunIISummer20UL16NanoAODAPVv9/WW_TuneCP5_13TeV-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/280000/B81CEDFF-0ABA-7A48-84E3-C52B5DD8ECC6.root']

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
