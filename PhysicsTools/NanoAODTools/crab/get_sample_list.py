import subprocess
import json
import glob 
import argparse

def get_das_info(query):
    '''Interface with das.py to get the query output.
    Could be done better, but this is time effective.
    Unfortunately the QL is more complicated than the 
    DBS one. '''
    
    das_command = [ 
        'dasgoclient',
        '--query=%s' % query,
        '--limit=0' 
        ]   
    p = subprocess.Popen(
        das_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        )   
    out, err = p.communicate()
    das_exitcode = p.wait()
    if das_exitcode != 0:
        #sometimes das sends the crash message to stdout
        raise RuntimeError('das.py crashed with error:\n%s' % err+out )
    return [str(i.strip(), 'utf-8') for i in out.split(b'\n') if i.strip()]

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Get the list of samples')
  parser.add_argument('-s', '--samples', type=str, default='mc,emb,data', help='what samples to look for; can be mc, emb, data, or a combination of them separated by comma')
  args = parser.parse_args()

  ############################################ MC #############################################
  if 'mc' in args.samples:
    campaigns = {'2016preVFP':'RunIISummer20UL16NanoAODAPVv9-*', '2016postVFP':'RunIISummer20UL16NanoAODv9-*', '2017':'RunIISummer20UL17NanoAODv9-*', '2018':'RunIISummer20UL18NanoAODv9-*'}
    missing_samples = {'2016preVFP':[], '2016postVFP':[], '2017':[], '2018':[]}
    
    with open("NanoAOD_MC.json", 'r') as f:
      MC_names = json.load(f)
    for year, campaign in campaigns.items():
      print("----------------------Checking MC samples DAG for year %s----------------------"%year)
      allsamples = {}
      for MC_shorthand, MC_name in MC_names.items():
        sample = get_das_info("dataset=/*%s*/%s/*"%(MC_name,campaign))
        if sample:
          allsamples[MC_shorthand]=list(sample)
          print("%s Found!!"%MC_name)
          if len(sample) > 1: 
            for subsample in sample:
              if any([_ in subsample for _ in ['PUFor', 'JMENano', 'Pilot', 'PU35For', 'bugFix']]):
                allsamples[MC_shorthand].remove(subsample) 
              elif 'ext' in subsample:
                allsamples.setdefault(MC_shorthand+'_ext',[]).append(subsample)
                allsamples[MC_shorthand].remove(subsample)
            if len(allsamples[MC_shorthand]) > 1:
              print("!!%s has duplicates!!Only using the first one!!"%MC_name)
              print(allsamples[MC_shorthand])
          allsamples[MC_shorthand] = get_das_info("dataset=%s"%(allsamples[MC_shorthand][0]))
        else:
          print("%s is Missing!!"%MC_name)
          missing_samples[year].append(MC_name)
      with open("NanoAODUL_%s_MC.json"%year, 'w') as f:
        json.dump(allsamples, f, indent=4, sort_keys=True)
    with open("MissingSamples.json", 'w') as f:
      json.dump(missing_samples, f, indent=4, sort_keys=True)
  
  ############################################ data #############################################
  if 'data' in args.samples:
    dataNames = ['SingleMuon', 'SingleElectron', 'EGamma', 'MuonEG']
    campaigns = {'2016':'Run2016*UL2016_MiniAODv2_NanoAODv9-v*', '2017':'Run2017*-UL2017_MiniAODv2_NanoAODv9-v*', '2018':'Run2018*-UL2018_MiniAODv2_NanoAODv9-*'}
    for year, campaign in campaigns.items():
      print("----------------------Checking DATA samples DAG for year %s----------------------"%year)
      allsamples = {}
      for dataname in dataNames:
        sample = get_das_info("dataset=/%s/%s/*"%(dataname,campaign))
        if sample:
          for run in sample:
            runName = run.split("/")[2].split("_")[0]
            subsample = dataname+'_'+runName
            if subsample in allsamples:
              print("!!%s has duplicates!!Only using the first one!!"%subsample)
              allsamples[subsample].append(run)
              print(allsamples[subsample])
            else:
              allsamples[subsample]=[run]
            allsamples[subsample] = get_das_info("dataset=%s"%(allsamples[subsample][0]))
            print("%s Found!!"%(subsample))
      if year=='2016':
        allsamplespostVFP,  allsamplespreVFP = {}, {}
        for shorthand2016, names2016 in allsamples.items():     
          if '2016F-UL' in shorthand2016 or '2016G-' in shorthand2016 or '2016H-' in shorthand2016:
            allsamplespostVFP[shorthand2016]= names2016
          else: 
            allsamplespreVFP[shorthand2016] = names2016
        with open("NanoAODUL_2016preVFP_data.json", 'w') as f:
          json.dump(allsamplespreVFP, f, indent=4, sort_keys=True)
        with open("NanoAODUL_2016postVFP_data.json", 'w') as f:
          json.dump(allsamplespostVFP, f, indent=4, sort_keys=True)
      else:
        with open("NanoAODUL_%s_data.json"%year, 'w') as f:
          json.dump(allsamples, f, indent=4, sort_keys=True)
    
