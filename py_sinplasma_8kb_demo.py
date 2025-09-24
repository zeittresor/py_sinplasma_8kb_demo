import pygame as p,wave,struct,math,os,random,tempfile
from math import sin as sn,cos as co,pi
rr=random.random;ru=random.uniform
CO=[rr()*6.28 for _ in range(3)]
SW1=ru(-0.3,0.3);SW2=ru(-0.3,0.3)
CBV=[(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]
CBF=[(0,1,2,3),(4,5,6,7),(0,1,5,4),(2,3,7,6),(0,3,7,4),(1,2,6,5)]
THV=[(1,1,1),(-1,-1,1),(-1,1,-1),(1,-1,-1)]
THF=[(0,1,2),(0,1,3),(0,2,3),(1,2,3)]
OCV=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
OCF=[(0,2,4),(2,1,4),(1,3,4),(3,0,4),(0,3,5),(3,1,5),(1,2,5),(2,0,5)]
PYV=[(0,1,0),(1,-1,1),(-1,-1,1),(-1,-1,-1),(1,-1,-1)]
PYF=[(1,2,3,4),(0,1,2),(0,2,3),(0,3,4),(0,4,1)]
def sh(sf,t,vs,fs):
    ang=t*0.6;ca=co(ang);sa=sn(ang);cbg=co(ang*0.5);sbg=sn(ang*0.5);
    ps=[]
    for vx,vy,vz in vs:
        x1=vx*ca-vz*sa;z1=vx*sa+vz*ca;y1=vy*cbg-z1*sbg;z2=vy*sbg+z1*cbg;sc=350/(z2+3);
        ps.append((int(W/2+x1*sc),int(H/2+y1*sc),z2))
    sf.fill((0,0,0))
    for face in fs:
        z=sum(ps[i][2] for i in face)/len(face)
        col=int(max(0,min(255,200+z*40)))
        pg=[ps[i][:2] for i in face]
        p.draw.polygon(sf,(col,col*0.6,col*0.3),pg)
def g():
    dt=tempfile.gettempdir();sr=22050;dur=48
    mp=os.path.join(dt,'m.wav')
    pool=(69,73,82,87,98,110,123)
    nr=int(4+rr()*3);roots=random.sample(pool,nr)
    segD=4+int(rr()*3)
    kf=ru(18,28);kw=ru(0.25,0.4)
    fma=ru(0.1,0.35);fmr=ru(1.4,3);fmm=ru(0.2,0.6)
    fma2=ru(0.05,0.2);fmr2=ru(1,2.5);fmm2=ru(0.1,0.4)
    wv=wave.open(mp,'wb');wv.setnchannels(1);wv.setsampwidth(2);wv.setframerate(sr)
    for i in range(int(sr*dur)):
        t=i/sr
        seg=int(t/segD)%len(roots);root=roots[seg];third=root*5/4;fifth=root*3/2
        ph=(t%segD)/segD
        mel=(sn(2*pi*root*t)+0.6*sn(2*pi*third*t)+0.5*sn(2*pi*fifth*t))*(1-ph)
        mel*=0.25
        bass=sn(2*pi*(root/2)*t)*0.4
        bp=t%1;kick=sn(2*pi*kf*t)*(max(0,kw-bp)/kw)
        amb=(sn(2*pi*0.03*t)+sn(2*pi*0.041*t))*0.12
        fm=sn(2*pi*root*fmr*t+fmm*sn(2*pi*root*t))*fma
        fm+=sn(2*pi*(root*0.5)*fmr2*t+fmm2*sn(2*pi*(root*0.5)*t))*fma2
        fm*=1+t/dur
        env=sn(pi*t/dur*0.5)**2
        s=(amb+mel*0.8+bass+kick+fm)*env
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
    br=int(128+127*sn(t*0.1+CO[0]));bg=int(128+127*sn(t*0.1+2+CO[1]));bb=int(128+127*sn(t*0.1+4+CO[2]))
    CO[0]+=0.001;CO[1]+=0.0015;CO[2]+=0.002
    for y in range(0,H,4):
        h=int(128*(sn(y*0.03+t*0.4)+1))
        p.draw.line(sf,(br*h//255,bg*h//255,bb*h//255),(0,y),(W,y))
def ss(sfce,sw,d):
    global st
    sfce.fill((0,0,0))
    for s in st:
        x,y,vx,vy,r,sh=s
        if sw:
            dx=x-W/2;dy=y-H/2;vx+=sw*dy*d;vy-=sw*dx*d
        x+=vx*d;y+=vy*d;r+=d*50
        s[0]=x;s[1]=y;s[2]=vx;s[3]=vy;s[4]=r
    st=[s for s in st if 0<=s[0]<W and 0<=s[1]<H]
    cx=W/2+sn(tm*0.2)*W*0.25;cy=H/2+co(tm*0.17)*H*0.25
    for _ in range(5):
        a=rr()*2*pi;sp=ru(50,200);sh=int(rr()*3)
        st.append([cx,cy,co(a)*sp,sn(a)*sp,1,sh])
    for s in st:
        c=min(255,int(s[4]*10))
        rad=max(1,int(s[4]*0.05))
        sh=s[5]
        if sh==0:
            p.draw.circle(sfce,(c,c,c),(int(s[0]),int(s[1])),rad)
        elif sh==1:
            p.draw.rect(sfce,(c,c,c),(int(s[0])-rad,int(s[1])-rad,rad*2,rad*2))
        else:
            x0=int(s[0]);y0=int(s[1])
            pts=[(x0,y0-rad),(x0+rad,y0+rad),(x0-rad,y0+rad)]
            p.draw.polygon(sfce,(c,c,c),pts)
def cb(sf,t):sh(sf,t,CBV,CBF)
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
def th(sf,t):sh(sf,t,THV,THF)
def oc(sf,t):sh(sf,t,OCV,OCF)
def hx(sf,t):
    sf.fill((0,0,0))
    m=max(W,H)/3
    for i in range(100):
        z=i/100;a=t*1.2+i*0.15;r=(1-z)*m;x=int(W/2+co(a)*r);y=int(H/2+sn(a)*r);
        c=int(255*z);p.draw.circle(sf,(c,int(c*0.7),int(c*0.4)),(x,y),4)
def ls(sf,t):
    sf.fill((0,0,0))
    pts=[]
    for i in range(200):
        a=i*0.03;x=int(W/2+co(3*a+t)*W*0.3);y=int(H/2+sn(4*a+t*1.5)*H*0.3);pts.append((x,y))
    p.draw.lines(sf,(200,100,200),True,pts,2)
def vg(sf,t):
    sf.fill((0,0,0))
    for i in range(0,W,40):
        for j in range(0,H,40):
            x=i+int(sn(i*0.05+t)*10);y=j+int(co(j*0.05-t)*10);c=int(128+127*sn((i+j)*0.02+t*0.3));p.draw.circle(sf,(c,c//2,255-c),(x,y),2)
def sc(sf,t):
    sf.fill((0,0,0))
    s="github.com/zeittresor"
    wd=F.size("A")[0]
    off=int((t*80)%(len(s)*wd))
    for i,ch in enumerate(s*2):
        x=(i*wd-off)%W
        y=int(H*0.5+sn(i*0.4+t*1.5)*H*0.1)
        col=200+int(55*sn(i*0.5+t))
        sur=F.render(ch,1,(col,col*0.7,255-col))
        sf.blit(sur,(x,y))
def np(sf,t):
    for x in range(80):
        for y in range(80):
            v=int(128+127*sn(x*0.08+t)+127*sn(y*0.08-t)+127*sn((x+y)*0.04+t*0.5));v=max(0,min(255,v))
            g=int(v*0.5+127*sn(t*0.2))
            g=max(0,min(255,g))
            P.set_at((x,y),(v,g,255-v))
    Q=p.transform.smoothscale(P,(W,H));Q.set_alpha(90);sf.blit(Q,(0,0))
def og(sf,t):
    sf.fill((0,0,0))
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
    sg=tm%sd;i=int(tm/sd)%15;j=(i+1)%15;a=0
    if sg>sd-fd:a=(sg-(sd-fd))/fd
    if i==0:bw(u,tm)
    elif i==1:ss(u,SW1,d)
    elif i==2:ss(u,SW2,d)
    elif i==3:cb(u,tm)
    elif i==4:th(u,tm)
    elif i==5:oc(u,tm)
    elif i==6:tn(u,tm)
    elif i==7:dm(u,tm)
    elif i==8:og(u,tm)
    elif i==9:hx(u,tm)
    elif i==10:ls(u,tm)
    elif i==11:vg(u,tm)
    elif i==12:sc(u,tm)
    elif i==13:np(u,tm)
    elif i==14:sh(u,tm,PYV,PYF)
    else:np(u,tm)
    if j==0:bw(v,tm)
    elif j==1:ss(v,SW1,d)
    elif j==2:ss(v,SW2,d)
    elif j==3:cb(v,tm)
    elif j==4:th(v,tm)
    elif j==5:oc(v,tm)
    elif j==6:tn(v,tm)
    elif j==7:dm(v,tm)
    elif j==8:og(v,tm)
    elif j==9:hx(v,tm)
    elif j==10:ls(v,tm)
    elif j==11:vg(v,tm)
    elif j==12:sc(v,tm)
    elif j==13:np(v,tm)
    elif j==14:sh(v,tm,PYV,PYF)
    else:np(v,tm)
    u.set_alpha(int(255*(1-a)));v.set_alpha(int(255*a))
    S.blit(u,(0,0));S.blit(v,(0,0))
    pl(tm)
    np(S,tm)
    p.display.flip()
p.quit()
