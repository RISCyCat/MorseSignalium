import tkinter as tk
from tkinter import ttk, messagebox

MORSE_CODE = {
    'A': '.-',    'B': '-...',  'C': '-.-.', 'D': '-..',
    'E': '.',     'F': '..-.',  'G': '--.',  'H': '....',
    'I': '..',    'J': '.---',  'K': '-.-',  'L': '.-..',
    'M': '--',    'N': '-.',    'O': '---',  'P': '.--.',
    'Q': '--.-',  'R': '.-.',   'S': '...',  'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',  'X': '-..-',
    'Y': '-.--',  'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ',': '--..--', '.': '.-.-.-', '?': '..--..', '!': '-.-.--',
    '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-'
}

MORSE_TO_TEXT = {v: k for k, v in MORSE_CODE.items()}

def text_to_morse(text: str) -> str:
    parts = []
    for ch in text.upper():
        if ch == ' ':
            parts.append('')  # cuvânt separator -> vom avea 2 spații consecutive -> 3 în final
        elif ch in MORSE_CODE:
            parts.append(MORSE_CODE[ch])
        else:
            parts.append('?')
    # Înlocuim '' cu separator de cuvinte (două spații vor rezulta din join -> facem 3)
    return ' '.join(parts).replace('  ', '   ')

def morse_to_text(morse: str) -> str:
    words = morse.strip().split('   ')
    decoded = []
    for w in words:
        letters = w.split()
        decoded.append(''.join(MORSE_TO_TEXT.get(l, '?') for l in letters))
    return ' '.join(decoded)

def do_encode():
    txt = input_text.get("1.0", tk.END).strip()
    if not txt:
        messagebox.showinfo("Info", "Introdu text pentru criptare.")
        return
    out = text_to_morse(txt)
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, out)
    output_text.config(state=tk.DISABLED)

def do_decode():
    txt = input_text.get("1.0", tk.END).strip()
    if not txt:
        messagebox.showinfo("Info", "Introdu cod Morse pentru decriptare.")
        return
    out = morse_to_text(txt)
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, out)
    output_text.config(state=tk.DISABLED)

def swap_io():
    inp = input_text.get("1.0", tk.END)
    out = output_text.get("1.0", tk.END)
    input_text.delete("1.0", tk.END)
    input_text.insert(tk.END, out)
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, inp)
    output_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Morse Encoder / Decoder")
root.geometry("760x440")
root.resizable(False, False)

frm = ttk.Frame(root, padding=12)
frm.pack(fill=tk.BOTH, expand=True)

lbl_in = ttk.Label(frm, text="Input (text sau Morse):")
lbl_in.grid(row=0, column=0, sticky="w")
input_text = tk.Text(frm, height=10, width=80)
input_text.grid(row=1, column=0, columnspan=3, pady=6)

btn_encode = ttk.Button(frm, text="Encode -> Morse", command=do_encode)
btn_encode.grid(row=2, column=0, sticky="ew", padx=(0,6))

btn_decode = ttk.Button(frm, text="Decode -> Text", command=do_decode)
btn_decode.grid(row=2, column=1, sticky="ew", padx=(0,6))

btn_swap = ttk.Button(frm, text="Swap I/O", command=swap_io)
btn_swap.grid(row=2, column=2, sticky="ew")

lbl_out = ttk.Label(frm, text="Output:")
lbl_out.grid(row=3, column=0, sticky="w", pady=(10,0))
output_text = tk.Text(frm, height=10, width=80, state=tk.DISABLED)
output_text.grid(row=4, column=0, columnspan=3, pady=6)

status = ttk.Label(root, text="Reguli: dot='.', dash='-'. Separator litere = un spațiu, separator cuvinte = 3 spații.", anchor="w")
status.pack(fill=tk.X, padx=12, pady=(0,8))

root.mainloop()
