import argparse,random
p = argparse.ArgumentParser()
p.add_argument('-p',help='pity',type=int,default=0)
p.add_argument('-w',help='wishes',type=int,default=0)
p.add_argument('-e',action='store_true',help='use weapon banner probs')
p.add_argument('-n',help='simulation rounds',type=int,default=100000)
p.add_argument('-g',action='store_true',help='guarantee')
p.add_argument('-c',help='CR counter',type=int,default=1)
p.add_argument('-f',help='five-star probs',type=int,default=0)
args = p.parse_args()

wp,g,cr,t,w,p,n=args.e,args.g,args.c,args.f,args.w,args.p,args.n;z=76 if wp else 90
try:assert p in range(z)
except: print('pity must be between 0 and %s for %s'%(z,'weapon' if wp else 'char'));quit()
try:assert w>=0
except: print('wishes must be non-negative');quit()

fs=lambda s,n,g,cr,wp:1 if not s else 0 if not n else fs(s-1,n-1,0,cr,wp) if g else 0.375*fs(s-1,n-1,0,0,wp)+0.625*fs(s,n-1,1,0,wp) if wp else 0.5*(fs(s-1,n-1,0,max(0,cr-1),wp)+max(0,cr-1)*0.5*fs(s-1,n-1,0,1,wp)+(1-max(0,cr-1)*0.5)*fs(s,n-1,1,cr+1,wp))
pp=lambda p,wp:(0.007 if wp else 0.006) if p<(62 if wp else 74) else min(1,(p-(62 if wp else 73))*(.07 if wp else .06)+(.007 if wp else 0.006))

def prob_calc(s,w,wp):
    p,c=1,[0]
    for i in range(min((76 if wp else 90)-s,w if w else 76 if wp else 90)):z=pp(i+s+1,wp);c[0]+=p*z*(i+1);p*=1-z;c.append(1-p)
    return c

def sim(n,w,s,g,cr,wp):
    p,d=s,{}
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

print('')
if t:
    try: assert t>0
    except: print('number of 5*s must be positive');quit()
    try: assert cr in range(4)
    except: print('CR must be between 0 and 3');quit()
    print('analytic probabilities of target 5* in %s 5*\n\nguarantee:\t%s%s\nbanner:\t\t%s\n\n'%(t,g,'' if wp else '\nCR counter:\t%s'%cr,'weapon' if wp else 'char')+'\n'.join('%s\t\t%s%%'%(i,round(fs(i,t,g,cr,wp)*100,4)) for i in range(t+1)))
elif w:
    print('one-5* analytic probability: %s%%'%round(prob_calc(p,w,wp)[-1]*100,4))
    try:
        assert n and cr in range(4)
        d,e=sim(n,w,p,g,cr,wp)
        print('\n========== SIMULATION ==========\nrounds:\t\t%s\nwishes:\t\t%s\npity:\t\t%s\nguarantee:\t%s%s\nbanner:\t\t%s\n\n'%(n,w,p,g,'' if wp else '\nCR counter:\t%s'%cr,'weapon' if wp else 'char')+'5*s\trounds\t\tprob\t\tave no. of pulls\n'+'\n'.join('%s\t%-10s\t%s%%\t\t%s'%(i,len(d[i]),round(len(d[i])*100/n,4),round(sum(d[i])/len(d[i]),2)) for i in d)+'\n\ntarget 5*\tprob\n'+'\n'.join('%s\t\t%s%%'%(i,round(e[i-1]*100,4)) for i in d))
    except: print('simulation parameters failed validation; no simulation run')
else: 
    ps=prob_calc(p,w,wp)
    print('========== 5* PROBS FROM %s PITY ==========\nexpected num of pulls: %s\n\npulls\t\tprob\n'%(p,ps[0])+'\n'.join('%s\t\t%s%%'%(i+1,round(ps[i+1]*100,4)) for i in range(z)))
print('')
