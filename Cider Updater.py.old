import os, requests, json
from datetime import datetime

def updater():
    os.system('taskkill /f /im Cider.exe > nul 2>&1')
    print("[INFO] All Cider instances terminated.")
    
    working_dir = directory_manager()
    
    print("[INFO] Finding latest Cider release...")
    cider_link, exe_name = github_json()
    print("[INFO] Found latest Cider release.")
    
    print("[INFO] Downloading Cider installer...")
    cider_exe = requests.get(cider_link, stream=True)
    if cider_exe.status_code != 200:
        raise Exception(f"[ERROR] GitHub Asset Download returned status: {cider_exe.status_code}")
    
    with open(f'{working_dir}\{exe_name}', 'wb') as f:
        for chunk in cider_exe.iter_content(chunk_size=1024*8):
            if chunk:
                f.write(chunk)
        f.close()
    print("[INFO] Downloaded Cider installer.")
    
    print("[INFO] Launching Cider installer...")
    # os.system(f'{working_dir}\{exe_name} /S')
    os.system(f'powershell -command "Set-Location -Path \'{working_dir}\'; .\{exe_name}')
    
def github_json():
    response = requests.get("https://api.github.com/repos/ciderapp/cider-releases/releases?per_page=100")
    if response.status_code != 200:
        raise Exception(f"[ERROR] GitHub Releases API returned status: {response.status_code}")
       
    cider_json = response.json()
    
    working_dir = os.getcwd()
    with open(f'{working_dir}\Cider.json', 'w', encoding='utf-8') as f:
        json.dump(cider_json, f, ensure_ascii=False, indent=4)
        f.close()
        
    this_date = datetime.fromtimestamp(0)
    latest_date = datetime.fromtimestamp(0)
    latest_build = False
    for build in cider_json:
        if "(main)" in build['name']:
            this_date = datetime.fromisoformat(build['published_at'][:-1])
            if this_date >= latest_date: 
                latest_date = this_date
                latest_build = build['assets'][3]['browser_download_url']
                
    if latest_build == False:
        raise Exception("[ERROR] GitHub Releases API returned no valid releases")
        
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