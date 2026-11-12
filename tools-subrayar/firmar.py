# Rehace site/manifest.json (sha256 de cada archivo) y lo firma en site/manifest.sig (Ed25519).
# Uso: python3 tools-subrayar/firmar.py /ruta/clave-privada-firma.pem   (la clave NUNCA va al repo)
import os,sys,json,hashlib,time,subprocess
site=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site')
key=sys.argv[1]
files={}
for r,_,fs in os.walk(site):
    for f in fs:
        p=os.path.join(r,f);rel=os.path.relpath(p,site).replace(os.sep,'/')
        if rel in('manifest.json','manifest.sig','_headers'):continue
        files[rel]=hashlib.sha256(open(p,'rb').read()).hexdigest()
old=json.load(open(os.path.join(site,'manifest.json')))
man={'version':max(int(time.time()),old.get('version',0)+1),'files':files}
raw=json.dumps(man);open(os.path.join(site,'manifest.json'),'w').write(raw)
sig=subprocess.run(['node','-e',"const c=require('crypto'),fs=require('fs');process.stdout.write(c.sign(null,fs.readFileSync(process.argv[1]),fs.readFileSync(process.argv[2],'utf8')).toString('base64'))",os.path.join(site,'manifest.json'),key],check=True,capture_output=True,text=True).stdout
open(os.path.join(site,'manifest.sig'),'w').write(sig)
print('manifest',len(files),'archivos, versión',man['version'],'firmado')
