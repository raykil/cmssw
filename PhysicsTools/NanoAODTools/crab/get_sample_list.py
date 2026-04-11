import os, json, subprocess
from argparse import ArgumentParser

parser = ArgumentParser(prog='python3 get_sample_list.py', epilog="jkil@nd.edu", description='Get the list of samples from DAS.')
parser.add_argument('-y', '--year', default="2018", type=str, help='Options: 2016preVFP, 2016postVFP, 2017, 2018')
parser.add_argument('-t', '--type', default="data", type=str, help='Options: data, mc')
args = parser.parse_args()

MCMC_campaigns = {
    '2016preVFP' :'RunIISummer20UL16NanoAODAPVv9-*',
    '2016postVFP':'RunIISummer20UL16NanoAODv9-*',
    '2017'       :'RunIISummer20UL17NanoAODv9-*',
    '2018'       :'RunIISummer20UL18NanoAODv9-*'
}
DATA_campaigns = {
    '2016preVFP' :'Run2016*UL2016_MiniAODv2_NanoAODv9-v*',
    '2016postVFP':'Run2016*UL2016_MiniAODv2_NanoAODv9-v*', 
    '2017'       :'Run2017*-UL2017_MiniAODv2_NanoAODv9-v*',
    '2018'     :'Run2018*-UL2018_MiniAODv2_NanoAODv9-*'
}
dataNames = ['SingleMuon', 'SingleElectron', 'EGamma'] # 'MuonEG'

def getSamplesFromDAS(query):
    command = ['dasgoclient', f'--query={query}', '--limit=0']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    samples = [str(i.strip(), 'utf-8') for i in out.split(b'\n') if i.strip()]
    samples = [s for s in samples if not any(x in s for x in ['PUFor', 'JMENano', 'Pilot', 'PU35For', 'bugFix'])]
    return samples

if __name__=='__main__':
    SAMPLES = {}

    if args.type=='mc':
        with open("sample_json/NanoAOD_MC.json", 'r') as f: MC_names = json.load(f)
        for short, name in MC_names.items():
            query = f"dataset=/*{name}*/*{MCMC_campaigns[args.year]}*/*NANO*"
            samples = getSamplesFromDAS(query)
            for sample in samples:
                tag = '_ext' if 'ext' in sample else ''
                if args.year == '2018' and short+tag == 'TTTo2L2Nu_ext':
                    continue
                SAMPLES.update({short+tag: [sample]})

    elif args.type=='data':
        for name in dataNames:
            query = f"dataset=/*{name}*/*{DATA_campaigns[args.year]}*/*NANO*"
            samples = getSamplesFromDAS(query)
            if   args.year=='2016preVFP' : samples = [s for s in samples if 'HIPM' in s]
            elif args.year=='2016postVFP': samples = [s for s in samples if 'HIPM' not in s]
            for sample in samples:
                run_name = sample.split('/')[2].split('_')[0]
                SAMPLES.update({f"{name}_{run_name}": [sample]})
        
    os.makedirs('sample_json', exist_ok=True)
    json_name = f"sample_json/NanoAODUL_{args.year}_{args.type}.json"
    with open(json_name, 'w') as j:
        json.dump(SAMPLES, j, indent=4, sort_keys=True)
    print(f"{json_name} made!")