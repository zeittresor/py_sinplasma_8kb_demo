import pygame as p,wave,struct,math,os,random,tempfile
# github.com/zeittresor
from math import sin as sn,cos as co,pi
rr=random.random;ru=random.uniform
def g():
    dt=tempfile.gettempdir();sr=22050;dur=48
    mp=os.path.join(dt,'m.wav')
    wv=wave.open(mp,'wb');wv.setnchannels(1);wv.setsampwidth(2);wv.setframerate(sr)
    for i in range(int(sr*dur)):
        t=i/sr
        # cycle through roots every 8 seconds (G3,A3,B3,C4)
        seg=int(t/8)%4;root=(196,220,247,262)[seg]
        # major chord components
        third=root*5/4;fifth=root*3/2
        ph=(t%8)/8
        # fading melody envelope
        mel=(sn(2*pi*root*t)+0.6*sn(2*pi*third*t)+0.5*sn(2*pi*fifth*t))*0.3*(1-ph)
        # sub bass
        bass=sn(2*pi*(root/2)*t)*0.4
        # kick: deep sine burst on whole second with slower tempo
        bp=t%1;kick=sn(2*pi*24*t)*(max(0,0.3-bp)/0.3)
        # slowly evolving ambient pad
        amb=(sn(2*pi*0.03*t)+sn(2*pi*0.041*t))*0.15
        s=amb+mel+bass+kick
        wv.writeframes(struct.pack('<h',int(max(-1,min(1,s))*32767)))
    wv.close()
    return mp
p.init();p.mixer.init(22050,-16,1)
info=p.display.Info();W,H=info.current_w,info.current_h
S=p.display.set_mode((W,H),p.FULLSCREEN);p.mouse.set_visible(False)
F=p.font.Font(None,int(H*0.12))
txt=F.render('wait',1,(220,220,240))
S.fill((0,0,0));S.blit(txt,(W//2-txt.get_width()//2,H//2-txt.get_height()//2));p.display.flip()
mp=g()
try:
    p.mixer.music.load(mp);p.mixer.music.play(-1)
except:pass
u=p.Surface((W,H));v=p.Surface((W,H))
st=[];P=p.Surface((80,80))
C=p.time.Clock();tm=0
sd=8;fd=2
def bw(sf,t):
    sf.fill((0,0,0))
    br=int(128+127*sn(t*0.1));bg=int(128+127*sn(t*0.1+2));bb=int(128+127*sn(t*0.1+4))
    for y in range(0,H,4):
        h=int(128*(sn(y*0.03+t*0.4)+1))
        p.draw.line(sf,(br*h//255,bg*h//255,bb*h//255),(0,y),(W,y))
def ss(sfce,sw,d):
    global st
    sfce.fill((0,0,0))
    for s in st:
        x,y,vx,vy,r=s
        if sw:
            dx=x-W/2;dy=y-H/2;vx+=sw*dy*d;vy-=sw*dx*d
        x+=vx*d;y+=vy*d;r+=d*50
        s[0]=x;s[1]=y;s[2]=vx;s[3]=vy;s[4]=r
    st=[s for s in st if 0<=s[0]<W and 0<=s[1]<H]
    # spawn new particles from moving center
    cx=W/2+sn(tm*0.2)*W*0.25;cy=H/2+co(tm*0.17)*H*0.25
    for _ in range(5):
        a=rr()*2*pi;sp=ru(50,200);st.append([cx,cy,co(a)*sp,sn(a)*sp,1])
    for s in st:
        c=min(255,int(s[4]*10))
        rad=max(1,int(s[4]*0.05))
        sh=int(s[4])%3
        if sh==0:
            p.draw.circle(sfce,(c,c,c),(int(s[0]),int(s[1])),rad)
        elif sh==1:
            p.draw.rect(sfce,(c,c,c),(int(s[0])-rad,int(s[1])-rad,rad*2,rad*2))
        else:
            x0=int(s[0]);y0=int(s[1])
            pts=[(x0,y0-rad),(x0+rad,y0+rad),(x0-rad,y0+rad)]
            p.draw.polygon(sfce,(c,c,c),pts)
def cb(sf,t):
    verts=[(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]
    edges=[(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
    ang=t*0.6;ca=co(ang);sa=sn(ang);cbg=co(ang*0.5);sbg=sn(ang*0.5)
    pts=[]
    for vx,vy,vz in verts:
        x1=vx*ca-vz*sa;z1=vx*sa+vz*ca;y1=vy*cbg-z1*sbg;z2=vy*sbg+z1*cbg;sc=300/(z2+3)
        pts.append((int(W/2+x1*sc),int(H/2+y1*sc),z2))
    sf.fill((0,0,0))
    for a,b in edges:
        zavg=(pts[a][2]+pts[b][2])*0.5;col=int(max(0,min(255,200+zavg*30)))
        p.draw.line(sf,(col,col,col),pts[a][:2],pts[b][:2],2)
def pl(t):
    for x in range(80):
        for y in range(80):
            v=int(128+127*sn(0.13*x+t*0.5)+127*sn(0.14*y-t*0.5));v=max(0,min(255,v));P.set_at((x,y),(v,v//2,v))
    Q=p.transform.smoothscale(P,(W,H));Q.set_alpha(80);S.blit(Q,(0,0))
def tn(sf,t):
    sf.fill((0,0,0))
    for i in range(30):
        r=i/30;rad=int((1-r)*(W if W<H else H)/2)
        xo=int(sn(t*2+i*0.1)*60);yo=int(co(t*2+i*0.1)*60)
        c=int(255*(1-r));p.draw.circle(sf,(c,int(c*0.7),int(c*0.4)),(W//2+xo,H//2+yo),rad,1)
def dm(sf,t):
    sf.fill((0,0,0))
    for i in range(20):
        r=i/20;w0=int(W*(1-r*0.8));h0=int(H*(1-r*0.8))
        xo=int(sn(t*1.5+i)*40);yo=int(co(t*1.5+i)*40)
        x0=(W-w0)//2+xo;y0=(H-h0)//2+yo;col=int(255*(1-r))
        p.draw.rect(sf,(col,int(col*0.6),int(col*0.3)),(x0,y0,w0,h0),2)
def og(sf,t):
    sf.fill((0,0,0))
    # draw a rotating rose/organic curve
    for i in range(120):
        a=i*pi/60+t*0.5
        r=0.4+0.3*sn(3*a)
        x=int(W/2+r*co(a)*W*0.3)
        y=int(H/2+r*sn(a)*H*0.3)
        col=int(200+55*sn(5*a))
        p.draw.circle(sf,(col,col//2,255-col),(x,y),3)
running=True
while running:
    for e in p.event.get():
        if e.type==p.QUIT or (e.type==p.KEYDOWN and e.key==27):running=False
    d=C.tick(60)/1000;tm+=d
    cur=p.time.get_ticks()/1000
    sg=tm%sd;i=int(tm/sd)%7;j=(i+1)%7;a=0
    if sg>sd-fd:a=(sg-(sd-fd))/fd
    if i==0:bw(u,tm)
    elif i==1:ss(u,0,d)
    elif i==2:ss(u,0.2,d)
    elif i==3:cb(u,tm)
    elif i==4:tn(u,tm)
    elif i==5:dm(u,tm)
    else:og(u,tm)
    if j==0:bw(v,tm)
    elif j==1:ss(v,0,d)
    elif j==2:ss(v,0.2,d)
    elif j==3:cb(v,tm)
    elif j==4:tn(v,tm)
    elif j==5:dm(v,tm)
    else:og(v,tm)
    u.set_alpha(int(255*(1-a)));v.set_alpha(int(255*a))
    S.blit(u,(0,0));S.blit(v,(0,0))
    pl(tm)
    p.display.flip()
p.quit()