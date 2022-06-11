import re, os, requests, json

def updater():
    os.system('taskkill /f /im Cider.exe > nul 2>&1')
    print("[INFO] All Cider instances terminated.")
    
    working_dir = directory_manager()
    
    print("[INFO] Finding latest Cider release...")
    cider_link, exe_name = circleci_json()
    print("[INFO] Found latest Cider release.")
    
    print("[INFO] Downloading Cider installer...")
    cider_exe = requests.get(cider_link, stream=True)
    if cider_exe.status_code != 200:
        raise Exception(f"[ERROR] CircleCI Artifact Download returned status: {cider_exe.status_code}")
    
    with open(f'{working_dir}\{exe_name}', 'wb') as f:
        for chunk in cider_exe.iter_content(chunk_size=1024*8):
            if chunk:
                f.write(chunk)
        f.close()
    print("[INFO] Downloaded Cider installer.")
    
    print("[INFO] Launching Cider installer...")
    # os.system(f'{working_dir}\{exe_name} /S')
    os.system(f'powershell -command "Set-Location -Path \'{working_dir}\'; .\{exe_name}')

def circleci_json():
    pipelineListResponse = requests.get("https://circleci.com/api/v2/project/gh/ciderapp/Cider/pipeline?branch=main")
    if pipelineListResponse.status_code != 200:
        raise Exception(f"[ERROR] CircleCI Pipelines List API returned status: {pipelineListResponse.status_code}")
    
    pipelineID = pipelineListResponse.json()['items'][0]['id']
    
    workflowListResponse = requests.get(f"https://circleci.com/api/v2/pipeline/{pipelineID}/workflow")
    if workflowListResponse.status_code != 200:
        raise Exception(f"[ERROR] CircleCI Workflows List API returned status: {workflowListResponse.status_code}")
    
    workflowID = workflowListResponse.json()['items'][0]['id']
    
    jobListResponse = requests.get(f"https://circleci.com/api/v2/workflow/{workflowID}/job")
    if jobListResponse.status_code != 200:
        raise Exception(f"[ERROR] CircleCI Jobs List API returned status: {jobListResponse.status_code}")
    
    jobNumber = jobListResponse.json()['items'][-1]['job_number']
    
    artifactsListResponse = requests.get(f"https://circleci.com/api/v2/project/gh/ciderapp/Cider/{jobNumber}/artifacts")
    if jobListResponse.status_code != 200:
        raise Exception(f"[ERROR] CircleCI Artifacts List API returned status: {jobListResponse.status_code}")
    
    artifactsJSON = artifactsListResponse.json()
    
    working_dir = os.getcwd()
    with open(f'{working_dir}\Cider.json', 'w', encoding='utf-8') as f:
        json.dump(artifactsJSON, f, ensure_ascii=False, indent=4)
        f.close()
        
    latest_build = artifactsJSON['items'][3]['url']
    return latest_build, latest_build.split('/')[-1]

def directory_manager():
    working_dir = os.getcwd()
    os.system(f'rmdir "{working_dir}\Source" /S /Q')
    os.system(f'mkdir "{working_dir}\Source"')
    os.chdir(f'{working_dir}\Source')
    working_dir = os.getcwd()
    return working_dir

print("--- Cider Updater ---")
updater()