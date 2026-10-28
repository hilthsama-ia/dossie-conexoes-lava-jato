"""Build crawlable guides and metadata for the Hostinger deployment."""
import json, re
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parent.parent
D=json.loads((ROOT/'src/dados.json').read_text(encoding='utf-8'))
BASE='https://lavajatointerativa.com.br/'
TITLE='Lava Jato Interativa | Relações, provas e processos'
DESC='Explore o painel de relações da Lava Jato: Lula, Odebrecht, sítio de Atibaia, triplex e José Dirceu. Veja provas, decisões e documentos públicos.'
CASES=[('sitio-de-atibaia','Sítio','Sítio de Atibaia: provas, reformas e decisões',[2,6]),('triplex-do-guaruja','Triplex','Triplex do Guarujá: provas, penas e desfecho',[3,6]),('sistemas-odebrecht','Odebrecht','Drousys e MyWebDay B: sistemas e provas da Odebrecht',[4,5]),('jose-dirceu','Dirceu','José Dirceu: processos, penas e tempo preso',[7]),('instituto-lula','Instituto','Instituto Lula: acusações e decisões sobre as provas',[5])]

def meta(title,desc,path=''):
    url=BASE+path
    schema={'@context':'https://schema.org','@graph':[{'@type':'WebSite','@id':BASE+'#website','name':'Lava Jato Interativa','url':BASE,'inLanguage':'pt-BR'},{'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,'inLanguage':'pt-BR','isPartOf':{'@id':BASE+'#website'},'primaryImageOfPage':{'@type':'ImageObject','url':BASE+'assets/compartilhar.jpg','width':1200,'height':630}}]}
    return '\n'.join(['<!-- SEO START -->',f'<meta name="description" content="{escape(desc,quote=True)}">',f'<link rel="canonical" href="{url}">','<meta name="robots" content="index,follow,max-image-preview:large">','<meta name="theme-color" content="#0c121b">',f'<meta property="og:title" content="{escape(title,quote=True)}">',f'<meta property="og:description" content="{escape(desc,quote=True)}">',f'<meta property="og:url" content="{url}">','<meta property="og:type" content="website">','<meta property="og:locale" content="pt_BR">','<meta property="og:site_name" content="Lava Jato Interativa">',f'<meta property="og:image" content="{BASE}assets/compartilhar.jpg">','<meta property="og:image:width" content="1200">','<meta property="og:image:height" content="630">','<meta property="og:image:type" content="image/jpeg">','<meta property="og:image:alt" content="Painel real com fotografias, nomes e fios coloridos que conectam os personagens e empresas dos processos.">','<meta name="twitter:card" content="summary_large_image">',f'<meta name="twitter:title" content="{escape(title,quote=True)}">',f'<meta name="twitter:description" content="{escape(desc,quote=True)}">',f'<meta name="twitter:image" content="{BASE}assets/compartilhar.jpg">','<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('</','<\\/')+'</script>','<!-- SEO END -->'])

def refs(keys):
    return '<ul>'+''.join('<li><a target="_blank" rel="noopener noreferrer" href="'+escape(D['sources'][k]['url'],quote=True)+'">'+escape(D['sources'][k]['title'])+'</a> — '+escape(D['sources'][k]['kind'])+'</li>' for k in dict.fromkeys(keys))+'</ul>'

guide='<section class="section" id="guias"><div class="eyebrow">Lava Jato Interativa / Guias por processo</div><h2>Entenda cada caso e confira as fontes</h2><p>Leia as explicações por assunto ou explore o quadro para seguir as relações. Acusações, condenações históricas, anulações e absolvições têm identificação própria.</p><div class="seo-guides">'+''.join(f'<a href="{slug}/"><strong>{escape(title)}</strong><span>Abrir guia e documentos →</span></a>' for slug,case,title,chap in CASES)+'</div></section>'
guidecss='<style id="seo-guides-style">.seo-guides{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}.seo-guides a{background:#182b3e;border:1px solid #53677e;border-radius:9px;padding:20px;text-decoration:none;color:#f3d293}.seo-guides span{display:block;color:#bacddd;font-size:13px;margin-top:12px}</style>'
for p in [ROOT/'index.html',ROOT/'src/template.html']:
    s=p.read_text(encoding='utf-8')
    s=re.sub(r'<!-- SEO START -->.*?<!-- SEO END -->','',s,flags=re.S)
    s=re.sub(r'<style id="seo-guides-style">.*?</style>','',s,flags=re.S)
    s=re.sub(r'<title>.*?</title>','<title>'+TITLE+'</title>',s,count=1)
    s=s.replace('</head>',meta(TITLE,DESC)+guidecss+'</head>')
    if 'id="guias"' not in s:s=s.replace('<section class="section" id="mapa">',guide+'<section class="section" id="mapa">')
    s=s.replace('CONEXÕES / DOSSIÊ</div>','LAVA JATO / INTERATIVA</div>')
    p.write_text(s,encoding='utf-8')

css='body{margin:0;background:#0c121b;color:#ecf1f7;font:17px/1.8 system-ui,sans-serif}header,main,footer{max-width:900px;margin:auto;padding:25px}header{border-bottom:1px solid #35455b}a{color:#efc77c;text-underline-offset:4px}h1{font-size:clamp(30px,5vw,49px);line-height:1.15}h2{margin-top:45px;color:#f0d7a6}h3{margin-top:28px}small{color:#bac8d9}.intro{font-size:20px;color:#c7d6e5}.box{padding:22px;background:#1b2d40;border-left:4px solid #e7bd71;margin:25px 0}.ref li{margin:10px 0;font-size:14px;overflow-wrap:anywhere}.button{display:inline-block;padding:12px 20px;background:#e8c278;color:#16273a;text-decoration:none;border-radius:8px;font-weight:700}footer{border-top:1px solid #35455b;font-size:13px}nav{display:flex;gap:18px;flex-wrap:wrap}img{width:100%;height:auto;border-radius:12px}p,li{overflow-wrap:anywhere}'
for slug,case,title,chapters in CASES:
    c=D['cases'][case]
    intro={'Sítio':'Propriedade, uso do imóvel, reformas e decisões são etapas diferentes. Entenda o papel dos documentos e dos depoimentos no caso do sítio Santa Bárbara.','Triplex':'Veja como documentos, visitas, reformas e depoimentos foram interpretados no caso do triplex, as mudanças da pena e o desfecho do processo.','Odebrecht':'Saiba o que faziam Drousys e MyWebDay B, como dados eletrônicos viraram objeto de disputa e o que as decisões sobre sua utilização determinaram.','Dirceu':'Separe o mensalão dos processos Engevix e Apolo. Compare penas sucessivas, períodos de custódia, indulto, anulações e prescrição.','Instituto':'Entenda as diferenças entre terreno para sede, doações e a instituição, além das decisões relativas ao material probatório.'}[case]
    content=f'<p class="intro">{intro}</p><p><a class="button" href="../#mapa">Explorar o painel interativo →</a></p><div class="box"><strong>Processos e consulta</strong><p>{escape(c["number"])}</p><p>{escape(c["note"])}</p>{refs([c["portal"]])}</div>'
    for i in chapters:
        ch=D['chapters'][i]
        content+='<section><h2>'+escape(ch['title'].split('. ',1)[-1])+'</h2><p>'+escape(ch['lead'])+'</p>'+''.join('<h3>'+escape(t)+'</h3><p>'+escape(b)+'</p>' for t,b in ch['parts'])+'<div class="ref">'+refs(ch['sources'])+'</div></section>'
    content+='<section><h2>Examine as evidências deste caso</h2>'
    for e in D['evidence']:
        if e['case']!=case:continue
        content+='<article><h3>'+escape(e['id']+' · '+e['title'])+'</h3>'+''.join('<p><strong>'+label+':</strong> '+escape(e[key])+'</p>' for label,key in [('Material','content'),('Tese da acusação','claim'),('Limites e controvérsia','limit'),('Situação judicial','status')])+'<h4>'+escape(e['guide']['title'])+'</h4><p>'+escape(e['guide']['text'])+'</p><div class="ref">'+refs(e['sources'])+'</div></article>'
    content+='</section><section><h2>Documentos para conferir</h2><div class="ref">'+refs(c['documents']+c['rulings'])+'</div></section>'
    links='<nav>'+''.join(f'<a href="../{s}/">{escape(k)}</a>' for s,k,t,ch in CASES)+'</nav>'
    out=f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | Lava Jato Interativa</title>'+meta(title+' | Lava Jato Interativa',intro,slug+'/')+f'<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml"><style>{css}</style></head><body><header><a href="../">LAVA JATO / INTERATIVA</a></header><main><small><a href="../">Início</a> / {escape(case)}</small><h1>{escape(title)}</h1>'+content+f'<section><h2>Continue explorando</h2>{links}<p><a href="../dossie-completo.pdf">Ler o dossiê completo em PDF</a></p></section></main><footer>Dossiê documental independente. Pesquisa de 28/10/2026. Inclui material invalidado com identificação do status; conexões não transferem responsabilidade criminal. Confira os andamentos posteriores nos portais oficiais.</footer></body></html>'
    folder=ROOT/slug;folder.mkdir(exist_ok=True);(folder/'index.html').write_text(out,encoding='utf-8')

(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /src/\n\nSitemap: '+BASE+'sitemap.xml\n',encoding='utf-8')
paths=['']+[s+'/' for s,c,t,ch in CASES]
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('<url><loc>'+BASE+p+'</loc><lastmod>2026-10-28</lastmod></url>\n' for p in paths)+'</urlset>',encoding='utf-8')
(ROOT/'assets').mkdir(exist_ok=True)
(ROOT/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#142334"/><path d="M16 18L48 24L28 48Z" fill="none" stroke="#efc875" stroke-width="3"/><circle cx="16" cy="18" r="6" fill="#66b4ff"/><circle cx="48" cy="24" r="6" fill="#efc875"/><circle cx="28" cy="48" r="6" fill="#ff798a"/></svg>',encoding='utf-8')
for p in [ROOT/'index.html',ROOT/'src/template.html']:
    s=p.read_text(encoding='utf-8')
    if 'rel="icon"' not in s:s=s.replace('</head>','<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"></head>')
    p.write_text(s,encoding='utf-8')
print('SEO: 6 páginas, metadados sociais, canonical, dados estruturados, sitemap e robots.')
