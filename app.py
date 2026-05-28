"""
MorseSignalium
===============

Educational desktop application for encoding and decoding Morse code.

Features:
- Encode plain text to Morse code.
- Decode Morse code back to readable text.
- Play Morse code as audio beeps where supported.
- Copy output to clipboard.
- Clear input/output areas.
- Save a small local conversion history.

Author: RISCyCat
"""

from __future__ import annotations

import json
import platform
import time
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, scrolledtext


# -----------------------------------------------------------------------------
# Morse alphabet table
# -----------------------------------------------------------------------------
# Each key is a supported character.
# Each value is the Morse representation of that character.
MORSE_CODE: dict[str, str] = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    "'": ".----.",
    "!": "-.-.--",
    "/": "-..-.",
    "(": "-.--.",
    ")": "-.--.-",
    "&": ".-...",
    ":": "---...",
    ";": "-.-.-.",
    "=": "-...-",
    "+": ".-.-.",
    "-": "-....-",
    "_": "..--.-",
    '"': ".-..-.",
    "$": "...-..-",
    "@": ".--.-.",
}


# Reverse dictionary used for decoding Morse back to text.
TEXT_CODE: dict[str, str] = {value: key for key, value in MORSE_CODE.items()}


# Local history file stored near the application.
HISTORY_FILE = Path("morse_history.json")


# -----------------------------------------------------------------------------
# Core algorithmic functions
# -----------------------------------------------------------------------------
def encode_to_morse(text: str) -> str:
    """
    Convert normal text into Morse code.

    Rules:
    - Letters are converted case-insensitively.
    - Characters inside one word are separated by one space.
    - Words are separated by " / ".
    - Unsupported characters are ignored instead of crashing the application.
    """

    encoded_words: list[str] = []

    for word in text.upper().split():
        encoded_letters: list[str] = []

        for character in word:
            morse_symbol = MORSE_CODE.get(character)

            if morse_symbol is not None:
                encoded_letters.append(morse_symbol)

        if encoded_letters:
            encoded_words.append(" ".join(encoded_letters))

    return " / ".join(encoded_words)


def decode_from_morse(morse: str) -> str:
    """
    Convert Morse code back into normal text.

    Rules:
    - Morse letters must be separated by spaces.
    - Morse words must be separated by slash: /.
    - Unknown Morse groups are replaced with "?".
    """

    decoded_words: list[str] = []

    for morse_word in morse.strip().split("/"):
        decoded_letters: list[str] = []

        for symbol in morse_word.strip().split():
            decoded_letters.append(TEXT_CODE.get(symbol, "?"))

        decoded_words.append("".join(decoded_letters))

    return " ".join(decoded_words).strip()


def save_history(input_text: str, output_text: str, operation: str) -> None:
    """Save the latest conversion in a small JSON history file."""

    entry = {
        "operation": operation,
        "input": input_text,
        "output": output_text,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    try:
        if HISTORY_FILE.exists():
            history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        else:
            history = []

        history.append(entry)

        # Keep the history compact.
        history = history[-50:]

        HISTORY_FILE.write_text(
            json.dumps(history, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except OSError:
        # History is useful but not essential. The app should continue working.
        pass


# -----------------------------------------------------------------------------
# Audio support
# -----------------------------------------------------------------------------
def play_beep(frequency: int, duration_ms: int, root: tk.Tk) -> None:
    """Play a short beep using the best method available on the current OS."""

    if platform.system() == "Windows":
        try:
            import winsound

            winsound.Beep(frequency, duration_ms)
            return
        except RuntimeError:
            pass

    # Portable fallback: Tkinter bell. It does not control frequency/duration,
    # but it keeps the button functional on Linux/macOS.
    root.bell()
    root.update()
    time.sleep(duration_ms / 1000)


def play_morse_audio(morse: str, root: tk.Tk) -> None:
    """
    Play Morse code as audio.

    Timing convention used here:
    - dot: short beep
    - dash: longer beep
    - space: short pause between letters
    - slash: longer pause between words
    """

    if not morse.strip():
        messagebox.showwarning("Empty output", "There is no Morse code to play.")
        return

    dot_ms = 120
    dash_ms = dot_ms * 3
    frequency = 700

    for character in morse:
        if character == ".":
            play_beep(frequency, dot_ms, root)
            time.sleep(dot_ms / 1000)
        elif character == "-":
            play_beep(frequency, dash_ms, root)
            time.sleep(dot_ms / 1000)
        elif character == " ":
            time.sleep((dot_ms * 2) / 1000)
        elif character == "/":
            time.sleep((dot_ms * 6) / 1000)


# -----------------------------------------------------------------------------
# Tkinter graphical interface
# -----------------------------------------------------------------------------
class MorseSignaliumApp:
    """Main graphical application class."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("MorseSignalium")
        self.root.geometry("850x650")
        self.root.minsize(760, 560)

        self._build_interface()

    def _build_interface(self) -> None:
        """Create all visual widgets used by the application."""

        title_label = tk.Label(
            self.root,
            text="MorseSignalium",
            font=("Arial", 22, "bold"),
        )
        title_label.pack(pady=(16, 4))

        subtitle_label = tk.Label(
            self.root,
            text="Encode and decode Morse code with a simple educational interface.",
            font=("Arial", 11),
        )
        subtitle_label.pack(pady=(0, 12))

        input_label = tk.Label(
            self.root,
            text="Input text or Morse code:",
            font=("Arial", 12, "bold"),
            anchor="w",
        )
        input_label.pack(fill="x", padx=20)

        self.input_box = scrolledtext.ScrolledText(
            self.root,
            height=8,
            font=("Consolas", 11),
            wrap=tk.WORD,
        )
        self.input_box.pack(fill="both", padx=20, pady=(4, 12), expand=True)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=4)

        encode_button = tk.Button(
            button_frame,
            text="Encode → Morse",
            width=18,
            command=self.encode_action,
        )
        encode_button.grid(row=0, column=0, padx=6, pady=4)

        decode_button = tk.Button(
            button_frame,
            text="Decode ← Morse",
            width=18,
            command=self.decode_action,
        )
        decode_button.grid(row=0, column=1, padx=6, pady=4)

        play_button = tk.Button(
            button_frame,
            text="Play Morse Audio",
            width=18,
            command=self.play_action,
        )
        play_button.grid(row=0, column=2, padx=6, pady=4)

        copy_button = tk.Button(
            button_frame,
            text="Copy Output",
            width=18,
            command=self.copy_output_action,
        )
        copy_button.grid(row=1, column=0, padx=6, pady=4)

        clear_button = tk.Button(
            button_frame,
            text="Clear",
            width=18,
            command=self.clear_action,
        )
        clear_button.grid(row=1, column=1, padx=6, pady=4)

        history_button = tk.Button(
            button_frame,
            text="Show History",
            width=18,
            command=self.show_history_action,
        )
        history_button.grid(row=1, column=2, padx=6, pady=4)

        output_label = tk.Label(
            self.root,
            text="Output:",
            font=("Arial", 12, "bold"),
            anchor="w",
        )
        output_label.pack(fill="x", padx=20, pady=(8, 0))

        self.output_box = scrolledtext.ScrolledText(
            self.root,
            height=8,
            font=("Consolas", 11),
            wrap=tk.WORD,
        )
        self.output_box.pack(fill="both", padx=20, pady=(4, 16), expand=True)

    def _get_input(self) -> str:
        """Read user input from the input text area."""
        return self.input_box.get("1.0", tk.END).strip()

    def _set_output(self, value: str) -> None:
        """Replace the current output with a new value."""
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, value)

    def encode_action(self) -> None:
        """Handle the Encode button."""
        input_text = self._get_input()

        if not input_text:
            messagebox.showwarning("Empty input", "Please write text before encoding.")
            return

        output_text = encode_to_morse(input_text)
        self._set_output(output_text)
        save_history(input_text, output_text, "encode")

    def decode_action(self) -> None:
        """Handle the Decode button."""
        input_text = self._get_input()

        if not input_text:
            messagebox.showwarning("Empty input", "Please write Morse code before decoding.")
            return

        output_text = decode_from_morse(input_text)
        self._set_output(output_text)
        save_history(input_text, output_text, "decode")

    def play_action(self) -> None:
        """Handle the Play Morse Audio button."""
        morse = self.output_box.get("1.0", tk.END).strip()
        play_morse_audio(morse, self.root)

    def copy_output_action(self) -> None:
        """Copy output text to the operating system clipboard."""
        output_text = self.output_box.get("1.0", tk.END).strip()

        if not output_text:
            messagebox.showwarning("Empty output", "There is no output to copy.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(output_text)
        messagebox.showinfo("Copied", "Output copied to clipboard.")

    def clear_action(self) -> None:
        """Clear both input and output fields."""
        self.input_box.delete("1.0", tk.END)
        self.output_box.delete("1.0", tk.END)

    def show_history_action(self) -> None:
        """Display the saved conversion history in a new window."""
        history_window = tk.Toplevel(self.root)
        history_window.title("MorseSignalium History")
        history_window.geometry("700x450")

        history_box = scrolledtext.ScrolledText(
            history_window,
            font=("Consolas", 10),
            wrap=tk.WORD,
        )
        history_box.pack(fill="both", expand=True, padx=12, pady=12)

        if not HISTORY_FILE.exists():
            history_box.insert(tk.END, "No history available yet.")
            return

        try:
            history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            history_box.insert(tk.END, "History could not be loaded.")
            return

        for index, entry in enumerate(history, start=1):
            history_box.insert(tk.END, f"#{index} | {entry['timestamp']} | {entry['operation']}\n")
            history_box.insert(tk.END, f"Input : {entry['input']}\n")
            history_box.insert(tk.END, f"Output: {entry['output']}\n")
            history_box.insert(tk.END, "-" * 70 + "\n")


# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------
def main() -> None:
    """Start the MorseSignalium desktop application."""
    root = tk.Tk()
    app = MorseSignaliumApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
