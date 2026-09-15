"""Build the expanded, source-grounded guide and its editable Markdown companion."""
from pathlib import Path
from html import escape
import json
import re
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                               TableStyle, PageBreak, Preformatted, KeepTogether,
                               Flowable)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from guide_content import AUTHORS, PAGES

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/Guia-Microproyecto2-AKS.pdf'
MD = ROOT / 'docs/Guia-Microproyecto2-AKS.md'
INK=colors.HexColor('#17263d')
BODY=colors.HexColor('#28364c')
MUTED=colors.HexColor('#5a697f')
PURPLE=colors.HexColor('#6152ce')
TEAL=colors.HexColor('#117c78')
PALE=colors.HexColor('#f0eefb')
LINE=colors.HexColor('#dce3ee')
W=170*mm
ST={
 'title':ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=25,leading=29,textColor=INK,spaceAfter=10),
 'cover':ParagraphStyle('cover',fontName='Helvetica-Bold',fontSize=32,leading=37,textColor=INK,spaceAfter=19),
 'subtitle':ParagraphStyle('subtitle',fontName='Helvetica',fontSize=10.6,leading=14.5,textColor=MUTED,spaceAfter=12),
 'body':ParagraphStyle('body',fontName='Helvetica',fontSize=10.3,leading=14.2,textColor=BODY,spaceAfter=7),
 'sub':ParagraphStyle('sub',fontName='Helvetica-Bold',fontSize=11.4,leading=14.8,textColor=INK,spaceBefore=7,spaceAfter=5,keepWithNext=True),
 'small':ParagraphStyle('small',fontName='Helvetica',fontSize=8.8,leading=12.3,textColor=MUTED,spaceAfter=7),
 'kicker':ParagraphStyle('kicker',fontName='Helvetica-Bold',fontSize=8.3,leading=11,textColor=PURPLE,spaceAfter=11),
 'cell':ParagraphStyle('cell',fontName='Helvetica',fontSize=9.1,leading=12,textColor=BODY),
 'head':ParagraphStyle('head',fontName='Helvetica-Bold',fontSize=9.1,leading=12,textColor=colors.white),
 'note':ParagraphStyle('note',fontName='Helvetica',fontSize=9.9,leading=13.5,textColor=BODY),
 'code':ParagraphStyle('code',fontName='Courier',fontSize=8.3,leading=11.3,textColor=INK),
 'author':ParagraphStyle('author',fontName='Helvetica-Bold',fontSize=12.2,leading=18,textColor=INK,spaceAfter=4),
 'source':ParagraphStyle('source',fontName='Helvetica',fontSize=9.1,leading=12.5,textColor=BODY,spaceAfter=7),
}
SOURCES=[
 ('S1','Kubernetes: Deployments','https://kubernetes.io/docs/concepts/workloads/controllers/deployment/'),
 ('S2','Kubernetes: volúmenes persistentes','https://kubernetes.io/docs/concepts/storage/persistent-volumes/'),
 ('S3','TorchVision 0.23: MobileNetV3 Small y pesos','https://docs.pytorch.org/vision/0.23/models/generated/torchvision.models.mobilenet_v3_small.html'),
 ('S4','Kubernetes: sondas de inicio, disponibilidad y salud','https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/'),
 ('S5','Microsoft: crear AKS mediante Azure Portal','https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-portal'),
 ('S6','Microsoft: grupos de nodos del sistema','https://learn.microsoft.com/en-us/azure/aks/use-system-pools'),
 ('S7','Microsoft: integrar ACR con AKS','https://learn.microsoft.com/en-us/azure/aks/cluster-container-registry-integration'),
 ('S8','Microsoft: habilitar monitoreo en AKS','https://learn.microsoft.com/en-us/azure/azure-monitor/containers/kubernetes-monitoring-enable'),
 ('S9','Kubernetes: Horizontal Pod Autoscaler','https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/'),
]

def clean(text):
    # Angle brackets used as literal UI values must not be treated as XML tags.
    text=text.replace('<unknown>', '&lt;unknown&gt;')
    for key,_,_ in SOURCES:
        text=text.replace(f'[{key}]',f'<link href="#source-{key}" color="#6152ce">[{key}]</link>')
    return text

def para(text, style='body'):
    return Paragraph(clean(text),ST[style])

def make_table(headers,rows,widths):
    assert abs(sum(widths)-170)<0.1
    data=[[Paragraph(escape(str(c)),ST['head']) for c in headers]]
    data += [[Paragraph(escape(str(c)),ST['cell']) for c in row] for row in rows]
    t=Table(data,colWidths=[v*mm for v in widths],repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),INK),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f5f7fb')]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LINEBELOW',(0,0),(-1,0),.6,INK),
        ('LINEBELOW',(0,1),(-1,-1),.45,LINE),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ]))
    return t

def callout(title,text):
    inner=para(f'<b>{escape(title)}</b><br/>{text}','note')
    t=Table([[inner]],colWidths=[W],hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),PALE),('LINEBEFORE',(0,0),(0,0),3,PURPLE),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    return t

class Architecture(Flowable):
    """Vector illustration: access, runtime, storage and telemetry, not measured topology."""
    def __init__(self):
        Flowable.__init__(self); self.width=W; self.height=275
    def draw(self):
        c=self.canv
        def box(x,y,w,h,title,lines=(),fill=colors.white,accent=PURPLE):
            c.setFillColor(fill);c.setStrokeColor(LINE);c.roundRect(x,y,w,h,7,fill=1,stroke=1)
            c.setFillColor(accent);c.rect(x,y+8,3,h-16,fill=1,stroke=0)
            c.setFont('Helvetica-Bold',10);c.setFillColor(INK);c.drawString(x+12,y+h-18,title)
            c.setFont('Helvetica',8.4);c.setFillColor(MUTED)
            for i,line in enumerate(lines):c.drawString(x+12,y+h-33-i*12,line)
        def arrow(x1,y1,x2,y2,dashed=False):
            import math
            c.setStrokeColor(MUTED);c.setLineWidth(.9)
            if dashed:c.setDash(3,3)
            c.line(x1,y1,x2,y2);c.setDash()
            a=math.atan2(y2-y1,x2-x1);size=5
            path=c.beginPath();path.moveTo(x2,y2)
            path.lineTo(x2-size*math.cos(a-.5),y2-size*math.sin(a-.5))
            path.lineTo(x2-size*math.cos(a+.5),y2-size*math.sin(a+.5));path.close()
            c.setFillColor(MUTED);c.drawPath(path,fill=1,stroke=0)
        box(0,205,218,61,'Computador',('Navegador + kubectl port-forward',),fill=PALE)
        box(270,205,212,61,'Azure Container Registry',('Imágenes classifier y planner',),fill=PALE)
        c.setFillColor(colors.HexColor('#f5f8fb'));c.setStrokeColor(LINE)
        c.roundRect(0,60,482,123,9,fill=1,stroke=1)
        c.setFillColor(INK);c.setFont('Helvetica-Bold',10.5)
        c.drawString(12,164,'AKS · 2 nodos · namespace microproyecto2')
        box(12,79,213,67,'Visión AI',('Service classifier','2 Pods · sin fotografías persistidas'),accent=TEAL)
        box(257,79,213,67,'Campus Planner',('Service planner','1 Pod · SQLite en /data'),accent=TEAL)
        arrow(109,205,109,184); arrow(376,205,376,184,True)
        box(0,0,225,46,'Azure Monitor',('Container Insights + Log Analytics',),accent=TEAL)
        box(257,0,225,46,'PVC planner-data',('Disco independiente del Pod',),accent=TEAL)
        arrow(109,79,109,46,True);arrow(363,79,363,46)
        c.setFont('Helvetica',7.6);c.setFillColor(MUTED)
        c.drawString(118,53,'registros');c.drawString(371,53,'datos')

class GuideDoc(SimpleDocTemplate):
    def afterFlowable(self,flowable):
        key=getattr(flowable,'_guide_key',None)
        if key:
            self.canv.bookmarkPage(key)
            title=getattr(flowable,'_guide_title',key)
            self.canv.addOutlineEntry(title,key,level=0,closed=False)
            starts[key]=self.page
        source=getattr(flowable,'_source_key',None)
        if source:self.canv.bookmarkPage(source)

starts={}
story=[]
markdown=['# Guía de ejecución del microproyecto 2','',
          'Kubernetes en Azure con clasificación de imágenes, persistencia y monitoreo.','',
          '**Integrantes incluidos:** '+', '.join(AUTHORS)+'.','',
          '**Edición:** 14 de septiembre de 2026.','']

def plain(text):
    text=re.sub(r'<br\s*/?>','\n',text)
    text=re.sub(r'<b>(.*?)</b>',r'**\1**',text)
    return text

for number,section in enumerate(PAGES,1):
    if number>1:story.append(PageBreak())
    if number==1:
        story.append(para('UNIVERSIDAD AUTÓNOMA DE OCCIDENTE','kicker'))
    else:
        story.append(para(f'MICROPROYECTO 02  /  SECCIÓN {number:02d}','kicker'))
    heading=para(escape(section['title']).replace('\n','<br/>'),'cover' if number==1 else 'title')
    heading._guide_key=f'page-{number}'
    heading._guide_title=section['title'].replace('\n',' ')
    story.append(heading)
    story.append(para(section['subtitle'],'subtitle'))
    markdown += [f"## {number:02d}. {section['title'].replace(chr(10),' ')}",'',section['subtitle'],'']
    for block in section['blocks']:
        kind=block[0]
        if kind=='p':story.append(para(block[1]));markdown += [plain(block[1]),'']
        elif kind=='h':story.append(para(block[1],'sub'));markdown += ['### '+block[1],'']
        elif kind=='ref':story.append(para(block[1],'small'));markdown += [plain(block[1]),'']
        elif kind=='table':
            story += [make_table(*block[1:]),Spacer(1,10)]
            markdown += ['| '+' | '.join(block[1])+' |','| '+' | '.join(['---']*len(block[1]))+' |']
            markdown += ['| '+' | '.join(map(str,row))+' |' for row in block[2]]
            markdown += ['']
        elif kind=='code':
            if max(map(len,block[1].splitlines()))>91:
                raise ValueError(f'Code line too long on page {number}')
            t=Table([[Preformatted(block[1],ST['code'])]],colWidths=[W],hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#edf3f6')),
                                   ('BOX',(0,0),(-1,-1),.5,LINE),
                                   ('LEFTPADDING',(0,0),(-1,-1),10),
                                   ('RIGHTPADDING',(0,0),(-1,-1),10),
                                   ('TOPPADDING',(0,0),(-1,-1),9),
                                   ('BOTTOMPADDING',(0,0),(-1,-1),9)]))
            story += [t,Spacer(1,10)];markdown += ['```',block[1],'```','']
        elif kind=='note':
            story += [Spacer(1,4),callout(block[1],block[2]),Spacer(1,10)]
            markdown += ['> **'+block[1]+'**', '> '+plain(block[2]),'']
        elif kind=='cover':
            story.append(Spacer(1,5))
            for author in AUTHORS:story.append(para(escape(author),'author'))
            story.append(Spacer(1,21))
        elif kind=='diagram':
            story += [Architecture(),Spacer(1,13)]
            markdown += ['```mermaid','flowchart TB',
                         '  U[Computador y túnel autenticado] --> A[AKS: 2 nodos]',
                         '  R[ACR: imágenes] -.-> A',
                         '  A --> C[Clasificador: 2 Pods]',
                         '  A --> P[Planner: 1 Pod]',
                         '  P --> V[PVC y disco]',
                         '  C -. registros .-> M[Container Insights y Log Analytics]',
                         '  P -. registros .-> M','```','']
        elif kind=='sources':
            for key,label,url in SOURCES:
                q=Paragraph(f'<b>{key}.</b> <link href="{escape(url,quote=True)}" color="#6152ce">{escape(label)}</link>',ST['source'])
                q._source_key='source-'+key
                story.append(q)
                markdown += [f'- [{key}: {label}]({url})']
            story.append(Spacer(1,4));markdown+=['']
        else:raise ValueError(kind)

def footer(canvas,doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE);canvas.setLineWidth(.6)
    canvas.line(20*mm,18*mm,190*mm,18*mm)
    canvas.setFont('Helvetica',8);canvas.setFillColor(MUTED)
    canvas.drawString(20*mm,13*mm,'UAO  |  Computación en la Nube  |  Guía de ejecución ampliada')
    canvas.drawRightString(190*mm,13*mm,f'{doc.page:02d} / {len(PAGES):02d}')
    canvas.setFillColor(PURPLE);canvas.rect(20*mm,20*mm,10*mm,1.1*mm,fill=1,stroke=0)
    canvas.restoreState()

OUT.parent.mkdir(exist_ok=True)
doc=GuideDoc(str(OUT),pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,
             topMargin=21*mm,bottomMargin=24*mm,
             title='Guía de ejecución del microproyecto 2 · Edición ampliada',
             author='; '.join(AUTHORS),subject='Arquitectura, justificación, ejecución, pruebas y sustentación de AKS')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
MD.write_text('\n'.join(markdown),encoding='utf-8')
report={'expected_pages':len(PAGES),'section_start_pages':starts,
        'misplaced_sections':{k:v for k,v in starts.items() if v!=int(k.split('-')[1])}}
(ROOT/'build').mkdir(exist_ok=True)
(ROOT/'build/guide-layout.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(OUT)
print(json.dumps(report,ensure_ascii=False))
