import numpy as np, wave, sys, os, subprocess
from scenes import SFX, T_END, T_B, T_C1
SR=44100; N=int(T_END*SR); out=np.zeros(N)
rng=np.random.default_rng(1)
def add(sig,t,g=1.0):
    i=int(t*SR); j=min(N,i+len(sig))
    if i<N: out[i:j]+=sig[:j-i]*g
def env(n,a=0.005,d=0.3):
    t=np.arange(n)/SR; return np.minimum(t/a,1)*np.exp(-t/d)
def lp(x,k=0.15):
    y=np.zeros_like(x); acc=0
    for i in range(len(x)): acc+=k*(x[i]-acc); y[i]=acc
    return y
def nf(m): return 440*2**((m-69)/12)
BPM=100; beat=60/BPM; bar=4*beat
chords=[[53,57,60,64],[55,59,62,65],[52,55,59,62],[57,60,64,67]]  # Fmaj7 G7 Em7 Am7
roots=[41,43,40,45]
nb=int(T_END/bar)+1
for b in range(nb):
    t0=b*bar; ch=chords[b%4]
    n=int(bar*SR); tt=np.arange(n)/SR
    pad=sum(np.sin(2*np.pi*nf(m)*tt)+0.4*np.sin(2*np.pi*nf(m)*1.003*tt) for m in ch)
    pad*=np.minimum(tt/0.3,1)*np.minimum((bar-tt)/0.3,1)
    add(pad,t0,0.035)
    for k in (0,2):
        nn=int(beat*1.8*SR); t2=np.arange(nn)/SR
        bs=(np.sin(2*np.pi*nf(roots[b%4])*t2)+0.3*np.sin(4*np.pi*nf(roots[b%4])*t2))*env(nn,0.01,0.5)
        add(bs,t0+k*beat,0.22 if t0>=T_B-0.1 else 0.12)
    # drums
    for k in range(4):
        tb=t0+k*beat
        if tb<T_B-0.6 and k%2: pass
        nn=int(0.4*SR); t2=np.arange(nn)/SR
        if k in (0,2) and tb>=2.4:
            f=45+90*np.exp(-t2*30); kick=np.sin(2*np.pi*np.cumsum(f)/SR)*env(nn,0.002,0.18)
            add(kick,tb,0.55 if tb>=T_B else 0.3)
        if k in (1,3) and tb>=T_B:
            sn=lp(rng.standard_normal(nn),0.5)*env(nn,0.001,0.09)+0.4*np.sin(2*np.pi*190*t2)*env(nn,0.001,0.06)
            add(sn,tb,0.22)
        for h in (0,0.5):
            th=tb+h*beat
            if th>=2.4:
                nh=int(0.06*SR); x=rng.standard_normal(nh); x=x-lp(x,0.3)
                add(x*env(nh,0.001,0.02),th,0.07 if th>=T_B else 0.04)
    # pluck arps on weekend
    if t0>=T_B-0.1:
        seq=[ch[0]+12,ch[2]+12,ch[1]+12,ch[3]+12,ch[2]+12,ch[1]+12,ch[3]+12,ch[2]+24]
        for k,m in enumerate(seq):
            nn=int(0.4*SR); t2=np.arange(nn)/SR
            ph=(t2*nf(m))%1; tri=2*np.abs(2*ph-1)-1
            add(tri*env(nn,0.003,0.15),t0+k*beat/2,0.06)
# sfx
def sfx(kind):
    if kind=='pop':
        n=int(0.12*SR); t=np.arange(n)/SR; f=500+1400*t/0.12
        return np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,0.002,0.04)*0.5
    if kind=='alert':
        n=int(0.35*SR); t=np.arange(n)/SR; f=np.where(t<0.15,880,1175)
        return np.sign(np.sin(2*np.pi*np.cumsum(f)/SR))*0.12*(np.where(t<0.15,env(n,0.002,0.08),np.roll(env(n,0.002,0.1),int(0.17*SR))))
    if kind=='close':
        n=int(0.3*SR); t=np.arange(n)/SR
        return (np.sin(2*np.pi*120*t)+lp(rng.standard_normal(n),0.2))*env(n,0.001,0.06)*0.6
    if kind=='whoosh':
        n=int(0.6*SR); t=np.arange(n)/SR; x=lp(rng.standard_normal(n),0.08)
        return x*np.sin(np.pi*t/0.6)**2*1.6
    if kind=='scare':
        n=int(0.9*SR); t=np.arange(n)/SR
        return (np.sin(2*np.pi*55*t)*0.8+lp(rng.standard_normal(n),0.4)*0.6)*env(n,0.002,0.3)
    if kind=='ding':
        n=int(1.2*SR); t=np.arange(n)/SR
        return (np.sin(2*np.pi*1318*t)+0.5*np.sin(2*np.pi*2637*t)+0.3*np.sin(2*np.pi*1975*t))*env(n,0.002,0.35)*0.3
    if kind=='boom':
        n=int(0.8*SR); x=lp(rng.standard_normal(n),0.05)
        return x*env(n,0.002,0.25)*1.2
for kind,t in SFX: add(sfx(kind),max(0,t))
# voiceover (dipasang mulai detik 0) + music ducking
import soundfile as sf
VO_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'voiceover', 'voiceover.wav')
OUT_WAV = sys.argv[2] if len(sys.argv) > 2 else 'audio.wav'
tmp = OUT_WAV + '.vo.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', VO_PATH, '-af',
                'highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=100:makeup=1.5',
                '-ar', str(SR), '-ac', '1', tmp], check=True)
x, sr = sf.read(tmp)
os.remove(tmp)
if x.ndim > 1: x = x[:, 0]
x = x / np.max(np.abs(x))
vo = np.zeros(N); n = min(N, len(x)); vo[:n] = x[:n]
e = np.abs(vo); k = int(0.15 * SR)
e = np.convolve(e, np.ones(k) / k, mode='same'); e = np.clip(e / 0.08, 0, 1)
out = out / np.max(np.abs(out)) * 0.6 * (1 - 0.5 * e) + vo * 0.85
# fade out
fo=int(1.5*SR); out[-fo:]*=np.linspace(1,0,fo)
out/=np.max(np.abs(out))/0.89
pcm=(np.stack([out,out],1)*32767).astype(np.int16)
w=wave.open(OUT_WAV,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
