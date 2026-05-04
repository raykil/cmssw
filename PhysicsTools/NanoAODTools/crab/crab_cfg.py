"""
Usage: python3 crab_cfg.py NanoAODUL_2017_MC.json
Accessing CEPH: xrdfs root://hactar01.crc.nd.edu ls /store/user/jkil
"""

from CRABClient.UserUtilities import config
import sys, json, random, subprocess

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
config.Data.outLFNDirBase = '/store/user/jkil'  # overridden per-sample below
config.Data.publication = False
config.Data.outputDatasetTag = 'NanoTestPost'

config.section_("Site")
config.Site.storageSite = "T3_US_NotreDame"   # "T2_CH_CERN"

# ── branch preflight ──────────────────────────────────────────────────────────
REQUIRED_BRANCHES = {
    '2016': {
        'triggers': ['HLT_IsoMu24', 'HLT_Ele27_WPTight_Gsf', 'HLT_IsoTkMu24'],
        'flags'   : ['Flag_goodVertices', 'Flag_globalSuperTightHalo2016Filter',
                     'Flag_HBHENoiseFilter', 'Flag_HBHENoiseIsoFilter',
                     'Flag_EcalDeadCellTriggerPrimitiveFilter', 'Flag_BadPFMuonFilter',
                     'Flag_eeBadScFilter', 'Flag_BadPFMuonDzFilter'],
    },
    '2017': {
        'triggers': ['HLT_IsoMu27', 'HLT_Ele27_WPTight_Gsf', 'HLT_Ele32_WPTight_Gsf_L1DoubleEG'],
        'flags'   : ['Flag_goodVertices', 'Flag_globalSuperTightHalo2016Filter',
                     'Flag_HBHENoiseFilter', 'Flag_HBHENoiseIsoFilter',
                     'Flag_EcalDeadCellTriggerPrimitiveFilter', 'Flag_BadPFMuonFilter',
                     'Flag_eeBadScFilter', 'Flag_BadPFMuonDzFilter', 'Flag_ecalBadCalibFilter'],
    },
    '2018': {
        'triggers': ['HLT_IsoMu24', 'HLT_Ele27_WPTight_Gsf', 'HLT_Ele32_WPTight_Gsf_L1DoubleEG',
                     'HLT_Ele32_WPTight_Gsf'],
        'flags'   : ['Flag_goodVertices', 'Flag_globalSuperTightHalo2016Filter',
                     'Flag_HBHENoiseFilter', 'Flag_HBHENoiseIsoFilter',
                     'Flag_EcalDeadCellTriggerPrimitiveFilter', 'Flag_BadPFMuonFilter',
                     'Flag_eeBadScFilter', 'Flag_BadPFMuonDzFilter', 'Flag_ecalBadCalibFilter'],
    },
}
REDIRECTOR = 'root://cms-xrd-global.cern.ch/'
N_FILES_CHECK = 3

def _das_files(dataset):
    proc = subprocess.run(['dasgoclient', f'--query=file dataset={dataset}', '--limit=0'],
                          capture_output=True, text=True)
    return [l.strip() for l in proc.stdout.splitlines() if l.strip()]

def _branch_names(pfn):
    import uproot
    with uproot.open(pfn + ':Events') as tree:
        return set(tree.keys())

def preflight_branch_check(samples, year):
    base_year = '2016' if '2016' in year else year
    required = (REQUIRED_BRANCHES[base_year]['triggers'] +
                REQUIRED_BRANCHES[base_year]['flags'])
    problems = {}   # short -> {lfn -> [missing branches]}

    print(f"\nPreflight branch check ({year}, {len(required)} required branches) ...")
    for short, paths in samples.items():
        dataset  = paths[0]
        lfns     = _das_files(dataset)
        if not lfns:
            print(f"  [{short}] DAS returned no files — treating as failure")
            problems[short] = {'(no files from DAS)': required}
            continue

        chosen = random.sample(lfns, min(N_FILES_CHECK, len(lfns)))
        per_file = {}
        for lfn in chosen:
            try:
                branches = _branch_names(REDIRECTOR + lfn)
                missing  = [b for b in required if b not in branches]
                if missing:
                    per_file[lfn] = missing
            except Exception as e:
                per_file[lfn] = [f'(could not open file: {e})']
        if per_file:
            problems[short] = per_file

    if not problems:
        print("  All datasets OK.\n")
        return

    # ── report and abort ──────────────────────────────────────────────────────
    print("\n" + "="*70)
    print("PREFLIGHT FAILED — missing branches detected. No jobs submitted.")
    print("="*70)
    for short, per_file in problems.items():
        print(f"\n  Dataset: {short}")
        for lfn, missing in per_file.items():
            print(f"    File checked: {lfn}")
            for b in missing:
                kind = 'TRIGGER' if b.startswith('HLT') else 'FLAG'
                print(f"      [{kind}] {b}")
    print("="*70 + "\n")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    from CRABAPI.RawCommand import crabCommand

    f = open(sys.argv[1])
    year = sys.argv[1].split('_')[-2]
    isMC = 1 if 'MC' in sys.argv[1] or 'mc' in sys.argv[1] else 0
    samples = json.load(f)
    print(f'isMC {isMC} year {year}')

    if 'embd' in sys.argv[1]: config.Data.inputDBS = 'phys03'

    preflight_branch_check(samples, year)

    for sample_shorthand, sample in samples.items():
        print("Submitting Jobs for "+sample_shorthand)
        assert (len(sample) == 1), "Multiple VERs of samples are imported! Pick one!"
        config.Data.outLFNDirBase = f"/store/user/jkil/{year}" # must be in /store/user/<username> format for eos! ext files are located with original files dir.
        config.Data.inputDataset = sample[0]
        config.General.requestName = sample_shorthand+'_'+year
        config.Data.outputDatasetTag = sample_shorthand
        isEmbd = 1 if 'embd' in sys.argv[1] else 0
        config.JobType.scriptArgs = ['year=%s'%year, 'embd=%d'%isEmbd]
        crabCommand('submit', config=config)