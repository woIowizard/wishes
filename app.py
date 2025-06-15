import flask,random
app = flask.Flask(__name__)
fs=lambda s,n,g,cr,wp:1 if not s else 0 if not n else fs(s-1,n-1,0,cr,wp) if g else 0.375*fs(s-1,n-1,0,0,wp)+0.625*fs(s,n-1,1,0,wp) if wp else 0.5*(fs(s-1,n-1,0,max(0,cr-1),wp)+max(0,cr-1)*0.5*fs(s-1,n-1,0,1,wp)+(1-max(0,cr-1)*0.5)*fs(s,n-1,1,cr+1,wp))
pp=lambda p,wp:(0.007 if wp else 0.006) if p<(62 if wp else 74) else min(1,(p-(62 if wp else 73))*(.07 if wp else .06)+(.007 if wp else 0.006))

def prob_calc(s,w,wp):
    p,c=1,[0]
    for i in range(min((76 if wp else 90)-s,w if w else 76 if wp else 90)):z=pp(i+s+1,wp);c[0]+=p*z*(i+1);p*=1-z;c.append(1-p)
    return c

def sim(n,w,s,g,cr,wp):
    p,d,c=s,{},''
    for _ in range(n):
        s,f=p,0
        for i in range(w):
            if random.random()<pp(s+1,wp):
                s,f=0,f+1
                if f in d: d[f].append(i+1)
                else: d[f]=[i+1]
            else: s+=1
    e=[0]*len(d)
    for i in d:
        for j in range(i): e[j]+=fs(j+1,i,g,cr,wp)*(len(d[i])-(0 if i==len(d) else len(d[i+1])))/n
    return (d,e)

@app.route('/',methods=['GET','POST'])
def home():
    r = flask.request
    if r.method == 'GET': return flask.render_template('main.html',p=0,w=0,s=0,n=10000,g=0,v=0,t=10,wp=0,cr=1)
    elif r.method == 'POST':
        p,w,n,g,v,t,wp,cr = r.form['pity'],r.form['wishes'],r.form['rounds'],'guarantee' in r.form,'fivestar' in r.form,r.form['stars'],'weapon' in r.form,r.form['cr']
        c = flask.render_template('main.html',p=p,w=w,n=n,g=g,v=v,t=t,wp=wp,cr=cr)
        try: p=int(p);assert p in range(76 if wp else 90)
        except: return c+'pity must be between 0 and %s for %s'%(76 if wp else 90,'weapon' if wp else 'char')
        try: w=int(w);assert w>=0
        except: return c+'wishes must be non-negative'
        if v:
            try: t=int(t);assert t>0
            except: return c+'number of 5*s must be positive'
            try: cr=int(cr);assert cr in range(4)
            except: return c+'CR must be between 0 and 3'
            c += flask.render_template('fs_sim.html',t=t,g=g,wp=wp,cr=cr,f=[fs(i,t,g,cr,wp) for i in range(t+1)])
        elif w:
            c += '<br><b>one-5* analytic probability: </b>%s%%<br><br>'%prob_calc(p,w,wp)[-1]
            try:
                n=int(n);cr=int(cr);assert n and cr in range(0,4);d,e=sim(n,w,p,g,cr,wp)
                c += flask.render_template('sim_res.html',n=n,w=w,p=p,wp=wp,cr=cr,g=g,d=d,e=e)
            except: pass
        else: c += flask.render_template('pr_list.html',p=p,ps=prob_calc(p,w,wp))
        return c
    return 'something went wrong' 

if __name__ == '__main__':
    app.run()
