"""Reproduce the tactile chord experiment. Requires Python 3.10+ and NumPy."""
import csv
from pathlib import Path
import numpy as np


HERE = Path(__file__).resolve().parent
N = 2000


def metric(a, b, deg):
    t = np.deg2rad(deg)
    r = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
    return r @ np.diag([a**-2, b**-2]) @ r.T


def chords(center, q, noise):
    # Intersect each equation (x-c)'Q(x-c)=1 with a world-coordinate axis.
    h = np.einsum("ni,ij,nj->n", center, q, center) - 1.
    linear = center @ q
    mid = linear / q.diagonal()
    disc = mid**2 - h[:,None] / q.diagonal()
    half = np.sqrt(np.maximum(0., disc))
    roots = np.stack([mid-half,mid+half], axis=2)
    valid = (disc>=0) & (np.max(np.abs(roots),axis=2)<=12.)
    return (roots + noise).mean(axis=2), valid


def observation_matrix(q):
    return q / q.diagonal()[:, None]


def main():
    rng = np.random.default_rng(1707)
    rows = []
    for radius in [0.5,2.5,4.5,6.5]:
        angles = rng.uniform(-np.pi,np.pi,N)
        radii = radius*np.sqrt(rng.uniform(0,1,N))
        center = np.column_stack([np.cos(angles),np.sin(angles)])*radii[:,None]
        noise = rng.normal(0,.12,(N,2,2))
        tracking = rng.normal(0,.06,(N,2))
        for shape,a,b,deg in [("round",5.,5.,0.),("oval",7.,3.5,35.)]:
            q=metric(a,b,deg)
            mids,ok=chords(center,q,noise)
            exact,exact_ok=chords(center,q,0.*noise)
            A=observation_matrix(q)
            x_shift=np.column_stack([mids[:,0],np.zeros(N)])
            second,second_ok=chords(center-x_shift,q,noise)
            adaptive=np.column_stack([mids[:,0],second[:,1]])
            solved=np.linalg.solve(A,exact.T).T
            good=np.all(exact_ok,axis=1)
            assert np.max(np.abs(solved[good]-center[good]))<2e-12
            for mu in [.12,.55]:
                alternatives=[
                    ("direct",np.zeros_like(center), np.ones(N,bool),0),
                    ("x_only",np.column_stack([mids[:,0],np.zeros(N)]),ok[:,0],2),
                    ("midpoints",mids,ok.all(axis=1),4),
                    ("recenter",adaptive,ok[:,0]&second_ok[:,1],4),
                    ("cad",np.linalg.solve(A,mids.T).T,ok.all(axis=1),4),
                    ("cad_plus15",np.linalg.solve(observation_matrix(metric(a,b,deg+15.)),mids.T).T,ok.all(axis=1),4)
                ]
                ref=None
                for method,est,visible,touches in alternatives:
                    residual=est+tracking-center
                    norm=np.linalg.norm(residual,axis=1)
                    rho=np.sqrt(np.einsum("ni,ij,nj->n",residual,q,residual))
                    outward_mm=norm*np.maximum(0.,1.-.08/np.maximum(1e-15,rho))
                    elapsed=touches*.22 + np.where(visible,.42+np.linalg.norm(est,axis=1)/30.,0.)
                    insert=visible & (elapsed<=1.8)
                    seated=insert & ((rho<=.08) | ((rho<=.18) & (mu<.35)))
                    load=np.maximum(.75 if touches else 0.,np.where(insert,np.minimum(5.,.65+1.4*outward_mm),0.))
                    if method=="midpoints": ref=seated.copy()
                    paired=ref if ref is not None else seated
                    rows.append(dict(radius_mm=radius,shape=shape,mu=mu,method=method,trials=N,
                        observable=int(visible.sum()),attempted=int(insert.sum()),successful=int(seated.sum()),
                        mean_cycle_s=round(np.minimum(1.8,elapsed).mean(),6),
                        mean_peak_N=round(load.mean(),6),p95_peak_N=round(np.quantile(load,.95),6),
                        mean_est_error_mm=round(np.linalg.norm(est[visible]-center[visible],axis=1).mean(),6),
                        gains_vs_midpoint=int(np.sum(seated & ~paired)) if ref is not None else "",
                        losses_vs_midpoint=int(np.sum(paired & ~seated)) if ref is not None else ""))
    with (HERE/"results.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print(len(rows),"condition-policy rows written.")


if __name__=="__main__":
    main()
