"""
Phonk (drift) com 808 pesado para shorts de FPS.
Versao 2: bem menos ruidoso, agudos controlados, limiter no lugar de clip.

Saida: audio/phonk_fps.wav  (44.1kHz, estereo, ~27s, loopavel)
Rodar (a partir da pasta BODYCAM):  python phonk_fps.py
"""

import numpy as np
import wave
from scipy.signal import butter, sosfilt

# ----------------------------- CONFIG -----------------------------
SR       = 44100
BPM      = 145
BARS     = 16
SEED     = 7
OUT      = "audio/phonk_fps.wav"

BASS_GAIN   = 1.00     # volume do 808/grave
BASS_DRIVE  = 1.8      # saturacao do 808 (1.2 = limpo, 3+ = agressivo)
HAT_GAIN    = 0.16     # chimbal (baixo de proposito)
COWBELL_GAIN= 0.34
BRIGHTNESS  = 8500     # corte de agudo do master em Hz (menor = mais abafado)
HEADROOM_DB = -3.0     # pico final
# ----------------------------------------------------------------

np.random.seed(SEED)

BEAT  = 60.0 / BPM
STEP  = BEAT / 4.0
STEPS = BARS * 16
DUR   = STEPS * STEP + 1.2
N     = int(DUR * SR)

b_drums = np.zeros(N)
b_808   = np.zeros(N)
b_cow   = np.zeros(N)
b_pad   = np.zeros(N)

# ----------------------------- helpers -----------------------------
def t_arr(dur):
    return np.arange(max(1, int(dur * SR))) / SR

def place(buf, sig, step_global, gain=1.0):
    i = int(round(step_global * STEP * SR))
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * gain

def lp(x, fc, order=4):
    sos = butter(order, min(fc, SR/2 - 100) / (SR/2), btype="low", output="sos")
    return sosfilt(sos, x)

def hp(x, fc, order=2):
    sos = butter(order, max(20, fc) / (SR/2), btype="high", output="sos")
    return sosfilt(sos, x)

def bp(x, f1, f2, order=2):
    sos = butter(order, [max(20, f1) / (SR/2), min(f2, SR/2 - 100) / (SR/2)],
                 btype="band", output="sos")
    return sosfilt(sos, x)

_NAMES = {'C':-9,'C#':-8,'D':-7,'D#':-6,'E':-5,'F':-4,'F#':-3,
          'G':-2,'G#':-1,'A':0,'A#':1,'B':2}
def hz(name):
    n, octv = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((_NAMES[n] + (octv - 4) * 12) / 12)

# ----------------------------- synths -----------------------------
def cowbell(freq, dur=0.20, gain=1.0):
    t = t_arr(dur)
    e = np.exp(-t / 0.10) * (1 - np.exp(-t / 0.003))
    # parciais de seno inharmonicos = metalico sem aspereza de onda quadrada
    sig = (np.sin(2*np.pi*freq*t)        * 0.7 +
           np.sin(2*np.pi*freq*1.48*t)   * 0.5 +
           np.sin(2*np.pi*freq*2.67*t)   * 0.28 +
           np.sin(2*np.pi*freq*3.86*t)   * 0.12)
    sig = np.tanh(sig * 1.1)                 # brilho leve, sem rasgar
    sig = bp(sig * e, freq * 0.7, 5200)
    return sig * gain

def bass808(freq, dur, gain=1.0, drive=BASS_DRIVE):
    t = t_arr(dur)
    pitch = freq * (1 + 0.35 * np.exp(-t / 0.020))
    phase = 2*np.pi * np.cumsum(pitch) / SR
    amp   = np.exp(-t / (dur * 0.45)) * (1 - np.exp(-t / 0.006))
    fund  = np.sin(phase)
    harm  = np.sin(2*phase) * 0.18          # 2o harmonico p/ ouvir em celular
    sat   = np.tanh((fund + harm) * drive) / np.tanh(drive)
    body  = (0.7 * fund + 0.3 * sat) * amp
    body  = lp(body, 240, order=4)          # tira o zumbido, deixa so o peso
    click = np.exp(-t / 0.010) * np.sin(2*np.pi*freq*4*t) * 0.10 * amp
    return (body + click) * gain

def kick(dur=0.36, gain=1.0):
    t = t_arr(dur)
    pitch = 44 + (150 - 44) * np.exp(-t / 0.015)
    phase = 2*np.pi * np.cumsum(pitch) / SR
    amp   = np.exp(-t / 0.10) * (1 - np.exp(-t / 0.001))
    tone  = np.sin(phase) * amp
    click = lp(np.exp(-t / 0.006) * (np.random.rand(len(t)) * 2 - 1), 1800) * 0.5
    out   = np.tanh((tone + click * np.exp(-t / 0.02)) * 1.3)
    return lp(out, 3500) * gain

def snare(dur=0.24, gain=1.0):
    t = t_arr(dur)
    noise = bp(np.random.rand(len(t)) * 2 - 1, 300, 3800, order=2)
    amp   = np.exp(-t / 0.07)
    tone  = (np.sin(2*np.pi*180*t) + 0.6*np.sin(2*np.pi*260*t)) * np.exp(-t / 0.05)
    return (noise * amp * 0.8 + tone * 0.35) * gain

def hat(open_=False, gain=1.0):
    dur = 0.16 if open_ else 0.05
    t = t_arr(dur)
    noise = bp(np.random.rand(len(t)) * 2 - 1, 6500, 11000, order=2)
    amp   = np.exp(-t / (0.055 if open_ else 0.013))
    return noise * amp * gain

def pad(freqs, dur, gain=1.0):
    t = t_arr(dur)
    sig = np.zeros(len(t))
    for f in freqs:
        for det in (0.995, 1.0, 1.005):
            sig += np.sin(2*np.pi * f * det * t + np.random.rand())
    sig /= (len(freqs) * 3)
    atk, rel = 0.7, 1.0
    env = np.minimum(1, t / atk) * np.minimum(1, np.maximum(0, (dur - t) / rel))
    return lp(sig * env, 650) * gain

# ----------------------------- arranjo -----------------------------
BAR_A = {0:'A3', 3:'A3', 6:'C4', 8:'A3', 11:'G3', 14:'A3'}
BAR_B = {0:'A3', 2:'C4', 4:'D4', 6:'C4', 8:'A3', 11:'G3', 14:'E3'}

B808_A = {0:('A1', 8), 8:('A1', 6), 14:('A1', 2)}
B808_B = {0:('A1', 6), 6:('F1', 4), 10:('G1', 6)}

KICK_STEPS  = [0, 6, 8, 11]
SNARE_STEPS = [4, 12]
HAT_STEPS   = [0, 2, 4, 6, 8, 10, 12, 14]   # colcheias, calmo

for bar in range(BARS):
    base = bar * 16
    is_b = (bar % 2 == 1)
    fill = (bar % 8 == 7)
    hype = (bar >= 8)

    mel  = BAR_B if is_b else BAR_A
    bass = B808_B if is_b else B808_A

    for st, note in mel.items():
        place(b_cow, cowbell(hz(note)), base + st,
              gain=COWBELL_GAIN * np.random.uniform(0.9, 1.05))

    for st, (note, ln) in bass.items():
        place(b_808, bass808(hz(note), ln * STEP * 0.98, gain=BASS_GAIN), base + st)

    for st in KICK_STEPS + ([14] if fill else []):
        place(b_drums, kick(), base + st)

    for st in SNARE_STEPS:
        place(b_drums, snare(gain=0.9), base + st)

    hats = HAT_STEPS + ([1, 5, 9, 13] if hype else [])
    for st in hats:
        v = HAT_GAIN * (1.25 if st % 4 == 0 else 0.8)
        place(b_drums, hat(gain=v * np.random.uniform(0.85, 1.1)), base + st)
    place(b_drums, hat(open_=True, gain=HAT_GAIN * 0.9), base + 6)
    if fill:
        for k in range(3):
            place(b_drums, hat(gain=HAT_GAIN * (0.7 + 0.15 * k)), base + 14 + k * 0.66)

    chord = ['A2','C3','E3'] if not is_b else ['F2','A2','C3']
    place(b_pad, pad([hz(c) for c in chord], BEAT * 4 + 0.3, gain=0.9), base)

# ----------------------------- sidechain -----------------------------
ducker = np.ones(N)
sc = t_arr(BEAT * 0.85)
sc_env = 0.6 + 0.4 * (1 - np.exp(-sc / 0.16))
for bar in range(BARS):
    for st in (0, 6, 8):
        i = int(round((bar * 16 + st) * STEP * SR))
        j = min(N, i + len(sc_env))
        ducker[i:j] = np.minimum(ducker[i:j], sc_env[: j - i])

# ----------------------------- mix -----------------------------
mix = (b_drums * 0.55 +
       b_808   * 0.95 +
       (b_cow * 0.7 + b_pad * 0.9) * ducker)

mix = lp(mix, BRIGHTNESS, order=2)          # tira a aspereza do topo
mix = hp(mix, 28, order=2)                  # limpa subgrave inutil

# limiter suave (lookahead simples por envelope)
def limiter(x, ceil=0.9, atk=0.002, rel=0.12):
    env = np.abs(x)
    a = np.exp(-1 / (atk * SR)); r = np.exp(-1 / (rel * SR))
    e = np.zeros_like(env); prev = 0.0
    for i in range(len(env)):
        cur = env[i]
        prev = cur if cur > prev else r * prev + (1 - r) * cur
        e[i] = prev
    gain = np.where(e > ceil, ceil / np.maximum(e, 1e-9), 1.0)
    # suaviza o ganho
    g = np.copy(gain); pg = 1.0
    for i in range(len(g)):
        pg = min(g[i], a * pg + (1 - a) * g[i])
        g[i] = pg
    return x * g

mix = limiter(mix, ceil=0.9)
peak = np.max(np.abs(mix))
mix *= (10 ** (HEADROOM_DB / 20)) / max(peak, 1e-9)

# estereo: grave mono, agudo levemente aberto (delay de ~6ms, nao 1 sample)
d = int(0.006 * SR)
air = hp(mix, 3000, order=2) * 0.35
left  = mix.copy()
right = mix.copy()
left[d:]  += air[:-d]
right[d:] += air[:-d] * -1.0
m = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-9)
scale = (10 ** (HEADROOM_DB / 20)) / m
left *= scale; right *= scale

pcm = np.clip(np.stack([left, right], 1) * 32767, -32768, 32767).astype("<i2")
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())

print(f"OK -> {OUT}  ({DUR:.1f}s, {BPM} BPM, Am)  peak={np.max(np.abs(pcm))/32767:.2f}")
