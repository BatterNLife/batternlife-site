"""Shared build: makes WebP images, adds lazy/size/priority attributes, async fonts.
mode='embed' -> single-file artifact (base64); mode='files' -> img/ paths for the live site."""
import re,os,base64
from PIL import Image
IMG='img'; OUT='webp'; os.makedirs(OUT,exist_ok=True)
def src_path(k): return os.path.join(IMG,k+('.png' if k.startswith('logo') else '.jpg'))
def make_webp(k,w=None,suffix=''):
    dst=os.path.join(OUT,k+suffix+'.webp'); src=src_path(k)
    if os.path.exists(dst) and os.path.getmtime(dst)>=os.path.getmtime(src): return dst
    im=Image.open(src); alpha=im.mode in('RGBA','LA','P') and k.startswith('logo')
    im=im.convert('RGBA' if alpha else 'RGB')
    if w and im.width>w: im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    if k=='logo_doodle2': im.save(dst,'WEBP',lossless=True,method=6)
    elif alpha: im.save(dst,'WEBP',quality=90,method=6)
    else: im.save(dst,'WEBP',quality=74,method=6)
    return dst
MAXW={'kitchen2':1400}
def build(mode):
    s=open('boutique.src.html').read()
    keys=sorted(set(re.findall(r'@@(\w+)@@',s)))
    files={k:make_webp(k,MAXW.get(k,900)) for k in keys}
    small=make_webp('kitchen2',760,'-760')
    dims={k:Image.open(f).size for k,f in files.items()}
    # fonts: non-blocking
    s=re.sub(r'<link href="(https://fonts\.googleapis\.com/css2[^"]+)" rel="stylesheet">',
             r'<link rel="preload" as="style" href="\1" onload="this.onload=null;this.rel=\'stylesheet\'"><noscript><link rel="stylesheet" href="\1"></noscript>',s,1)
    # base rule so width/height attrs never distort
    s=s.replace('<style>','<style>\nimg{height:auto}',1)
    def fix(m):
        tag=m.group(0); k=re.search(r'@@(\w+)@@',tag).group(1)
        if ' width=' not in tag:
            w,h=dims[k]; tag=tag.replace('<img ','<img width="%d" height="%d" '%(w,h),1)
        if k=='kitchen2':
            tag=tag.replace('<img ','<img fetchpriority="high" decoding="async" srcset="@@kitchen2_760@@ 760w, @@kitchen2@@ 1400w" sizes="(max-width:960px) 100vw, 52vw" ',1)
        elif k.startswith('logo_letters_flat'): pass
        elif 'loading=' not in tag: tag=tag.replace('<img ','<img loading="lazy" decoding="async" ',1)
        return tag
    s=re.sub(r'<img [^>]*src="@@\w+@@"[^>]*>',fix,s)
    files['kitchen2_760']=small
    if mode=='files':
        pre='<link rel="preload" as="image" href="img/kitchen2.webp" imagesrcset="img/kitchen2_760.webp 760w, img/kitchen2.webp 1400w" imagesizes="(max-width:960px) 100vw, 52vw" fetchpriority="high">'
        s=s.replace('<link rel="preconnect"',pre+'\n<link rel="preconnect"',1)
        return re.sub(r'@@(\w+)@@',lambda m:'img/'+m.group(1)+'.webp',s), files
    return re.sub(r'@@(\w+)@@',lambda m:'data:image/webp;base64,'+base64.b64encode(open(files[m.group(1)],'rb').read()).decode(),s), files
if __name__=='__main__':
    out,_=build('embed'); open('batter-n-life-boutique.html','w').write(out); print('artifact MB',round(len(out)/1e6,2))

# ================= SEO + real page addresses (live site only) =================
import json
SITE='https://batternlife.com'
TITLE_MAIN="Batter N' Life | Where Buttercream Meets Motherhood"
DESC_MAIN="Cakes, kids and everything in between. Custom cake orders, baking tips and real life as a mom of four."
PAGES={
 'home':('/',TITLE_MAIN,DESC_MAIN),
 'story':('/story/',"My Story | Batter N' Life","Meet Melinda: a wife, mom of four and self-taught baker who has created 600+ custom cakes over 10+ years."),
 'bake':('/bake/',"Custom Cakes in North Dallas | Bake Life | Batter N' Life","Custom celebration cakes made to order in the North Dallas area, for birthdays, weddings, showers and more. Browse my cake gallery and baking tips, then submit a dessert order."),
 'mom':('/mom/',"Mom Life | Batter N' Life","Family routines, everyday mom life and the real, sweet, messy moments of life with four kids."),
 'favorites':('/favorites/',"Shop My Favorites | Batter N' Life","The baking tools, kids' gear, home and beauty favorites I actually use and love."),
 'orders':('/orders/',"Cake Menu & Custom Cake Orders in North Dallas | Batter N' Life","Custom cake flavors, buttercreams and specialty fillings, from Brown Butter Vanilla to Bizcocho Mojadito. Serving the North Dallas area. See the menu and start your order."),
 'privacy':('/privacy/',"Privacy Policy | Batter N' Life","How Batter N' Life collects, uses, and protects the information you share through the website."),
 'contact':('/contact/',"Contact & Collaborations | Batter N' Life","Reach out about brand collaborations, partnerships, or just to say hi."),
}
SCHEMA={"@context":"https://schema.org","@graph":[
 {"@type":"WebSite","name":"Batter N' Life","url":SITE+"/","description":DESC_MAIN},
 {"@type":"Organization","name":"Batter N' Life","url":SITE+"/","logo":SITE+"/img/logo_letters_flat.webp","image":SITE+"/img/og.jpg",
  "description":"A baking and motherhood lifestyle brand: custom celebration cakes, baking tips, family life and favorite finds.",
  "email":"batternlife@gmail.com","founder":{"@type":"Person","name":"Melinda","jobTitle":"Baker, cake decorator and content creator"},
  "knowsAbout":["Custom cakes","Cake decorating","Baking tips","Motherhood","Family life"],
  "areaServed":{"@type":"Place","name":"North Dallas, Texas"},"makesOffer":{"@type":"Offer","areaServed":{"@type":"Place","name":"North Dallas, Texas"},"itemOffered":{"@type":"Service","serviceType":"Custom cakes","name":"Custom celebration cakes and desserts"}},
  "sameAs":["https://www.instagram.com/batternlife","https://www.youtube.com/@batternlife","https://www.tiktok.com/@batternlife","https://www.facebook.com/batternlife"]}]}
ROUTER_OLD_START="(function(){\n  var pages=document.querySelectorAll('main[data-page]'),tabs=document.querySelectorAll('header.bar nav a');"
PATH_ROUTER=r'''(function(){
  var pages=document.querySelectorAll('main[data-page]'),tabs=document.querySelectorAll('header.bar nav a');
  function cur(){var p=location.pathname.replace(/^\/+|\/+$/g,'');return p||'home'}
  window.bnlRoute=cur;
  window.bnlGo=function(href){if(href!==location.pathname)history.pushState(null,'',href);route();dispatchEvent(new Event('bnl:route'))};
  var META=__META__;
  function route(){
    var name=cur();if(!document.querySelector('main[data-page="'+name+'"]'))name='home';
    pages.forEach(function(m){m.hidden=m.getAttribute('data-page')!==name});document.documentElement.setAttribute('data-route',name);
    tabs.forEach(function(a){var t=a.getAttribute('href').replace(/\//g,'')||'home';if(t===name)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});
    var m=META[name];if(m){document.title=m[0];var d=document.querySelector('meta[name=description]');if(d)d.content=m[1];var c=document.querySelector('link[rel=canonical]');if(c)c.href=m[2]}
    window.scrollTo(0,0);
  }
  if(location.hash.indexOf('#/')===0){var o=location.hash.slice(2);history.replaceState(null,'',o?'/'+o+'/':'/')}
  document.addEventListener('click',function(e){var a=e.target.closest('a[href^="/"]');if(!a||e.defaultPrevented||e.metaKey||e.ctrlKey||e.shiftKey||a.target==='_blank')return;e.preventDefault();window.bnlGo(a.getAttribute('href'))});
  addEventListener('popstate',function(){route();dispatchEvent(new Event('bnl:route'))});route();
})();
(function(){'''
def seo_head(name):
    path,t,d=PAGES[name]; url=SITE+path
    return f'''<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Batter N' Life">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F1E7D8">
<script type="application/ld+json">{json.dumps(SCHEMA)}</script>'''
def build_site():
    html,files=build('files')
    html=html.replace('src="img/','src="/img/').replace('href="img/','href="/img/').replace(', img/',', /img/').replace('"img/','"/img/').replace("url(\"img/","url(\"/img/").replace('imagesrcset="img/','imagesrcset="/img/')
    html=re.sub(r'href="#/(\w*)"',lambda m:'href="/%s"'%(m.group(1)+'/' if m.group(1) else ''),html)
    i=html.index(ROUTER_OLD_START); j=html.index("window.addEventListener('hashchange',route);route();",i); j=html.index('})();',j)+len('})();')
    meta={k:[v[1],v[2],SITE+v[0]] for k,v in PAGES.items()}
    html=html[:i]+PATH_ROUTER.replace('__META__',json.dumps(meta))+"document.querySelector('header.bar .logo').setAttribute('href','/');})();"+html[j:]
    html=html.replace("document.querySelectorAll('a.logo,a[href=\"#/\"]')","document.querySelectorAll('a.logo,a[href=\"/\"]')")
    html=re.sub(r"\{var h=location\.hash;if\(h===''\|\|h==='#'\|\|h==='#/'\|\|h==='#/home'\)\{e\.preventDefault\(\);window\.scrollTo\(\{top:0,behavior:'smooth'\}\)\}else\{e\.preventDefault\(\);location\.hash='#/'\}\}",
        "{e.preventDefault();if(window.bnlRoute()==='home')window.scrollTo({top:0,behavior:'smooth'});else window.bnlGo('/')}",html)
    html=html.replace("addEventListener('hashchange',function(){if(location.hash.indexOf('#/contact')===0){","addEventListener('bnl:route',function(){if(window.bnlRoute()==='contact'){")
    assert 'location.hash' not in html.replace("location.hash.indexOf('#/')===0){var o=location.hash","")
    html=re.sub(r'<title>[^<]*</title>','',html,1)
    html=html.replace('</style>','.lsw{display:none!important} /* lsw-hide: preview-only switcher */\n</style>',1)
    out={}
    for name in PAGES:
        h=html.replace('<meta name="viewport"',seo_head(name)+'\n<meta name="viewport"',1)
        if name!='home': h=h.replace('<link rel="preload" as="image" href="/img/kitchen2.webp"','<link rel="prefetch" as="image" href="/img/kitchen2.webp"',1)
        out[PAGES[name][0]]=h
    return out,files
