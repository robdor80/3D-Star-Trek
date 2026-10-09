"""Dibuja medidas numéricas propias; nunca abre imágenes de referencia.

Pillow del runtime ya instalado de Codex. Sin IA generativa ni instalaciones.
Produce gráficos PNG nuevos, de planta muestreada y sección longitudinal.
"""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--grid',type=Path,required=True)
    parser.add_argument('--rutas',type=Path,required=True)
    parser.add_argument('--salida',type=Path,required=True)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[2]
    out=args.salida.resolve()
    if out.exists() or out==root/'assets' or root/'assets' in out.parents:
        raise RuntimeError('Salida nueva fuera de assets obligatoria')
    grid=json.loads(args.grid.read_text(encoding='utf-8'))
    routes=json.loads(args.rutas.read_text(encoding='utf-8'))
    out.mkdir(parents=True)
    font_path=Path('C:/Windows/Fonts/segoeui.ttf')
    font=ImageFont.truetype(str(font_path),17)
    small=ImageFont.truetype(str(font_path),14)
    big=ImageFont.truetype(str(font_path),24)
    colors={'clear':'#43a989','blocked':'#de7273','deep':'#9980c4','none':'#e6e9ed'}
    img=Image.new('RGB',(1100,1020),'#ffffff'); draw=ImageDraw.Draw(img)
    draw.text((65,20),'Enterprise — planta de ensayo de cápsula',fill='#142538',font=big)
    draw.text((65,56),'Radio 0,34 m · altura 1,76 m · grid 0,25 m · coordenadas mundiales en metros',fill='#445363',font=font)
    scale=42
    def xy(x,y): return (550+x*scale,470-y*scale)
    for row in grid['grid']:
        color=colors['none'] if row['floor_z'] is None else (colors['deep'] if row['floor_z']<-.12 else colors['clear' if row['clear'] else 'blocked'])
        x,y=xy(row['x'],row['y']); half=grid['grid_step']*scale/2
        draw.rectangle((x-half,y-half,x+half,y+half),fill=color)
    for x in range(-10,11,2):
        a,b=xy(x,-8),xy(x,8); draw.line((a,b),fill='#afbac5',width=1); draw.text((a[0]-8,a[1]+10),str(x),fill='#263d54',font=small)
    for y in range(-8,9,2):
        a,b=xy(-10.5,y),xy(10.5,y); draw.line((a,b),fill='#afbac5',width=1); draw.text((a[0]-38,a[1]-10),str(y),fill='#263d54',font=small)
    for label,row in routes['routes'].items():
        if row['continuous_flat_route_certified']:
            draw.line([xy(*p) for p in row['waypoints']],fill='#133b72',width=3)
    # Cajas de referencia declaradas; no contornos exactos de la geometría.
    for label,lo,hi in [('Capitán',(-.595,4.286),(.613,5.308)),('CONN/OPS',(-2.078,-.193),(2.003,1.874))]:
        a,b=xy(lo[0],hi[1]),xy(hi[0],lo[1]); draw.rectangle((*a,*b),outline='#16263a',width=2)
        draw.text((a[0]+5,a[1]+5),label,fill='#12253a',font=small)
    a,b=xy(-1.5,8.3),xy(1.5,6.4); draw.rectangle((*a,*b),outline='#c25508',width=3)
    draw.text((b[0]+10,a[1]+10),'Conexión propuesta\nNO abierta',fill='#a44909',font=small)
    draw.text((1010,240),'+Y\nfondo',fill='#263d54',font=small)
    draw.text((1010,630),'−Y\nfrente',fill='#263d54',font=small)
    for i,(key,label) in enumerate([('clear','Cápsula libre en muestra'),('blocked','Intersección con geometría'),('deep','Apoyo por debajo de z=−0,12'),('none','Sin apoyo aceptado por el rayo')]):
        x,y=65+(i%2)*500,920+(i//2)*30
        draw.rectangle((x,y,x+20,y+20),fill=colors[key]); draw.text((x+30,y-1),label,fill='#263d54',font=font)
    draw.text((65,868),'Azul: recorridos planos con margen geométrico continuo comprobado. Sin prueba UE5.',fill='#263d54',font=font)
    img.save(out/'planta_capsula.png')

    img=Image.new('RGB',(1100,590),'#ffffff'); draw=ImageDraw.Draw(img)
    draw.text((65,20),'Sección posterior central — cotas medidas y empalme propuesto',fill='#142538',font=big)
    def yz(y,z): return (100+(y-5.4)*285,430-(z+.8)*85)
    for y in [5.4,6,6.46,6.53,7,8,8.15,8.3]:
        p=yz(y,-.8); draw.line((yz(y,-.8),yz(y,3)),fill='#d9dfe5')
        text_x=p[0]-15
        text_y=p[1]+12
        if y==6.46: text_x-=22
        if y==6.53: text_y+=20
        draw.text((text_x,text_y),str(y),fill='#263d54',font=small)
    for z in [-.68,0,.43,1,2,2.63,2.85]:
        p=yz(5.4,z); draw.line((p,yz(8.4,z)),fill='#d9dfe5'); draw.text((p[0]-55,p[1]-10),str(z),fill='#263d54',font=small)
    rows=routes['profiles']['posterior_Y_0']
    for a,b in zip(rows,rows[1:]):
        if a['floor_z'] is not None and b['floor_z'] is not None:
            draw.line((yz(a['y'],a['floor_z']),yz(b['y'],b['floor_z'])),fill='#276c75',width=4)
    draw.line((yz(6.46,.43),yz(8.3,.43)),fill='#df750b',width=3)
    draw.line((yz(6.46,2.63),yz(8.3,2.63)),fill='#df750b',width=2)
    draw.line((yz(6.49,.43),yz(6.49,2.63)),fill='#df5353',width=5)
    draw.line((yz(8.15,-.68),yz(8.15,2.85)),fill='#df5353',width=5)
    draw.text((380,330),'Δ suelo = 1,11 m',fill='#903852',font=font)
    draw.text((510,75),'Altura libre propuesta 2,20 m · reserva nominal bajo techo ≈0,22 m',fill='#a44909',font=small)
    draw.text((100,490),'Verde: apoyo por rayo. Naranja: plano propuesto, sin malla nueva. Rojo: cerramientos.',fill='#263d54',font=font)
    draw.text((100,525),'Eje horizontal Y (m); vertical Z (m). Los cerramientos se simplifican a planos para el gráfico.',fill='#263d54',font=small)
    img.save(out/'seccion_posterior.png')
    (out/'MANIFIESTO_GRAFICOS.json').write_text(json.dumps({'grid':str(args.grid),'routes':str(args.rutas),
        'source_sha256':grid['original_sha256'],'outputs':['planta_capsula.png','seccion_posterior.png'],
        'note':'Solo datos numéricos del Enterprise. No se leen imágenes de assets. Cajas y paredes esquemáticas etiquetadas.'},ensure_ascii=False,indent=2),encoding='utf-8')


if __name__=='__main__': main()
