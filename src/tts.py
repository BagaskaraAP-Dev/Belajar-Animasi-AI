import sherpa_onnx, soundfile as sf, sys, json, numpy as np, pyworld as pw
import os
d=os.environ.get('PIPER_MODEL_DIR','models/vits-piper-id_ID-news_tts-medium')
cfg=sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(
    model=f'{d}/id_ID-news_tts-medium.onnx',tokens=f'{d}/tokens.txt',data_dir=f'{d}/espeak-ng-data',
    noise_scale=0.78,noise_scale_w=1.0,length_scale=1.0),num_threads=2))
tts=sherpa_onnx.OfflineTts(cfg)
lines=json.load(open(sys.argv[1])); speed=float(sys.argv[2])
F0_TARGET=float(sys.argv[3]); ALPHA=float(sys.argv[4]); EXPR=float(sys.argv[5])
def warp_env(sp, alpha):
    # lower formants: new(f) = old(f/alpha)... alpha<1 compresses spectrum downward
    n=sp.shape[1]; src=np.arange(n)/alpha
    out=np.empty_like(sp)
    for i in range(sp.shape[0]):
        out[i]=np.interp(src,np.arange(n),sp[i],right=sp[i,-1])
    return out
for k,txt in lines.items():
    a=tts.generate(txt,sid=0,speed=speed)
    x=np.array(a.samples,dtype=np.float64); sr=a.sample_rate
    f0,t=pw.harvest(x,sr,f0_floor=80,f0_ceil=500,frame_period=5)
    sp=pw.cheaptrick(x,f0,t,sr); ap=pw.d4c(x,f0,t,sr)
    v=f0>0; lf=np.log(f0[v]); m=np.median(lf)
    nf=np.zeros_like(f0); nf[v]=np.exp(np.log(F0_TARGET)+(lf-m)*EXPR)
    y=pw.synthesize(nf,warp_env(sp,ALPHA),warp_env(ap,ALPHA),sr,frame_period=5)
    y=y/np.max(np.abs(y))*0.95
    sf.write(f'vo_{k}.wav',y,sr)
    vf=nf[v]
    print(k, round(len(y)/sr,2), 'f0', round(np.median(vf)))
