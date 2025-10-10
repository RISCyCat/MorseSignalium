#!/usr/bin/env python3
# morse_gui_audio.py
# Morse encoder/decoder with GUI (tkinter) + audio playback using numpy + simpleaudio
# Requires: numpy, simpleaudio

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import numpy as np
import simpleaudio as sa

MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ',': '--..--', '.': '.-.-.-', '?': '..--..', '!': '-.-.--', '/': '-..-.',
    '-': '-....-', '(':'-.--.', ')':'-.--.-'
}
MORSE_TO_TEXT = {v: k for k, v in MORSE_CODE.items()}

# Audio generation helpers
def generate_tone(frequency=600, duration_ms=100, sample_rate=44100, volume=0.3):
    t = np.linspace(0, duration_ms / 1000.0, int(sample_rate * duration_ms / 1000.0), False)
    tone = np.sin(frequency * 2 * np.pi * t)
    audio = tone * volume
    # convert to 16-bit pcm
    audio_int16 = np.int16(audio * 32767)
    return audio_int16

def play_wave(audio_int16, sample_rate=44100):
    play_obj = sa.play_buffer(audio_int16, 1, 2, sample_rate)
    return play_obj  # play_obj.wait_done() to block

# Morse conversion
def text_to_morse(text: str) -> str:
    parts = []
    for ch in text.upper():
        if ch == ' ':
            parts.append('')  # produce double space -> becomes 3 after join
        else:
            parts.append(MORSE_CODE.get(ch, '?'))
    return ' '.join(parts).replace('  ', '   ')

def morse_to_text(morse: str) -> str:
    words = morse.strip().split('   ')
    decoded = []
    for w in words:
        if not w:
            continue
        letters = w.split()
        decoded.append(''.join(MORSE_TO_TEXT.get(l, '?') for l in letters))
    return ' '.join(decoded)

# Playback controller
class MorsePlayer:
    def __init__(self):
        self._stop_event = threading.Event()
        self._thread = None

    def stop(self):
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=0.5)
        self._thread = None
        self._stop_event.clear()

    def play(self, morse_string, wpm=20, freq=600):
        if self._thread and self._thread.is_alive():
            # stop current
            self.stop()
        self._thread = threading.Thread(target=self._play_thread, args=(morse_string, wpm, freq), daemon=True)
        self._thread.start()

    def _play_thread(self, morse_string, wpm, freq):
        # unit (dot) in ms: 1200 / wpm (PARIS standard)
        unit_ms = 1200.0 / max(1, float(wpm))
        sample_rate = 44100
        dot_audio = generate_tone(frequency=freq, duration_ms=unit_ms, sample_rate=sample_rate)
        dash_audio = generate_tone(frequency=freq, duration_ms=unit_ms * 3, sample_rate=sample_rate)
        intra_symbol_gap = int(unit_ms / 1000.0 * sample_rate)  # not used directly here, we use time.sleep

        # Normalize morse string (letters separated by single space, words by 3 spaces)
        morse = morse_string.strip()
        if not morse:
            return
        try:
            for wi, word in enumerate(morse.split('   ')):
                if self._stop_event.is_set(): return
                letters = word.split()
                for li, letter in enumerate(letters):
                    if self._stop_event.is_set(): return
                    for si, sym in enumerate(letter):
                        if self._stop_event.is_set(): return
                        if sym == '.':
                            play_obj = play_wave(dot_audio, sample_rate)
                            play_obj.wait_done()
                        elif sym == '-':
                            play_obj = play_wave(dash_audio, sample_rate)
                            play_obj.wait_done()
                        else:
                            # unknown symbol -> short pause
                            time.sleep(unit_ms / 1000.0)
                        # intra-symbol gap = 1 unit
                        time.sleep(unit_ms / 1000.0)
                    # after a letter: gap total 3 units; we already waited 1 after last symbol => wait 2 more
                    time.sleep((unit_ms * 2) / 1000.0)
                # after word: total 7 units; we already waited 3 between letters -> wait 4 more units
                time.sleep((unit_ms * 4) / 1000.0)
        except Exception as e:
            print("Playback error:", e)

player = MorsePlayer()

# GUI
def do_encode():
    txt = txt_input.get("1.0", tk.END).strip()
    if not txt:
        messagebox.showinfo("Info", "Introdu text pentru criptare.")
        return
    out = text_to_morse(txt)
    txt_output.config(state=tk.NORMAL)
    txt_output.delete("1.0", tk.END)
    txt_output.insert(tk.END, out)
    txt_output.config(state=tk.DISABLED)

def do_decode():
    txt = txt_input.get("1.0", tk.END).strip()
    if not txt:
        messagebox.showinfo("Info", "Introdu cod Morse pentru decriptare.")
        return
    out = morse_to_text(txt)
    txt_output.config(state=tk.NORMAL)
    txt_output.delete("1.0", tk.END)
    txt_output.insert(tk.END, out)
    txt_output.config(state=tk.DISABLED)

def do_swap():
    a = txt_input.get("1.0", tk.END)
    b = txt_output.get("1.0", tk.END)
    txt_input.delete("1.0", tk.END)
    txt_input.insert(tk.END, b)
    txt_output.config(state=tk.NORMAL)
    txt_output.delete("1.0", tk.END)
    txt_output.insert(tk.END, a)
    txt_output.config(state=tk.DISABLED)

def do_play():
    morse = txt_output.get("1.0", tk.END).strip()
    if not morse:
        # try auto-encode input
        src = txt_input.get("1.0", tk.END).strip()
        if not src:
            messagebox.showinfo("Info", "Nu există text sau cod Morse pentru redare.")
            return
        morse = text_to_morse(src)
        txt_output.config(state=tk.NORMAL)
        txt_output.delete("1.0", tk.END)
        txt_output.insert(tk.END, morse)
        txt_output.config(state=tk.DISABLED)
    try:
        wpm = float(spin_wpm.get())
    except:
        wpm = 20.0
    try:
        freq = int(spin_freq.get())
    except:
        freq = 600
    player.play(morse, wpm=wpm, freq=freq)

def do_stop():
    player.stop()

def save_project_snapshot():
    # Save output to a file (if user wants), but you said no txt by default; keep feature optional
    v = txt_output.get("1.0", tk.END).strip()
    if not v:
        messagebox.showinfo("Info", "Output gol.")
        return
    path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt"),("All files","*.*")])
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(v)
        messagebox.showinfo("Saved", f"Salvat: {path}")

root = tk.Tk()
root.title("Morse Signalium — Encoder/Decoder with Audio")
root.geometry("760x520")

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

lbl = ttk.Label(frame, text="Input (text sau Morse):")
lbl.pack(anchor="w")
txt_input = tk.Text(frame, height=7)
txt_input.pack(fill=tk.X, pady=6)

btn_frame = ttk.Frame(frame)
btn_frame.pack(fill=tk.X, pady=4)
btn_encode = ttk.Button(btn_frame, text="Encode → Morse", command=do_encode)
btn_encode.pack(side=tk.LEFT, padx=4)
btn_decode = ttk.Button(btn_frame, text="Decode → Text", command=do_decode)
btn_decode.pack(side=tk.LEFT, padx=4)
btn_swap = ttk.Button(btn_frame, text="Swap I/O", command=do_swap)
btn_swap.pack(side=tk.LEFT, padx=4)

lbl_out = ttk.Label(frame, text="Output:")
lbl_out.pack(anchor="w", pady=(8,0))
txt_output = tk.Text(frame, height=7, state=tk.DISABLED)
txt_output.pack(fill=tk.X, pady=6)

ctrls = ttk.Frame(frame)
ctrls.pack(fill=tk.X, pady=6)

ttk.Label(ctrls, text="WPM:").pack(side=tk.LEFT, padx=(0,6))
spin_wpm = ttk.Spinbox(ctrls, from_=5, to=60, width=6)
spin_wpm.set(20)
spin_wpm.pack(side=tk.LEFT)

ttk.Label(ctrls, text="Freq (Hz):").pack(side=tk.LEFT, padx=(10,6))
spin_freq = ttk.Spinbox(ctrls, from_=200, to=1500, width=8)
spin_freq.set(600)
spin_freq.pack(side=tk.LEFT)

play_btn = ttk.Button(ctrls, text="Play ▶", command=do_play)
play_btn.pack(side=tk.LEFT, padx=10)
stop_btn = ttk.Button(ctrls, text="Stop ■", command=do_stop)
stop_btn.pack(side=tk.LEFT)

save_btn = ttk.Button(ctrls, text="Save Output...", command=save_project_snapshot)
save_btn.pack(side=tk.RIGHT)

status = ttk.Label(root, text="Reguli: dot='.', dash='-'. Separator litere = 1 spațiu, separator cuvinte = 3 spații.", anchor="w")
status.pack(fill=tk.X, padx=10, pady=(0,8))

root.mainloop()

import unicodedata

def normalize_text_for_morse(s: str) -> str:
    # decomposes accents and strips diacritics
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    # German sharp S -> SS
    s = s.replace('ß', 'ss')
    # Optionally expand German umlauts to AE/OE/UE — comment/uncomment as you prefer:
    s = s.replace('Ä', 'AE').replace('ä', 'ae') \
         .replace('Ö', 'OE').replace('ö','oe') \
         .replace('Ü','UE').replace('ü','ue')
    return s.upper()

