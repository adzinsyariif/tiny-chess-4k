import json,os,urllib.request
E=os.environ["MAKEFUN_ENV_URL"]
def post(p,b):return json.load(urllib.request.urlopen(urllib.request.Request(E+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})))
V=[0,100,320,335,500,1000,0]
def D(t):return[(c-60)*2 for c in t]
PA=[0,D(b'<<<<<<<<UUUUUUUUAAFKKFAA>>AHHA>><<<FF<<<>:7<<7:>>AA22AA><<<<<<<<'),
D(b'#(----(#(2<<<<2(-<ADDA<-->DFFD>--<DFFD<-->ADDA>-(2<<<<2(#(----(#'),
D(b'277777727<<<<<<77<>AA><77>>AA>>77<AAAA<77AAAAAA77><<<<>727777772'),
D(b'<<<<<<<<>AAAAAA>:<<<<<<::<<<<<<::<<<<<<::<<<<<<::<<<<<<:<<<<<<<<'),
D(b'277::7727<<<<<<77<>>>><7:<>>>><:<<>>>><:7>>>>><77<><<<<7277::772'),
D(b'-((##((--((##((--((##((-2--((--272222227FF<<<<FFFKA<<AKF<<<<<<<<')]
KE=D(b'#(-22-(#-27<<72--7FKKF7--7KPPK7--7KPPK7--7FKKF7---<<<<--#------#')
TM=[[0]*128 for _ in range(13)]
TE=[[0]*128 for _ in range(13)]
for a in range(1,7):
 for s in(1,-1):
  for sq in range(128):
   if sq&136:continue
   m=sq if s>0 else sq^112
   t=(m>>4)*8+(m&7)
   TM[s*a+6][sq]=s*(V[a]+PA[a][t])
   TE[s*a+6][sq]=s*(V[a]+(KE[t]if a==6 else PA[a][t]))
PH=[0,0,1,1,2,4,0]
KN=(-33,-31,-18,-14,14,18,31,33)
KG=(-17,-16,-15,-1,1,15,16,17)
BD=(-17,-15,15,17)
RD=(-16,-1,1,16)
_r=1234567891011
def R64():
 global _r;_r=(_r*6364136223846793005+1442695040888963407)&18446744073709551615;return _r
Z=[[R64()for _ in range(128)]for _ in range(13)]
ZS=R64();ZC=[R64()for _ in range(16)]
CM={116:3,119:1,112:2,4:12,7:4,0:8}
MATE=100000;INF=10**9;CAP=90000
B=[0]*128;SD=1;CST=0;MG=0;EG=0;PHA=0;KGW=0;KGB=0;H=0;HIST=[];NP=[0,0];BP=[0,0]
TT={};KILL={};PATH=[];NODES=0
class Ab(Exception):pass
def ap(v,sq,d):
 global MG,EG,PHA
 MG+=d*TM[v+6][sq];EG+=d*TE[v+6][sq];PHA+=d*PH[abs(v)]
 if abs(v)>1 and abs(v)<6:NP[0 if v>0 else 1]+=d
 if abs(v)==3:BP[0 if v>0 else 1]+=d
def parse(fen):
 global B,SD,CST,MG,EG,PHA,KGW,KGB,H,HIST,NP,BP
 B=[0]*128;MG=0;EG=0;PHA=0;NP=[0,0];BP=[0,0];HIST=[]
 pt=fen.split();sq=0
 for ch in pt[0]:
  if ch=="/":sq+=8
  elif ch.isdigit():sq+=int(ch)
  else:
   v="pnbrqk".index(ch.lower())+1
   if ch.islower():v=-v
   B[sq]=v;ap(v,sq,1)
   if v==6:KGW=sq
   elif v==-6:KGB=sq
   sq+=1
 SD=1 if len(pt)<2 or pt[1]=="w" else -1
 CST=0
 if len(pt)>2:
  for i,c in enumerate("KQkq"):
   if c in pt[2]:CST|=1<<i
 h=0
 for sq in range(128):
  if not sq&136 and B[sq]:h^=Z[B[sq]+6][sq]
 if SD<0:h^=ZS
 h^=ZC[CST]
 H=h
def atk(sq,by):
 for d in(15,17):
  s=sq+by*d
  if not s&136 and B[s]==by:return 1
 for ds,pv,sl in((KN,2,0),(KG,6,0),(BD,3,1),(RD,4,1)):
  for d in ds:
   s=sq+d
   while not s&136:
    v=B[s]
    if v:
     if v==pv*by or(sl and v==5*by):return 1
     break
    if not sl:break
    s+=d
 return 0
def gen(caps=0):
 ms=[]
 for sq in range(128):
  if sq&136:continue
  v=B[sq]
  if not v or(v>0)!=(SD>0):continue
  a=abs(v)
  if a==1:
   up=-16*SD;tg=[]
   t=sq+up
   if not B[t]:
    if not caps:
     tg.append(t)
     if(sq>>4)==(6 if SD>0 else 1)and not B[sq+2*up]:ms.append(sq|(sq+2*up)<<7)
   for d in(up-1,up+1):
    t=sq+d
    if t&136:continue
    if B[t]and(B[t]>0)!=(SD>0):tg.append(t)
   for t in tg:
    if(t>>4)in(0,7):
     for pr in(5,4,3,2):ms.append(sq|t<<7|pr<<14)
    else:ms.append(sq|t<<7)
  else:
   for d in(KN if a==2 else BD if a==3 else RD if a==4 else KG):
    t=sq+d
    while not t&136:
     tv=B[t]
     if not tv:
      if not caps:ms.append(sq|t<<7)
     else:
      if(tv>0)!=(SD>0):ms.append(sq|t<<7)
      break
     if a==2 or a==6:break
     t+=d
   if a==6:
    for bit,rsq,rp,sg in((1,119,4,1),(2,112,4,-1),(4,7,-4,1),(8,0,-4,-1)):
     ds=sq+2*sg;em=(sq+sg,ds)+((sq-3,)if sg<0 else())
     if sq==(116 if rp>0 else 4)and CST&bit and B[rsq]==rp and not any(B[s]for s in em)and not any(atk(s,-SD)for s in(sq,sq+sg,ds)):ms.append(sq|ds<<7)
 return ms
def rk(f,t,d):
 global H
 rf,rt=(f+3,f+1)if t>f else(f-4,f-1)
 if d<0:rf,rt=rt,rf
 rv=B[rf];ap(rv,rf,-1);H^=Z[rv+6][rf];B[rf]=0;B[rt]=rv;ap(rv,rt,1);H^=Z[rv+6][rt]
def make(m):
 global SD,CST,H,KGW,KGB
 frm=m&127;to=(m>>7)&127;pr=(m>>14)&7
 v=B[frm];cap=B[to]
 HIST.append((m,cap,CST))
 H^=ZC[CST]
 if cap:ap(cap,to,-1);H^=Z[cap+6][to];B[to]=0
 ap(v,frm,-1);H^=Z[v+6][frm];B[frm]=0
 nv=pr*SD if pr else v
 B[to]=nv;ap(nv,to,1);H^=Z[nv+6][to]
 if abs(v)==6:
  if SD>0:KGW=to
  else:KGB=to
  if abs(to-frm)==2:rk(frm,to,1)
 c=CST&~CM.get(frm,0)&~CM.get(to,0)
 CST=c
 H^=ZC[c]
 H^=ZS;SD=-SD
def unmake():
 global SD,CST,H,KGW,KGB
 m,cap,cst=HIST.pop()
 frm=m&127;to=(m>>7)&127;pr=(m>>14)&7
 SD=-SD
 H^=ZS;H^=ZC[CST]
 nv=B[to];v=SD if pr else nv
 ap(nv,to,-1);H^=Z[nv+6][to];B[to]=0;B[frm]=v;ap(v,frm,1);H^=Z[v+6][frm]
 if abs(v)==6:
  if SD>0:KGW=frm
  else:KGB=frm
  if abs(to-frm)==2:rk(frm,to,-1)
 if cap:B[to]=cap;ap(cap,to,1);H^=Z[cap+6][to]
 CST=cst;H^=ZC[cst]
def ev():
 ph=PHA if PHA<=24 else 24
 s=(MG*ph+EG*(24-ph))//24
 if BP[0]==2:s+=30
 if BP[1]==2:s-=30
 return s if SD>0 else -s
def mk(m,ttm,ply=-1):
 if m==ttm:return 10**7
 frm=m&127;to=(m>>7)&127;pr=(m>>14)&7
 cap=B[to]
 if cap:return 10**6+10*V[abs(cap)]-V[abs(B[frm])]
 if pr:return 10**6+V[pr]
 if ply>=0 and m in KILL.get(ply,()):return 500000
 return 0
def legalms(ms):
 for m in ms:
  make(m)
  if atk(KGW if SD<0 else KGB,SD):unmake();continue
  try:yield m
  finally:unmake()
def sr(d,a,b,ply,nullok=1):
 global NODES,H,SD
 if ply>0 and H in PATH:return 0
 NODES+=1
 if NODES>CAP:raise Ab()
 chk=atk(KGW if SD>0 else KGB,-SD)
 if chk:d+=1
 a0=a;ttm=None;best=-INF;bm=None
 if d<=0:
  if not chk:
   best=ev()
   if best>=b:return b
   if best>a:a=best
 else:
  ent=TT.get(H)
  if ent and ply>0:
   ed,fl,esc,ttm=ent
   if ed>=d:
    if fl==0:return esc
    if fl==1:a=max(a,esc)
    elif fl==2:b=min(b,esc)
    if a>=b:return esc
  if nullok and not chk and d>=3 and ply>0 and NP[0 if SD>0 else 1]>0:
   H^=ZS;SD=-SD
   sc=-sr(d-3,-b,-b+1,ply+1,0)
   SD=-SD;H^=ZS
   if sc>=b:return b
 ms=gen(1)if d<=0 and not chk else gen()
 ms.sort(key=lambda m:mk(m,ttm,ply),reverse=True)
 legal=0
 PATH.append(H)
 for m in legalms(ms):
  legal+=1
  cap=HIST[-1][1]
  if legal==1:
   sc=-sr(d-1,-b,-a,ply+1)
  else:
   red=1 if(d>=3 and legal>3 and not cap and not(m>>14) and not chk)else 0
   sc=-sr(d-1-red,-a-1,-a,ply+1)
   if red and sc>a:sc=-sr(d-1,-a-1,-a,ply+1)
   if sc>a and sc<b:sc=-sr(d-1,-b,-a,ply+1)
  if sc>best:best=sc;bm=m
  if sc>a:
   a=sc
   if a>=b:
    if d>0 and not cap:
     kl=KILL.setdefault(ply,[])
     if m not in kl:kl.append(m);del kl[:-2]
    break
 PATH.pop()
 if not legal:return -MATE+ply if chk else best if d<=0 else 0
 if d>0:
  fl=2 if best<=a0 else 1 if best>=b else 0
  TT[H]=(d,fl,best,bm)
 return best
def nm(sq):return "abcdefgh"[sq&7]+str(8-(sq>>4))
def uci(m):
 s=nm(m&127)+nm((m>>7)&127)
 pr=(m>>14)&7
 if pr:s+="nbrq"[pr-2]
 return s
def choose(fen,legal):
 global NODES,PATH
 parse(fen)
 ls=set(legal)
 roots=[m for m in gen()if uci(m)in ls]
 if not roots:return legal[0]
 best=roots[0];NODES=0;d=1
 try:
  while d<=64:
   PATH=[H];a=-INF;cur=best
   ordered=sorted(roots,key=lambda m:mk(m,best),reverse=True)
   for m in legalms(ordered):
    sc=-sr(d-1,-INF,-a,1)
    if sc>a:a=sc;cur=m
   best=cur;roots=ordered
   if NODES>CAP*0.7:break
   d+=1
 except Ab:pass
 return uci(best)
while True:
 g=post("/game",{})
 if g["status"]=="done":break
 TT.clear()
 while g["status"]=="your_move":
  g=post("/move",{"game":g["game"],"move":choose(g["fen"],g["legal_moves"])})
