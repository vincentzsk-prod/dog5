# Polyphase allpass halfband design (Valenzuela & Constantinides; as in L. de Soras' HIIR), verified numerically.
import numpy as np
from math import tan, pi, sin, cos, sqrt
def trans_param(tbw):
    k = tan((1 - tbw * 2) * pi / 4); k *= k
    kk = (1 - k * k) ** 0.25
    e = 0.5 * (1 - kk) / (1 + kk); e2 = e * e; e4 = e2 * e2
    q = e * (1 + e4 * (2 + e4 * (15 + 150 * e4)))
    return k, q
def coefs(n, tbw):
    k, q = trans_param(tbw); order = 2 * n + 1; out = []
    for idx in range(n):
        c = idx + 1
        num = 0; i = 0; j = 1
        while True:
            t = q ** (i * (i + 1)) * sin((2 * i + 1) * c * pi / order) * j
            num += t; j = -j; i += 1
            if abs(t) < 1e-100: break
        den = 0; i = 1; j = -1
        while True:
            t = q ** (i * i) * cos(2 * i * c * pi / order) * j
            den += t; j = -j; i += 1
            if abs(t) < 1e-100: break
        ww = num * q ** 0.25 / (den + 0.5); ws = ww * ww
        x = sqrt((1 - ws * k) * (1 - ws / k)) / (1 + ws)
        out.append((1 - x) / (1 + x))
    return out
def response(c, nf=4096):
    w = np.linspace(0, pi, nf); z1 = np.exp(-1j * w); z2 = z1 * z1
    A0 = np.ones(nf, complex); A1 = np.ones(nf, complex)
    for i, a in enumerate(c):
        ap = (a + z2) / (1 + a * z2)
        if i % 2 == 0: A0 *= ap
        else: A1 *= ap
    return w / (2 * pi), 0.5 * (A0 + z1 * A1)
if __name__ == "__main__":
    for n, tbw in ((4, 0.1), (6, 0.1), (4, 0.15), (3, 0.2), (2, 0.25), (6, 0.05), (8, 0.05)):
        c = coefs(n, tbw); f, H = response(c); m = 20 * np.log10(np.abs(H) + 1e-20)
        sb = m[f >= 0.5 - tbw].max(); pb = m[f <= tbw].min()
        print(f"n={n} tbw={tbw}: stopband max {sb:7.1f} dB, passband min {pb:.4f} dB, coefs {[round(x,6) for x in c]}")
