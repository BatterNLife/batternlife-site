import os,shutil,subprocess,sys
from build import build_site,PAGES,SITE
R=sys.argv[2] if len(sys.argv)>2 and not sys.argv[2].startswith('--') else '/home/claude/batternlife-site'
pages,files=build_site()
d=R+'/img'; os.makedirs(d,exist_ok=True)
for f in os.listdir(d): os.remove(os.path.join(d,f))
for k,f in files.items(): shutil.copy(f,os.path.join(d,k+'.webp'))
shutil.copy('og.jpg',d+'/og.jpg')
for name in ('story','bake','mom','favorites','orders','privacy','contact'): shutil.rmtree(R+'/'+name,ignore_errors=True)
for path,html in pages.items():
    p=R+path; os.makedirs(p,exist_ok=True); open(p+'index.html','w').write(html)
open(R+'/robots.txt','w').write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n"%SITE)
open(R+'/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>%s%s</loc></url>\n'%(SITE,v[0]) for v in PAGES.values())+'</urlset>\n')
if '--nopush' in sys.argv: sys.exit()
msg=sys.argv[1]+"\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01CXUxTZZBRhio4oJKXsYzKV"
run=lambda *a:subprocess.run(a,cwd=R,capture_output=True,text=True)
run('git','add','-A'); c=run('git','-c',"user.name=Batter N' Life",'-c','user.email=noreply@batternlife.com','commit','-qm',msg); print(c.stdout,c.stderr)
p=run('git','push','origin','main'); print(p.stdout[-300:],p.stderr[-300:])
