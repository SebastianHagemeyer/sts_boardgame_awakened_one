import numpy as np
from PIL import Image
def rgb2hsv(a):
    r,g,b=a[...,0],a[...,1],a[...,2]
    mx=a.max(-1); mn=a.min(-1); d=mx-mn
    h=np.zeros_like(mx)
    m=d>1e-6
    rc=np.where(m,(mx-r)/np.where(m,d,1),0); gc=np.where(m,(mx-g)/np.where(m,d,1),0); bc=np.where(m,(mx-b)/np.where(m,d,1),0)
    h=np.where(r==mx,bc-gc,np.where(g==mx,2+rc-bc,4+gc-rc))
    h=(h/6)%1; h=np.where(m,h,0)
    s=np.where(mx>0,d/np.where(mx>0,mx,1),0)
    return h,s,mx
def hsv2rgb(h,s,v):
    i=np.floor(h*6).astype(int)%6; f=h*6-np.floor(h*6)
    p=v*(1-s); q=v*(1-s*f); t=v*(1-s*(1-f))
    r=np.choose(i,[v,q,p,p,t,v]); g=np.choose(i,[t,v,v,q,p,p]); b=np.choose(i,[p,p,t,v,v,q])
    return np.stack([r,g,b],-1)
GEM=[(92,46),(152,100),(152,152),(110,182),(58,174),(31,120)]
def awaken(im, orb_box=None, frame_hue=234, orb_hue=268, gem=False):
    a=np.asarray(im.convert('RGBA')).astype(np.float64)/255
    rgb=a[...,:3]; h,s,v=rgb2hsv(rgb)
    H,W=h.shape; yy,xx=np.mgrid[0:H,0:W]
    if gem:
        from PIL import ImageDraw
        mk=Image.new('L',im.size,0); ImageDraw.Draw(mk).polygon(GEM,fill=255); inorb=np.asarray(mk)>0
    elif orb_box is None:
        inorb=np.zeros(a.shape[:2],bool)
    else:
      cx=(orb_box[0]+orb_box[2])/2; cy=(orb_box[1]+orb_box[3])/2; rx=(orb_box[2]-orb_box[0])/2; ry=(orb_box[3]-orb_box[1])/2
      inorb=((xx-cx)/rx)**2+((yy-cy)/ry)**2<=1
    hd=h*360
    purple=(hd>255)&(hd<345)&(s>0.18)
    # frame body -> slate lavender
    fm=purple&~inorb
    h2=np.where(fm,frame_hue/360,h); s2=np.where(fm,s*0.55,s); v2=np.where(fm,np.clip(v*0.92,0,1),v)
    # orb -> violet
    om=purple&inorb
    h2=np.where(om,orb_hue/360,h2); s2=np.where(om,np.clip(s*0.95,0,1),s2)
    # dark text panel (low-sat purple-grey) -> VG slate panel
    pm=(hd>220)&(hd<300)&(s<=0.35)&(s>0.05)&(v<0.45)&~inorb
    h2=np.where(pm,frame_hue/360,h2); s2=np.where(pm,np.clip(s*1.5,0,0.36),s2); v2=np.where(pm,np.clip(v*1.35,0,1),v2)
    out=hsv2rgb(h2,s2,v2)
    res=np.concatenate([out,a[...,3:]],-1)
    return Image.fromarray((res*255+0.5).astype(np.uint8),'RGBA')
