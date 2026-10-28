"""Learning stack: SML (kNN) + ML scorer + NNL (tiny MLP) + LLM reasoner (offline KB, Gemini if key set).
Pattern carried from shannon-re-lab / bug-bounty-re.
"""
import math, os, random
# SML: kNN
class KNN:
    def __init__(self,k=3): self.k=k; self.X=[]; self.y=[]
    def fit(self,X,y): self.X,self.y=list(X),list(y); return self
    def predict(self,x):
        d=sorted(((math.dist(x,xi),yi) for xi,yi in zip(self.X,self.y)), key=lambda t:t[0])
        votes=[yi for _,yi in d[:self.k]]; return max(set(votes), key=votes.count)
# NNL: tiny MLP, 1 hidden layer, from scratch
class MLP:
    def __init__(self,n_in,n_hidden=6,n_out=1,seed=7):
        r=random.Random(seed); self.W1=[[r.uniform(-.5,.5) for _ in range(n_in)] for _ in range(n_hidden)]
        self.b1=[0.0]*n_hidden; self.W2=[r.uniform(-.5,.5) for _ in range(n_hidden)]; self.b2=0.0
    def _sig(self,z): return 1/(1+math.exp(-z))
    def forward(self,x):
        h=[self._sig(sum(w*xi for w,xi in zip(row,x))+b) for row,b in zip(self.W1,self.b1)]
        return self._sig(sum(w*hi for w,hi in zip(self.W2,h))+self.b2), h
    def train(self,X,y,epochs=200,lr=0.3):
        for _ in range(epochs):
            for xi, yi in zip(X,y):
                out,h=self.forward(xi); err=out-yi
                for j in range(len(self.W2)):
                    g=err*out*(1-out)*h[j]; self.W2[j]-=lr*g
                self.b2-=lr*err*out*(1-out)
        return self
    def predict(self,x): return self.forward(x)[0]
# LLM reasoner: deterministic offline, Gemini only if GEMINI_API_KEY is set
KB = [
 ("delegatecall proxy upgrade", "DELEGATECALL usually means a proxy. RE the implementation contract, not just the proxy, and check who can upgrade."),
 ("aave lending", "For Aave-style markets on Monad: map pool, reserve configs and liquidation thresholds before simulating positions."),
 ("unlock cliff november 2026", "The 16.6B MON cliff unlock on 2026-11-24 is a supply event: model circulating-supply shock in any MON risk score."),
 ("high entropy bytecode", "High entropy suggests packed/obfuscated bytecode: disassemble, extract selectors, and compare against known protocol fingerprints."),
]
def reason(query):
    q=query.lower(); hits=[v for k,v in KB if any(w in q for w in k.split())]
    if os.environ.get("GEMINI_API_KEY"): return {"mode":"gemini-configured (offline KB shown)","answers":hits or ["No KB hit - queue as a new experiment."]}
    return {"mode":"offline","answers":hits or ["No KB hit - queue as a new experiment."]}
