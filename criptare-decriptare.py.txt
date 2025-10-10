# Cod Morse - Criptare & Decriptare
# by Georgiana & GPT-5 😊

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

# inversare: Morse -> litere
MORSE_TO_TEXT = {v: k for k, v in MORSE_CODE.items()}

def text_to_morse(text):
    text = text.upper()
    morse = []
    for char in text:
        if char == ' ':
            morse.append('')  # spațiu între cuvinte
        elif char in MORSE_CODE:
            morse.append(MORSE_CODE[char])
    return ' '.join(morse)

def morse_to_text(morse):
    words = morse.split('   ')  # 3 spații = despărțitor de cuvinte
    decoded_words = []
    for word in words:
        letters = word.split()
        decoded_letters = [MORSE_TO_TEXT.get(l, '') for l in letters]
        decoded_words.append(''.join(decoded_letters))
    return ' '.join(decoded_words)

# Exemple de utilizare
text = "HELLO MORSE"
morse = text_to_morse(text)
decoded = morse_to_text(morse)

print("Text original:", text)
print("Cod Morse:", morse)
print("Decriptare:", decoded)
