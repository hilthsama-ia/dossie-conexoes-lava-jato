import base64, io, json, mimetypes, re, sys
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image, ImageOps
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, A2
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader, PdfWriter

ROOT=Path(__file__).parent
D=json.loads((ROOT/'dados.json').read_text(encoding='utf-8'))
assets={}
manifest=ROOT/'assets/manifest.json'
if manifest.exists():
 raw=json.loads(manifest.read_text(encoding='utf-8-sig'))
 items=raw.get('assets',raw) if isinstance(raw,dict) else raw
 if isinstance(items,dict): items=[dict(v,id=k) for k,v in items.items() if isinstance(v,dict)]
 aliases={'jose_dirceu':'dirceu','jose-dirceu':'dirceu','marcelo_odebrecht':'marcelo','marcelo-odebrecht':'marcelo','leo_pinheiro':'leo','leo-pinheiro':'leo','emilio_odebrecht':'emilio','emilio-odebrecht':'emilio','antonio_palocci':'palocci','antonio-palocci':'palocci','fernando_bittar':'bittar','fernando-bittar':'bittar','jonas_suassuna':'jonas','jonas-suassuna':'jonas','jose_carlos_bumlai':'bumlai','jose-carlos-bumlai':'bumlai','milton_pascowitch':'milton','milton-pascowitch':'milton','odebrecht_logo':'odebrecht','logo_odebrecht':'odebrecht','logo-oas':'oas','oas_logo':'oas','logo_oas':'oas','petrobras_logo':'petrobras','logo_petrobras':'petrobras','pt_logo':'pt','logo_pt':'pt','instituto_lula':'instituto','instituto-lula':'instituto','engevix_logo':'engevix','logo_engevix':'engevix','sitio_atibaia':'sitio','sitio-atibaia':'sitio','triplex_guaruja':'triplex','triplex-guaruja':'triplex'}
 for item in items:
  fname=item.get('filename') or item.get('file') or item.get('path')
  if not fname: continue
  p=Path(fname)
  if not p.is_absolute():
   p=ROOT/'assets'/p
   if not p.exists(): p=ROOT/fname
  if not p.exists(): continue
  id=aliases.get(item['id'],item['id'])
  try:
   im=Image.open(p); im.thumbnail((900,900));b=io.BytesIO()
   if im.mode in ('RGBA','LA'):
    im.save(b,format='PNG');mime='image/png'
   else:im.convert('RGB').save(b,format='JPEG',quality=88);mime='image/jpeg'
   item=dict(item);item['data']='data:'+mime+';base64,'+base64.b64encode(b.getvalue()).decode();item['local']=str(p);item['alt']=item.get('alt') or item.get('name') or item['id'].replace('_',' ');item['source']=item.get('source') or item.get('source_url') or item.get('url') or '';assets[id]=item
  except Exception as exc: print('Asset ignorado:',p,exc)
D['assets']=assets
public_data=dict(D)
public_data['assets']={k:{a:b for a,b in v.items() if a!='local'} for k,v in assets.items()}
payload=json.dumps(public_data,ensure_ascii=False).replace('</','<\\/')
html=(ROOT/'template.html').read_text(encoding='utf-8').replace('__DATA__',payload)
if (ROOT/'enhance.html').exists():html=html.replace('</body>',(ROOT/'enhance.html').read_text(encoding='utf-8')+'</body>')
if (ROOT/'drilldown.html').exists():html=html.replace('</body>',(ROOT/'drilldown.html').read_text(encoding='utf-8')+'</body>')
(ROOT/'index.html').write_text(html,encoding='utf-8')

pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold','C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial',boldItalic='Arial-Bold')
INK=colors.HexColor('#172b40');GOLD=colors.HexColor('#b47d26');MUTED=colors.HexColor('#4e6072')
COL={'politica':'#2789d4','financeiro':'#16a77d','obra':'#d58122','depoimento':'#9563cc','acusacao':'#d64862','uso':'#2babb7'}
LABEL={'politica':'Cargo / vínculo político ou pessoal','financeiro':'Contrato / fluxo financeiro examinado','obra':'Obras / fornecimento','depoimento':'Declaração de depoente','acusacao':'Hipótese acusatória','uso':'Propriedade / utilização'}
N={n['id']:n for n in D['nodes']}

def drawmap(c,left,bottom,w,h):
 scale=min(w/1600,h/1380)
 c.saveState();c.translate(left,bottom+h);c.scale(scale,-scale)
 # Coordinates match the interactive map, while text is unflipped individually.
 def txt(x,y,t,size=13,bold=False,col=INK):
  c.saveState();c.translate(x,y);c.scale(1,-1);c.setFillColor(col);c.setFont('Arial-Bold' if bold else 'Arial',size);c.drawString(0,0,t);c.restoreState()
 for i,e in enumerate(D['edges']):
  a=N[e['a']];b=N[e['b']];x1=a['x']+85;y1=a['y']+80;x2=b['x']+85;y2=b['y']+80
  c.setStrokeColor(colors.HexColor(COL[e['kind']]));c.setLineWidth(3)
  c.setDash([9,7] if e['status']=='invalidada' else [])
  c.line(x1,y1,x2,y2)
  mx=(x1+x2)/2;my=(y1+y2)/2
  c.setFillColor(colors.white);c.rect(mx-2,my-12,30,18,fill=1,stroke=0)
  txt(mx,my+1,e['id'],11,True,colors.HexColor(COL[e['kind']]))
 c.setDash([])
 for n in D['nodes']:
  x,y=n['x'],n['y'];c.setFillColor(colors.HexColor('#f7f3e9'));c.setStrokeColor(colors.HexColor('#aab4bf'));c.setLineWidth(.8);c.roundRect(x,y,170,160,3,fill=1,stroke=1)
  a=assets.get(n['asset'])
  if a:
   im=Image.open(a['local']).convert('RGB')
   if n['group']=='empresa':im=ImageOps.pad(im,(462,294),color='white')
   else:im=ImageOps.fit(im,(462,294),centering=(.5,.3))
   c.saveState();c.translate(x+8,y+105);c.scale(1,-1);c.drawImage(ImageReader(im),0,0,width=154,height=98);c.restoreState()
  else:
   c.setFillColor(colors.HexColor('#d6e3eb'));c.rect(x+8,y+7,154,98,fill=1,stroke=0);txt(x+25,y+65,'DOCUMENTO' if n['group']=='documento' else 'SEM FOTO',16,True)
  size=15
  while pdfmetrics.stringWidth(n['name'],'Arial-Bold',size)>155: size-=.5
  txt(x+8,y+127,n['name'],size,True)
  role=n['role'];size=9
  while pdfmetrics.stringWidth(role,'Arial',size)>155:size-=.3
  txt(x+8,y+145,role,size,col=MUTED)
  c.setFillColor(colors.HexColor('#d94351'));c.circle(x+85,y,5,fill=1,stroke=0)
  if n['id']=='sistemas':
   c.setStrokeColor(colors.HexColor('#b12b40'));c.setLineWidth(2);c.rect(x+4,y+72,162,27,fill=0,stroke=1);txt(x+10,y+91,'PROVA INVALIDADA',12,True,colors.HexColor('#b12b40'))
 c.restoreState()

pw,ph=A2
c=canvas.Canvas(str(ROOT/'quadro-relacoes.pdf'),pagesize=A2)
c.setTitle('Quadro de relações — Lula, empreiteiras e processos');c.setAuthor('Dossiê documental')
c.setFillColor(INK);c.rect(0,ph-165,pw,165,fill=1,stroke=0)
c.setFillColor(colors.HexColor('#f1c775'));c.setFont('Arial-Bold',15);c.drawString(45,ph-45,'CONEXÕES / QUADRO DOCUMENTAL')
c.setFillColor(colors.white);c.setFont('Arial-Bold',30);c.drawString(45,ph-90,'Lula, empreiteiras e os processos')
c.setFont('Arial',12);c.drawString(45,ph-121,'Cores indicam a natureza da relação. A proximidade no quadro não demonstra culpa.')
c.drawString(45,ph-142,'Linhas tracejadas: dados invalidados. IDs R01–R29: explicações e fontes no dossiê completo.')
drawmap(c,35,270,pw-70,ph-455)
for i,(k,v) in enumerate(LABEL.items()):
 x=45+(i%2)*(pw/2);y=210-(i//2)*32;c.setStrokeColor(colors.HexColor(COL[k]));c.setLineWidth(3);c.line(x,y,x+30,y);c.setFont('Arial',12);c.setFillColor(INK);c.drawString(x+42,y-4,v)
c.setFont('Arial',10);c.drawString(45,70,'Recorte: sítio, triplex, Odebrecht, Instituto Lula e José Dirceu. Inclui acusações e condenações anuladas.')
c.drawString(45,51,'Pesquisa em 28/10/2026. Fontes e créditos fotográficos constam do dossiê completo e do HTML.');c.save()

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyX',fontName='Arial',fontSize=10.5,leading=16,textColor=INK,spaceAfter=10))
styles.add(ParagraphStyle(name='SmallX',fontName='Arial',fontSize=8,leading=11,textColor=MUTED,spaceAfter=9,wordWrap='CJK'))
styles.add(ParagraphStyle(name='H1X',fontName='Arial-Bold',fontSize=22,leading=27,textColor=INK,spaceBefore=12,spaceAfter=16,keepWithNext=True))
styles.add(ParagraphStyle(name='H2X',fontName='Arial-Bold',fontSize=13,leading=17,textColor=INK,spaceBefore=15,spaceAfter=8,keepWithNext=True))
styles.add(ParagraphStyle(name='LeadX',fontName='Arial',fontSize=12,leading=18,textColor=GOLD,spaceAfter=16))
source_ids=list(D['sources'])
def P(t,style='BodyX'):return Paragraph(escape(str(t)),styles[style])
def refp(ids):
 return P('Fontes: '+', '.join('F%02d'%(source_ids.index(x)+1) for x in ids),'SmallX')
flow=[]
flow+=[Spacer(1,75),P('CONEXÕES / DOSSIÊ DOCUMENTAL','LeadX'),P('Lula, empreiteiras e os processos','H1X'),P('As relações, as evidências, as decisões e o tempo efetivamente preso.','LeadX'),Spacer(1,20),P(str(len(D['nodes']))+' pessoas e entidades · '+str(len(D['edges']))+' relações · '+str(len(D['evidence']))+' fichas de evidência · '+str(len(D['sources']))+' fontes'),P('Inclui material invalidado com identificação do status judicial. Uma relação não é um veredito. O relatório distingue fatos documentados, alegações, declarações e conclusões judiciais posteriormente anuladas.'),P('Pesquisa realizada em 28/10/2026. O recorte e as limitações estão explicitados no primeiro capítulo. Não houve perícia independente nas mídias originais nem auditoria integral de todos os andamentos de 2025–2026.'),Spacer(1,25),P('Como usar','H2X'),P('A página seguinte contém o quadro em formato A2: amplie no leitor de PDF. No HTML, passe o mouse e clique nas pessoas e nos fios. Neste documento, procure os identificadores R01–R29 no catálogo de relações e E01–E12 no inventário de evidências.'),P('Fotos e logotipos identificam os personagens e organizações. Sua presença no quadro não atribui responsabilidade criminal.'),PageBreak()]
for ch in D['chapters']:
 flow+=[P(ch['title'],'H1X'),P(ch['lead'],'LeadX')]
 for title,body in ch['parts']:flow+=[P(title,'H2X'),P(body)]
 if ch['sources']:flow+=[refp(ch['sources'])]
 flow+=[Spacer(1,14)]
flow+=[PageBreak(),P('Inventário de evidências','H1X')]
for e in D['evidence']:
 flow+=[P(e['id']+' · '+e['title'],'H2X'),P(e['case']+' / '+e['type'],'SmallX')]
 for label,key in [('O que contém','content'),('Como a acusação usou','claim'),('O que não demonstra sozinha','limit'),('Situação judicial','status')]:flow+=[Paragraph('<b>'+escape(label)+':</b> '+escape(e[key]),styles['BodyX'])]
 if e.get('guide'):flow+=[P(e['guide']['title'],'H2X'),P(e['guide']['text'])]
 flow+=[refp(e['sources']),Spacer(1,8)]
flow+=[PageBreak(),P('Penas e tempo efetivamente preso','H1X'),P('Setas indicam versões sucessivas da pena no mesmo processo; não devem ser somadas.','LeadX')]
for p in D['penalties']:
 flow+=[P(p[0]+' — '+p[1],'H2X'),P('Pena: '+p[2]),P('Custódia: '+p[3]),P('Desfecho: '+p[4]),refp(p[5])]
flow+=[P('José Dirceu: cronologia de custódia','H2X')]
rows=[[P('Intervalo','SmallX'),P('Dias','SmallX'),P('Tipo e contexto','SmallX')]]
for p in D['custody']['periodos']:rows.append([P(p['inicio']+' a '+p['fim'],'SmallX'),P(p['dias'],'SmallX'),P(p['tipo'],'SmallX')])
t=Table(rows,colWidths=[130,40,330],repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e7edf3')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),.5,colors.HexColor('#bac7d2')),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),6)]));flow+=[t,Spacer(1,15),P(D['custody']['metodo'],'SmallX'),P('Totais aproximados: 854 dias em estabelecimento prisional pela Lava Jato; 1.208 dias incluindo o mensalão; outros 272 dias em regime aberto cumprido em casa. Prisões da ditadura não estão incluídas.'),refp(['dirceutempo','dirceucasa','apolo'])]
flow+=[PageBreak(),P('Cronologia dos processos','H1X')]
for t in D['timeline']:flow+=[P(t['date']+' · '+t['title'],'H2X'),P(t['case']+' — '+t['text']),refp(t['sources'])]
flow+=[PageBreak(),P('Catálogo de relações: todos os fios','H1X'),P('Cada identificador corresponde a uma linha do quadro. As relações são específicas; conexões em sequência não provam automaticamente uma transação entre as pontas.','LeadX')]
for e in D['edges']:
 flow+=[P(e['id']+' · '+N[e['a']]['name']+' ↔ '+N[e['b']]['name'],'H2X'),P(LABEL[e['kind']]+' — '+e['label'],'SmallX'),P(e['detail']),P('Status: '+{'documentada':'relação descrita nas fontes, sem transferência automática de responsabilidade','anulada':'contexto de condenação ou atos anulados','acusacao':'hipótese acusatória','declaracao':'declaração atribuída ao depoente','invalidada':'PROVA INVALIDADA — elementos atingidos pela RCL 43.007'}[e['status']]),refp(e['sources'])]
flow+=[PageBreak(),P('Personagens e entidades','H1X')]
for n in D['nodes']:flow+=[P(n['name']+' — '+n['role'],'H2X'),P(n['desc'])]
flow+=[PageBreak(),P('Perguntas e respostas','H1X')]
for q,a in D['faq']:flow+=[P(q,'H2X'),P(a)]
flow+=[PageBreak(),P('Caminhos aos autos oficiais','H1X')]
for case in D.get('cases',{}).values():
 flow+=[P(case['title'],'H2X'),P(case['number']),P(case['court']),P(case['note'])]
 for key in dict.fromkeys([case['portal']]+case['documents']+case['rulings']):
  s=D['sources'][key];flow+=[Paragraph('<link href="'+escape(s['url'],{'"':'&quot;'})+'" color="#185e9c">'+escape(s['title'])+'</link>',styles['BodyX']),P(s['kind'],'SmallX')]
flow+=[PageBreak(),P('Fontes e documentos','H1X'),P('Links são clicáveis. Documentos processuais hospedados por veículos são identificados como cópias públicas. Consulte a fonte para o texto integral e eventuais atualizações.','LeadX')]
for i,(id,s) in enumerate(D['sources'].items()):
 flow+=[P('F%02d · %s'%(i+1,s['title']),'H2X'),P(s['kind']+' · '+s['date'],'SmallX'),Paragraph('<link href="'+escape(s['url'],{'"':'&quot;'})+'" color="#185e9c">'+escape(s['url'])+'</link>',styles['SmallX'])]
flow+=[PageBreak(),P('Créditos das imagens','H1X')]
for id,a in assets.items():
 flow+=[P(a.get('alt',id),'H2X'),P((a.get('author') or a.get('credit') or 'Autoria: consultar origem')+' · '+(a.get('license') or 'Direitos: consultar origem'),'SmallX')]
 if a.get('source'):flow+=[Paragraph('<link href="'+escape(a['source'],{'"':'&quot;'})+'" color="#185e9c">'+escape(a['source'])+'</link>',styles['SmallX'])]
def footer(c,doc):
 c.setStrokeColor(colors.HexColor('#d3dce5'));c.line(42,40,A4[0]-42,40);c.setFont('Arial',8);c.setFillColor(MUTED);c.drawString(42,26,'CONEXÕES · Pesquisa 28/10/2026 · Fontes e limites no relatório');c.drawRightString(A4[0]-42,26,str(doc.page if doc.page==1 else doc.page+1))
doc=SimpleDocTemplate(str(ROOT/'texto-dossie.pdf'),pagesize=A4,leftMargin=45,rightMargin=45,topMargin=44,bottomMargin=55,title='Conexões — Dossiê completo',author='Dossiê documental')
doc.build(flow,onFirstPage=footer,onLaterPages=footer)
writer=PdfWriter();textpdf=PdfReader(ROOT/'texto-dossie.pdf');writer.add_page(textpdf.pages[0]);writer.add_page(PdfReader(ROOT/'quadro-relacoes.pdf').pages[0]);
for p in textpdf.pages[1:]:writer.add_page(p)
with (ROOT/'dossie-completo.pdf').open('wb') as f:writer.write(f)
summary={'nodes':len(D['nodes']),'edges':len(D['edges']),'evidence':len(D['evidence']),'sources':len(D['sources']),'assets':len(assets),'missing_node_assets':[n['id'] for n in D['nodes'] if n['group']!='documento' and n['asset'] not in assets],'pdf_pages':len(writer.pages),'html_bytes':(ROOT/'index.html').stat().st_size}
(ROOT/'build-report.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(summary,ensure_ascii=False))
