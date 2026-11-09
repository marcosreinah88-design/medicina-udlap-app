# hub/ (lo publicado en el artefacto) -> site/ (fuentes locales + manifest.json) para Netlify y para la app
import os,sys,shutil,hashlib,json,subprocess,time
here=os.path.dirname(os.path.abspath(__file__));hub=os.path.join(here,'..','hub');site=os.path.join(here,'site')
if os.path.exists(site):shutil.rmtree(site)
shutil.copytree(hub,site,ignore=shutil.ignore_patterns('_test*'))
# sw.js y pwa.js (uso sin internet en el cel) viven en pwa/ de este repo y reemplazan los del hub
for f in ('sw.js','pwa.js'):shutil.copy(os.path.join(here,'pwa',f),os.path.join(site,f))
fonts_cache=os.path.join(here,'fonts_cache')
if os.path.exists(fonts_cache):shutil.copytree(fonts_cache,os.path.join(site,'fonts'),dirs_exist_ok=True)
subprocess.run([sys.executable,os.path.join(here,'fonts.py'),site],check=True)
shutil.copytree(os.path.join(site,'fonts'),fonts_cache,dirs_exist_ok=True)
files={}
for r,_,fs in os.walk(site):
    for f in fs:
        p=os.path.join(r,f);rel=os.path.relpath(p,site).replace(os.sep,'/')
        files[rel]=hashlib.sha256(open(p,'rb').read()).hexdigest()
man={'version':int(time.time()),'files':files}
json.dump(man,open(os.path.join(site,'manifest.json'),'w'))
open(os.path.join(site,'_headers'),'w').write('/manifest.json\n  Cache-Control: no-cache\n/sw.js\n  Cache-Control: no-cache\n')
print('site',len(files),'files, version',man['version'])
