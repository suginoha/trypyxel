# リバーシを作ってみる

import pyxel
import random
ri = random.randint
pyxel.init(16*12, 16*12, caption = "rev", fps = 60)
pyxel.load("my_resource.pyxres")
pyxel.mouse(True)
flow_no = 0 # 0:title 1:game you 2:com 3:over 
char = [(0,0,16), (16,0,16), (16,16,16), (0,16,16), (32,0,16)]
player_c = "1"
com_c = "2"
mk = -1
bd = "#"*10+"#00000000#"+"#00000000#"+"#00000000#"+"#00012000#"\
+"#00021000#"+"#00000000#"+"#00000000#"+"#00000000#"+"#"*10
w, h = 10, 8
def rev_ps(bd, p, c):
    oc = "12"[c=="1"]
    rp = []
    for d in [-11,-10,-9,-1,1,9,10,11]:
        line = []
        for i in range(1,8):
    	    np = p + d * i
    	    if bd[np]==c:
    	        if line!=[]:rp += line
    	        break
    	    if bd[np]==oc:
    	        line += [np]
    	    else:
    	        break
    return rp
    	
def think(bd, c):
    global mk
    bp = -1
    bbd = bd
    bscore = 0
    for x in range(8):
        for y in range(8):
            p0 = x+1+(y+1)*10
            if bd[p0]!="0":continue
            ps = rev_ps(bd, p0, c)            
            if len(ps)>0:
                nbd = bd
                for p in ps:
                    nbd = nbd[:p] + c + nbd[p+1:]
                nbd = nbd[:p0] + c + nbd[p0+1:]
                score = bd_score(nbd, c)
                if bscore < score:
                    bscore = score
                    bbd = nbd
                    bp = p0
    if bscore == 0:mk = -1#pass
    mk = bp
    return bbd
   
def pass_check(bd, c):
    for x in range(8):
        for y in range(8):
            p0 = x+1+(y+1)*10
            if bd[p0]!="0":continue
            ps = rev_ps(bd, p0, c)            
            if len(ps)>0:
                return False
    return True
	
	
def hit_pos(bd, c):
    r = []
    for x in range(8):
        for y in range(8):
            p0 = x+1+(y+1)*10
            if bd[p0]!="0":continue
            ps = rev_ps(bd, p0, c)            
            if len(ps)>0:
                r += [p0]
    return r	
	
def bd_score(bd, c):
    score = 0
    for p in [11,18,81,88]:
        for d in [-11,-10,-9,-1,1,9,10,11]:
            if bd[p]=="0" and bd[p+d]==c:
            	return 1
            if d in [-10,10,-1,1]:
                for i in range(7):
                    if bd[p+d*i]==c:
                        score += 10
                    else:
                        break
    return bd.count(c) + score
    
	
def put(bd,x,y,c): 
    cx = (x-32)//16
    cy = (y-32)//16
    tn = 0
    if 0<=cx<8 and 0<=cy<8:
        p0 = cx+1+(cy+1)*10
        if bd[p0]!="0":return tn, bd
        ps = rev_ps(bd, p0, c)
        if len(ps)>0:
            for p in ps:
                bd = bd[:p] + c + bd[p+1:]
            bd = bd[:p0] + c + bd[p0+1:]
            tn = 1
    return tn, bd
	
def title():stage();pyxel.text(80, 66, "Rev. four", pyxel.frame_count % 16);pyxel.text(70, 166, "- PRESS ENTER -", 13)
def game_over():stage();pyxel.text(80, 66, "GAME OVER", pyxel.frame_count % 16);pyxel.text(70, 166, "- PRESS ENTER -", 13)
def game_start():
    global flow_no, us, bd, mk, player_c
    player_c = "1"
    mk = -1
    flow_no = 1
    pyxel.playm(0, loop=True)
    bd = "#"*10+"#00000000#"+"#00000000#"+"#00000000#"+"#00012000#"\
+"#00021000#"+"#00000000#"+"#00000000#"+"#00000000#"+"#"*10
def stage():
    global bd, player_c, flow_no
    hp = hit_pos(bd, player_c) if flow_no==1 else []
    for x in range(8):
        for y in range(8):
            cx, cy, sz = char[int(bd[x+1+(y+1)*10])]
            pyxel.blt(x*16+32, y*16+32 , 0, 0, 0, 16, 16, 15)        
            if cx!=0:pyxel.blt(x*16+32, y*16+32 , 0, cx, cy, sz, sz, 0)
            if x+1+(y+1)*10 in hp:
                cx, cy, sz = char[4]
                pyxel.blt(x*16+32, y*16+32 , 0, cx, cy, sz, sz, 0)
    if mk>-1:
        cx, cy, sz = char[3]
        pyxel.blt((mk%10-1)*16+32, (mk//10-1)*16+32 , 0, cx, cy, sz, sz, 15)
    t = []
    for n, c in enumerate("12"):
        t += [bd.count(c)]
        pyxel.text(60, n*12+5, ["you:","com:"][n]+str(bd.count(c)), [8,3][n])
    if sum(t)==64 or t[0]==0 or t[1]==0:flow_no = 3

def update():
    global flow_no,bd,player_c,com_c,mk
    if pyxel.btnp(pyxel.KEY_Q): pyxel.quit()
    if pyxel.btnp(pyxel.KEY_ENTER) and flow_no in [0, 3]:game_start()
    if flow_no == 1:
        if pyxel.btnp(pyxel.KEY_SPACE): pyxel.playm(1, loop=False); flow_no = 3
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            tn, bd = put(bd, pyxel.mouse_x, pyxel.mouse_y, player_c)
            pas = 0
            if tn == 1:
                flow_no = 2
                bd = think(bd, com_c)
                if mk==-1:pas+=1
                if pass_check(bd, player_c):
                    flow_no = 2
                    pas+=1
                else:
                    flow_no = 1
                if pas >= 2:
                    flow_no = 3
        
def draw():
    global flow_no
    pyxel.cls(0)
    if flow_no == 0: title()
    if flow_no in [1,2]: stage()
    if flow_no == 3: game_over()

pyxel.run(update, draw)
