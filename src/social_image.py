"""Render a social card using a real screenshot of the public board."""
from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import pypdfium2
ROOT=Path(__file__).resolve().parent.parent
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold','C:/Windows/Fonts/arialbd.ttf'))
shot=Image.open(ROOT/'src/assets/painel-captura.jpg')
# Crop only the board, excluding browser UI and the side explanation.
board=shot.crop((42,215,670,735))
pdf=ROOT/'social-preview.pdf'
c=canvas.Canvas(str(pdf),pagesize=(1200,630))
c.setFillColorRGB(.047,.071,.106);c.rect(0,0,1200,630,fill=1,stroke=0)
c.setFillColorRGB(.94,.78,.46);c.setFont('ArialBold',16);c.drawString(48,575,'LAVA JATO / INTERATIVA')
c.setFillColorRGB(.96,.97,.98);c.setFont('ArialBold',58);c.drawString(48,452,'Siga os fios.')
c.setFillColorRGB(.94,.78,.46);c.setFont('ArialBold',39);c.drawString(48,384,'Entenda cada');c.drawString(48,336,'ligação.')
c.setFillColorRGB(.72,.80,.88);c.setFont('Arial',19)
for y,t in [(267,'Relações, evidências e decisões.'),(235,'Dos personagens aos documentos.'),(150,'20 pessoas e entidades'),(120,'29 relações com fontes públicas')]:c.drawString(48,y,t)
c.setFillColorRGB(.88,.78,.60);c.setFont('ArialBold',16);c.drawString(48,47,'lavajatointerativa.com.br')
c.setStrokeColorRGB(.48,.34,.21);c.setLineWidth(12);c.roundRect(548,47,610,540,8,stroke=1,fill=0)
c.drawImage(ImageReader(board),554,53,width=598,height=528,mask='auto')
c.save()
doc=pypdfium2.PdfDocument(pdf)
im=doc[0].render(scale=1).to_pil().convert('RGB')
im.save(ROOT/'assets/compartilhar.jpg',quality=93,optimize=True)
print('Imagem social:',im.size)
