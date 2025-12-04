"""Tkinter GUI for the Day06 flag guessing game.

Run with:
    python -m game.day06.ui

The GUI shows a country flag emoji and four button options for country names.
The player clicks the correct country name or presses number keys (1-4).
The game continues until they click Stop, which shows the final score.
"""
import tkinter as tk
from tkinter import messagebox
import random
import sys
from pathlib import Path
import os
import platform
import subprocess
import threading


# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from .game_logic import GameState
except (ImportError, ValueError):
    from game_logic import GameState


class FlagGuessingApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Flag Guesser — Guess the Country!")
        root.geometry("500x500")

        self.state = GameState()
        self.choice_buttons = []
        self.settings = {"sound": True, "animations": True}
        self.guessing_active = True  # Prevent duplicate guesses during feedback

        # Title
        title = tk.Label(root, text="Guess the Country", font=("Arial", 18, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Flag display (large)
        self.flag_label = tk.Label(root, text="🚩", font=("Arial", 100))
        self.flag_label.grid(row=1, column=0, columnspan=2, pady=20)

        # Choice buttons grid
        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Status
        self.status = tk.Label(root, text="Rounds: 0 | Correct: 0", font=("Arial", 12))
        self.status.grid(row=3, column=0, columnspan=2, pady=10)

        # Settings button
        settings_btn = tk.Button(root, text="⚙ Settings", command=self.show_settings, font=("Arial", 10))
        settings_btn.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        # Stop button
        self.stop_btn = tk.Button(root, text="Stop and Show Score", command=self.stop_game, font=("Arial", 10))
        self.stop_btn.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Bind keyboard events for number keys 1-4
        root.bind("1", lambda e: self.key_press(0))
        root.bind("2", lambda e: self.key_press(1))
        root.bind("3", lambda e: self.key_press(2))
        root.bind("4", lambda e: self.key_press(3))

        # Show first round
        self.show_next()

    def show_next(self):
        """Load and display the next flag round."""
        result = self.state.next_round()
        if result is None:
            messagebox.showerror("Error", "Could not load countries data.")
            return
        
        flag, choices = result
        self.flag_label.config(text=flag)
        self.guessing_active = True  # Allow guessing on new round
        
        # Clear old buttons
        for btn in self.choice_buttons:
            btn.destroy()
        self.choice_buttons.clear()

        # Create new buttons for each choice, randomly positioned
        for i, choice in enumerate(choices):
            btn = tk.Button(
                self.button_frame,
                text=choice,
                font=("Arial", 11),
                width=20,
                command=lambda c=choice: self.submit(c)
            )
            btn.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            self.choice_buttons.append(btn)

        self.update_status()

    def submit(self, country_name: str):
        """Submit a guess."""
        if not self.guessing_active:
            return
        
        self.guessing_active = False  # Prevent duplicate guesses
        
        try:
            is_correct = self.state.submit_guess(country_name)
        except RuntimeError:
            messagebox.showwarning("No active round", "No active flag to guess.")
            self.guessing_active = True
            return

        # Highlight the buttons to show feedback
        self._highlight_answer(country_name, is_correct)
        
        # Play sound immediately (start before messagebox)
        if is_correct and self.settings["sound"]:
            self.play_correct_sound()
        
        # Show messagebox (this will block, but sound is already playing)
        if is_correct:
            messagebox.showinfo("Correct!", f"✓ That's right — {country_name}!")
        else:
            messagebox.showinfo("Wrong", f"✗ Incorrect. Try the next flag!")
        
        self.update_status()
        self.show_next()

    def _highlight_answer(self, country_name: str, is_correct: bool):
        """Highlight the selected button and show correct answer if wrong."""
        _, correct_name, _ = self.state.current or (None, None, [])
        
        for i, btn in enumerate(self.choice_buttons):
            if is_correct and btn.cget("text") == country_name:
                # Correct answer: highlight in green
                btn.config(bg="lightgreen", fg="darkgreen")
            elif not is_correct and btn.cget("text") == country_name:
                # Wrong selected answer: highlight in red
                btn.config(bg="lightcoral", fg="darkred")
            elif not is_correct and btn.cget("text") == correct_name:
                # Show correct answer in green when wrong
                btn.config(bg="lightgreen", fg="darkgreen")
        
        # Reset colors after a short delay (for visual feedback)
        if self.settings["animations"]:
            self.root.after(1500, self._reset_button_colors)
        else:
            self._reset_button_colors()

    def _reset_button_colors(self):
        """Reset button colors to default."""
        for btn in self.choice_buttons:
            btn.config(bg="SystemButtonFace", fg="black")

    def play_correct_sound(self):
        """Play a pleasant 'correct' sound on macOS asynchronously."""
        def _play():
            try:
                if platform.system() == "Darwin":  # macOS
                    # Use macOS system sound (Glass or Ping) - non-blocking
                    subprocess.Popen(
                        ["afplay", "/System/Library/Sounds/Glass.aiff"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                elif platform.system() == "Windows":
                    import winsound
                    # Windows system sound (ascending tones)
                    winsound.Beep(800, 150)  # 800 Hz, 150 ms
                    winsound.Beep(1000, 150)  # 1000 Hz, 150 ms
                else:  # Linux and others
                    self.root.bell()
            except Exception:
                # Fallback to system bell if sound fails
                try:
                    self.root.bell()
                except:
                    pass
        
        # Run sound in background thread to avoid blocking UI
        thread = threading.Thread(target=_play, daemon=True)
        thread.start()

    def update_status(self):
        """Update the status label with current score."""
        self.status.config(
            text=f"Rounds: {self.state.total_rounds} | Correct: {self.state.correct}"
        )

    def stop_game(self):
        """End the game and show final score."""
        pct = (
            round(100 * self.state.correct / self.state.total_rounds)
            if self.state.total_rounds > 0
            else 0
        )
        msg = (
            f"Final Score\n\n"
            f"Correct: {self.state.correct} out of {self.state.total_rounds}\n"
            f"Accuracy: {pct}%"
        )
        messagebox.showinfo("Game Over", msg)
        self.play_again_or_quit()

    def play_again_or_quit(self):
        """Ask user if they want to play again or quit."""
        result = messagebox.askyesno("Play Again?", "Would you like to play another round?")
        if result:
            self.reset_game()
        else:
            self.root.quit()

    def reset_game(self):
        """Reset the game for a new session."""
        self.state = GameState()
        self.guessing_active = True
        self.show_next()

    def key_press(self, index: int):
        """Handle number key presses (1-4)."""
        if index < len(self.choice_buttons):
            btn = self.choice_buttons[index]
            country_name = btn.cget("text")
            self.submit(country_name)

    def show_settings(self):
        """Show settings dialog."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x150")
        settings_window.transient(self.root)

        # Sound toggle
        sound_var = tk.BooleanVar(value=self.settings["sound"])
        sound_check = tk.Checkbutton(
            settings_window,
            text="🔊 Enable Sound Effects",
            variable=sound_var,
            font=("Arial", 11)
        )
        sound_check.pack(pady=10)

        # Animations toggle
        anim_var = tk.BooleanVar(value=self.settings["animations"])
        anim_check = tk.Checkbutton(
            settings_window,
            text="✨ Enable Animations",
            variable=anim_var,
            font=("Arial", 11)
        )
        anim_check.pack(pady=10)

        # Save button
        def save_settings():
            self.settings["sound"] = sound_var.get()
            self.settings["animations"] = anim_var.get()
            settings_window.destroy()

        save_btn = tk.Button(
            settings_window,
            text="Save Settings",
            command=save_settings,
            font=("Arial", 10)
        )
        save_btn.pack(pady=10)


def main():
    root = tk.Tk()
    app = FlagGuessingApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
