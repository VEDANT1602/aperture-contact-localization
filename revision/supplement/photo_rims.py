"""Sample real optical inner-rim crossings in the Calibration.zip ring-board series."""

import argparse
import csv
import hashlib
import io
import zipfile
from pathlib import Path
import numpy as np
from PIL import Image
from contact_budgets import D, known_fit, conic_fit
from run import chord_map

OUT = Path(__file__).resolve().parent
SHA = "a41f0566347036aec88cd3e58e3fcd029850bdfc912038654259bf3af2b25c7f"


def sample(im, xy):
    x, y = xy.T
    if (
        np.any(x < 0)
        | np.any(y < 0)
        | np.any(x >= im.shape[1] - 1)
        | np.any(y >= im.shape[0] - 1)
    ):
        raise ValueError("outside photo")
    ix = x.astype(int)
    iy = y.astype(int)
    dx = x - ix
    dy = y - iy
    return (
        im[iy, ix] * (1 - dx) * (1 - dy)
        + im[iy, ix + 1] * dx * (1 - dy)
        + im[iy + 1, ix] * (1 - dx) * dy
        + im[iy + 1, ix + 1] * dx * dy
    )


def hits(image, origin, u, cut, radius):
    result = []
    for sign in (-1, 1):
        d = np.arange(0, 1.65 * radius, 0.2)
        ray = origin + (sign * d)[:, None] * u
        values = sample(image, ray)
        ids = np.flatnonzero(values < cut)
        if not len(ids) or ids[0] == 0:
            raise ValueError("no light-to-dark crossing")
        j = ids[0]
        f = (values[j - 1] - cut) / (values[j - 1] - values[j])
        result.append(origin + sign * (d[j - 1] + f * (d[j] - d[j - 1])) * u)
    return np.array(result)


def image_rows(im, gt, label):
    ctr = gt[:, :2]
    a = gt[:, 2]
    rows = []
    for i, (cx, cy, maj, small, theta) in enumerate(gt):
        # Inner edge must have a companion outer annotation around the same center.
        if not np.any((np.linalg.norm(ctr - ctr[i], axis=1) <= 3) & (a > 1.3 * maj)):
            continue
        c = np.array([cx, cy])
        rad = int(np.ceil(1.6 * maj))
        cx0, cy0 = np.rint(c).astype(int)
        crop = im[max(0, cy0 - rad) : cy0 + rad + 1, max(0, cx0 - rad) : cx0 + rad + 1]
        cut = np.mean(np.percentile(crop, [10, 90]))
        origin = c + small * np.array([0.28, -0.32])
        cos, sin = np.cos(theta), np.sin(theta)
        rot = np.array([[cos, -sin], [sin, cos]])
        q = rot @ np.diag([maj**-2, small**-2]) @ rot.T
        preds = {}
        try:
            a0 = hits(im, origin, D[0], cut, maj)
            b0 = hits(im, origin, D[1], cut, maj)
            mid = np.array([a0[:, 0].mean(), b0[:, 1].mean()])
            pts = np.concatenate([a0, b0])
            preds["independent_4"] = mid
            preds["coupled_4"] = origin + np.linalg.solve(chord_map(q), mid - origin)
            preds["prior_LS_4"] = known_fit(pts, q)
            third = hits(im, mid, D[2], cut, maj)
            for k in (5, 6):
                preds[f"free_LS_{k}"] = conic_fit(np.vstack([pts, third])[:k])
        except (ValueError, np.linalg.LinAlgError):
            pass
        for method in (
            "independent_4",
            "coupled_4",
            "prior_LS_4",
            "free_LS_5",
            "free_LS_6",
        ):
            err = np.linalg.norm(preds[method] - c) if method in preds else None
            rows.append(
                dict(
                    image=label,
                    rim=i,
                    method=method,
                    available=int(err is not None),
                    center_error_px=err if err is not None else "",
                )
            )
    return rows


def main(path):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SHA:
        raise ValueError("unexpected image archive checksum")
    rows = []
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for name in sorted(
            n for n in z.namelist() if "/images/ring" in n and n.endswith(".jpg")
        ):
            stem = name.split("/")[-1]
            im = np.array(
                Image.open(io.BytesIO(z.read(name))).convert("L"), dtype=float
            )
            gt = np.loadtxt(
                io.BytesIO(z.read("Calibration/gt/gt_" + stem + ".txt")), skiprows=1
            )
            rows.extend(image_rows(im, gt, stem))
    # Aggregate by image to expose clustering; do not weight projections as independent trials.
    result = []
    for image in sorted({r["image"] for r in rows}):
        for method in (
            "independent_4",
            "coupled_4",
            "prior_LS_4",
            "free_LS_5",
            "free_LS_6",
        ):
            block = [r for r in rows if r["image"] == image and r["method"] == method]
            e = [r["center_error_px"] for r in block if r["available"]]
            result.append(
                dict(
                    image=image,
                    method=method,
                    eligible=len(block),
                    valid=len(e),
                    median_error_px=np.median(e) if e else "",
                    p90_error_px=np.quantile(e, 0.9) if e else "",
                )
            )
    for name, records in [("photo_results.csv", result), ("photo_rims.csv", rows)]:
        with (OUT / name).open("w", newline="") as f:
            out = csv.DictWriter(f, fieldnames=records[0])
            out.writeheader()
            out.writerows(records)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("zipfile", type=Path)
    main(p.parse_args().zipfile)
