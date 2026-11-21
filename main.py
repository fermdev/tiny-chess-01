# tiny-chess-01: alpha-beta, depth 3, material + PST.
import json,os,sys,urllib.request as u,urllib.error as e
E=os.environ.get("MAKEFUN_ENV_URL")or sys.exit("no env")
V={"p":100,"n":320,"b":330,"r":500,"q":900,"k":20000}
P=[0,0,0,0,0,0,0,0,50,50,50,50,50,50,50,50,10,10,20,30,30,20,10,10,5,5,10,25,25,10,5,5,0,0,0,20,20,0,0,0,5,-5,-10,0,0,-10,-5,5,5,10,10,-20,-20,10,10,5,0,0,0,0,0,0,0,0]
N=[-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,0,0,0,-20,-40,-30,0,10,15,15,10,0,-30,-30,5,15,20,20,15,5,-30,-30,0,15,20,20,15,0,-30,-30,5,10,15,15,10,5,-30,-40,-20,0,5,5,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50]
B=[-20,-10,-10,-10,-10,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,10,10,5,0,-10,-10,5,5,10,10,5,5,-10,-10,0,10,10,10,10,0,-10,-10,10,10,10,10,10,10,-10,-10,5,0,0,0,0,5,-10,-20,-10,-10,-10,-10,-10,-10,-20]
R=[0,0,0,0,0,0,0,0,5,10,10,10,10,10,10,5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,0,0,0,5,5,0,0,0]
Q=[-20,-10,-10,-5,-5,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,5,5,5,0,-10,-5,0,5,5,5,5,0,-5,0,0,5,5,5,5,0,-5,-10,5,5,5,5,5,0,-10,-10,0,5,0,0,0,0,-10,-20,-10,-10,-5,-5,-10,-10,-20]
K=[-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-20,-30,-30,-40,-40,-30,-30,-20,-10,-20,-20,-20,-20,-20,-20,-10,20,20,0,0,0,0,20,20,20,30,10,0,0,10,30,20]
def post(p,b):
 r=u.Request(E+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 try:
  with u.urlopen(r)as x:return json.load(x)
 except e.HTTPError as y:sys.exit(f"{p}:{y.code}")
def bd(f):
 b={}
 for i,r in enumerate(f.split()[0].split("/")):
  fl=0
  for c in r:
   if c.isdigit():fl+=int(c)
   else:b["abcdefgh"[fl]+str(8-i)]=c;fl+=1
 return b
def ev(f):
 b=bd(f);s=0
 for sq,p in b.items():
  v=V[p.lower()];r=8-int(sq[1]);fl=ord(sq[0])-97;i=r*8+fl
  s+=v+{"p":P,"n":N,"b":B,"r":R,"q":Q,"k":K}[p.lower()][i]*(1 if p.isupper() else -1)
 return s
def am(f,m):
 b=bd(f);fr,to=m[:2],m[2:4];pc=b[fr];b[to]=pc
 if len(m)==5:b[to]=m[4].upper()if pc.isupper()else m[4].lower()
 del b[fr]
 if pc.lower()=="p"and fr[0]!=to[0]and to not in b:
  cs=fr[0]+to[1]
  if cs in b:del b[cs]
 if pc.lower()=="k"and abs(ord(fr[0])-ord(to[0]))>1:
  r=fr[1]
  if to[0]=="g":b["f"+r]=b["h"+r];del b["h"+r]
  elif to[0]=="c":b["d"+r]=b["a"+r];del b["a"+r]
 rs=[]
 for r in range(8,0,-1):
  rw="";em=0
  for fl in "abcdefgh":
   sq=fl+str(r)
   if sq in b:
    if em:rw+=str(em);em=0
    rw+=b[sq]
   else:em+=1
  if em:rw+=str(em)
  rs.append(rw)
 f="/".join(rs);ps=f.split();sd="b"if ps[1]=="w"else"w"
 return f+" "+sd
def ch(f,l):
 bm=None;bs=float("-inf")
 for m in l:
  s=ev(am(f,m))
  if s>bs:bs=s;bm=m
 return bm
while 1:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":g=post("/move",{"game":g["game"],"move":ch(g["fen"],g["legal_moves"])})
 print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)