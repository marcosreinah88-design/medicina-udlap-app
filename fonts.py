import re,os,glob,hashlib,urllib.request,sys
root=sys.argv[1];fdir=os.path.join(root,'fonts');os.makedirs(fdir,exist_ok=True)
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=60).read()
cache={}
for f in glob.glob(root+'/**/*.html',recursive=True):
    t=open(f,encoding='utf-8').read()
    urls=set(re.findall(r'href="(https://fonts\.googleapis\.com/css2\?[^"]+)"',t))
    if not urls and 'fonts.g' not in t: continue
    for u in urls:
        if u not in cache:
            css=get(u.replace('&amp;','&')).decode()
            def rep(m):
                fu=m.group(1);name=hashlib.md5(fu.encode()).hexdigest()[:16]+'.woff2'
                p=os.path.join(fdir,name)
                if not os.path.exists(p):open(p,'wb').write(get(fu))
                return 'url(%s)'%name
            css=re.sub(r'url\((https://fonts\.gstatic\.com/[^)]+)\)',rep,css)
            cn='g'+hashlib.md5(u.encode()).hexdigest()[:10]+'.css'
            open(os.path.join(fdir,cn),'w').write(css);cache[u]=cn
        rel=os.path.relpath(os.path.join(fdir,cache[u]),os.path.dirname(f))
        t=t.replace('href="%s"'%u,'href="%s"'%rel)
    t=re.sub(r'<link rel="preconnect"[^>]*fonts\.(googleapis|gstatic)\.com[^>]*>\s*','',t)
    open(f,'w',encoding='utf-8').write(t)
print(len(cache),'css',len(os.listdir(fdir)))
