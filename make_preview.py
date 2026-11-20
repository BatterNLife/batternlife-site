"""Fast preview: writes pv/index.html with images as separate files in pv/img/
(publish pv/index.html as the artifact page with every pv/img/*.webp in `files`, root=pv).
The old single-file preview (build.py -> batter-n-life-boutique.html) embeds every photo and is ~15 MB."""
import os,shutil,re
src=open('build.py').read().split("if __name__")[0]; ns={}
exec(compile(src,'build.py','exec'),ns)
html,files=ns['build']('files')
os.makedirs('pv/img',exist_ok=True)
for k,f in files.items(): shutil.copy(f,'pv/img/'+k+'.webp')
open('pv/index.html','w').write(html)
print('preview html KB',len(html)//1024,'images',len(files))
