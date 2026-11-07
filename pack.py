import os,shutil,subprocess
os.chdir('dist')
SCRIPT='''#!/bin/bash
# Instala Medicina UDLAP en Aplicaciones y la deja lista para abrir.
cd "$(dirname "$0")"
APP="Medicina UDLAP.app"
echo "Instalando $APP en Aplicaciones..."
ditto "$APP" "/Applications/$APP" || { echo "No pude copiar a Aplicaciones"; exit 1; }
xattr -cr "/Applications/$APP"
codesign --force --deep --sign - "/Applications/$APP" >/dev/null 2>&1
echo "Listo. Abriendo Medicina UDLAP..."
open "/Applications/$APP"
'''
for a,label in [('arm64','Mac con chip Apple'),('x64','Mac con Intel')]:
    d='Medicina UDLAP (%s)'%label
    if not os.path.exists(d):
        os.mkdir(d)
        subprocess.run(['cp','-a','Medicina UDLAP-darwin-%s/Medicina UDLAP.app'%a,d+'/'],check=True)
    p=os.path.join(d,'Instalar Medicina UDLAP.command');open(p,'w').write(SCRIPT);os.chmod(p,0o755)
    z='Medicina-UDLAP-%s.zip'%('chip-Apple' if a=='arm64' else 'Intel')
    if not os.path.exists(z):
        subprocess.run(['zip','-qry',z,d],check=True)
    print(z,os.path.getsize(z)//1048576,'MB')
