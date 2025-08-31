#!/usr/bin/env python

"""
capucintype - KISS Monkeytype-like in cli, in Python
MIT License - Copyright (c) 2025 c4ffein
Code is dirty but was made with Claude and fixed in minutes
"""

import random
import time
import sys
import termios
import tty
import os
from os import get_terminal_size


# Source - https://gist.github.com/deekayen/4148741
KNOWN_WORDS = [
    "the", "of", "to", "and", "a", "in", "is", "it", "you", "that", "he", "was", "for", "on", "are", "with", "as",
    "I", "his", "they", "be", "at", "one", "have", "this", "from", "or", "had", "by", "not", "word", "but", "what",
    "some", "we", "can", "out", "other", "were", "all", "there", "when", "up", "use", "your", "how", "said", "an",
    "each", "she", "which", "do", "their", "time", "if", "will", "way", "about", "many", "then", "them", "write",
    "would", "like", "so", "these", "her", "long", "make", "thing", "see", "him", "two", "has", "look", "more",
    "day", "could", "go", "come", "did", "number", "sound", "no", "most", "people", "my", "over", "know", "water",
    "than", "call", "first", "who", "may", "down", "side", "been", "now", "find", "any", "new", "work", "part",
    "take", "get", "place", "made", "live", "where", "after", "back", "little", "only", "round", "man", "year",
    "came", "show", "every", "good", "me", "give", "our", "under", "name", "very", "through", "just", "form",
    "sentence", "great", "think", "say", "help", "low", "line", "differ", "turn", "cause", "much", "mean", "before",
    "move", "right", "boy", "old", "too", "same", "tell", "does", "set", "three", "want", "air", "well", "also",
    "play", "small", "end", "put", "home", "read", "hand", "port", "large", "spell", "add", "even", "land", "here",
    "must", "big", "high", "such", "follow", "act", "why", "ask", "men", "change", "went", "light", "kind", "off",
    "need", "house", "picture", "try", "us", "again", "animal", "point", "mother", "world", "near", "build", "self",
    "earth", "father", "head", "stand", "own", "page", "should", "country", "found", "answer", "school", "grow",
    "study", "still", "learn", "plant", "cover", "food", "sun", "four", "between", "state", "keep", "eye", "never",
    "last", "let", "thought", "city", "tree", "cross", "farm", "hard", "start", "might", "story", "saw", "far",
    "sea", "draw", "left", "late", "run", "don't", "while", "press", "close", "night", "real", "life", "few", "north",
    "open", "seem", "together", "next", "white", "children", "begin", "got", "walk", "example", "ease", "paper",
    "group", "always", "music", "those", "both", "mark", "often", "letter", "until", "mile", "river", "car", "feet",
    "care", "second", "book", "carry", "took", "science", "eat", "room", "friend", "began", "idea", "fish",
    "mountain", "stop", "once", "base", "hear", "horse", "cut", "sure", "watch", "color", "face", "wood", "main",
    "enough", "plain", "girl", "usual", "young", "ready", "above", "ever", "red", "list", "though", "feel", "talk",
    "bird", "soon", "body", "dog", "family", "direct", "pose", "leave", "song", "measure", "door", "product", "black",
    "short", "numeral", "class", "wind", "question", "happen", "complete", "ship", "area", "half", "rock", "order",
    "fire", "south", "problem", "piece", "told", "knew", "pass", "since", "top", "whole", "king", "space", "heard",
    "best", "hour", "better", "true", "during", "hundred", "five", "remember", "step", "early", "hold", "west",
    "ground", "interest", "reach", "fast", "verb", "sing", "listen", "six", "table", "travel", "less", "morning",
    "ten", "simple", "several", "vowel", "toward", "war", "lay", "against", "pattern", "slow", "center", "love",
    "person", "money", "serve", "appear", "road", "map", "rain", "rule", "govern", "pull", "cold", "notice",
    "voice", "unit", "power", "town", "fine", "certain", "fly", "fall", "lead", "cry", "dark", "machine", "note",
    "wait", "plan", "figure", "star", "box", "noun", "field", "rest", "correct", "able", "pound", "done", "beauty",
    "drive", "stood", "contain", "front", "teach", "week", "final", "gave", "green", "oh", "quick", "develop",
    "ocean", "warm", "free", "minute", "strong", "special", "mind", "behind", "clear", "tail", "produce", "fact",
    "street", "inch", "multiply", "nothing", "course", "stay", "wheel", "full", "force", "blue", "object", "decide",
    "surface", "deep", "moon", "island", "foot", "system", "busy", "test", "record", "boat", "common", "gold",
    "possible", "plane", "stead", "dry", "wonder", "laugh", "thousand", "ago", "ran", "check", "game", "shape",
    "equate", "hot", "miss", "brought", "heat", "snow", "tire", "bring", "yes", "distant", "fill", "east", "paint",
    "language", "among", "grand", "ball", "yet", "wave", "drop", "heart", "am", "present", "heavy", "dance",
    "engine", "position", "arm", "wide", "sail", "material", "size", "vary", "settle", "speak", "weight", "general",
    "ice", "matter", "circle", "pair", "include", "divide", "syllable", "felt", "perhaps", "pick", "sudden", "count",
    "square", "reason", "length", "represent", "art", "subject", "region", "energy", "hunt", "probable", "bed",
    "brother", "egg", "ride", "cell", "believe", "fraction", "forest", "sit", "race", "window", "store", "summer",
    "train", "sleep", "prove", "lone", "leg", "exercise", "wall", "catch", "mount", "wish", "sky", "board", "joy",
    "winter", "sat", "written", "wild", "instrument", "kept", "glass", "grass", "cow", "job", "edge", "sign", "visit",
    "past", "soft", "fun", "bright", "gas", "weather", "month", "million", "bear", "finish", "happy", "hope",
    "flower", "clothe", "strange", "gone", "jump", "baby", "eight", "village", "meet", "root", "buy", "raise",
    "solve", "metal", "whether", "push", "seven", "paragraph", "third", "shall", "held", "hair", "describe", "cook",
    "floor", "either", "result", "burn", "hill", "safe", "cat", "century", "consider", "type", "law", "bit", "coast",
    "copy", "phrase", "silent", "tall", "sand", "soil", "roll", "temperature", "finger", "industry", "value",
    "fight", "lie", "beat", "excite", "natural", "view", "sense", "ear", "else", "quite", "broke", "case", "middle",
    "kill", "son", "lake", "moment", "scale", "loud", "spring", "observe", "child", "straight", "consonant",
    "nation", "dictionary", "milk", "speed", "method", "organ", "pay", "age", "section", "dress", "cloud", "surprise",
    "quiet", "stone", "tiny", "climb", "cool", "design", "poor", "lot", "experiment", "bottom", "key", "iron",
    "single", "stick", "flat", "twenty", "skin", "smile", "crease", "hole", "trade", "melody", "trip", "office",
    "receive", "row", "mouth", "exact", "symbol", "die", "least", "trouble", "shout", "except", "wrote", "seed",
    "tone", "join", "suggest", "clean", "break", "lady", "yard", "rise", "bad", "blow", "oil", "blood", "touch",
    "grew", "cent", "mix", "team", "wire", "cost", "lost", "brown", "wear", "garden", "equal", "sent", "choose",
    "fell", "fit", "flow", "fair", "bank", "collect", "save", "control", "decimal", "gentle", "woman", "captain",
    "practice", "separate", "difficult", "doctor", "please", "protect", "noon", "whose", "locate", "ring",
    "character", "insect", "caught", "period", "indicate", "radio", "spoke", "atom", "human", "history", "effect",
    "electric", "expect", "crop", "modern", "element", "hit", "student", "corner", "party", "supply", "bone",
    "rail", "imagine", "provide", "agree", "thus", "capital", "won't", "chair", "danger", "fruit", "rich",
    "thick", "soldier", "process", "operate", "guess", "necessary", "sharp", "wing", "create", "neighbor",
    "wash", "bat", "rather", "crowd", "corn", "compare", "poem", "string", "bell", "depend", "meat", "rub",
    "tube", "famous", "dollar", "stream", "fear", "sight", "thin", "triangle", "planet", "hurry", "chief", "colony",
    "clock", "mine", "tie", "enter", "major", "fresh", "search", "send", "yellow", "gun", "allow", "print", "dead",
    "spot", "desert", "suit", "current", "lift", "rose", "continue", "block", "chart", "hat", "sell", "success",
    "company", "subtract", "event", "particular", "deal", "swim", "term", "opposite", "wife", "shoe", "shoulder",
    "spread", "arrange", "camp", "invent", "cotton", "born", "determine", "quart", "nine", "truck", "noise", "level",
    "chance", "gather", "shop", "stretch", "throw", "shine", "property", "column", "molecule", "select", "wrong",
    "gray", "repeat", "require", "broad", "prepare", "salt", "nose", "plural", "anger", "claim", "continent",
    "oxygen", "sugar", "death", "pretty", "skill", "women", "season", "solution", "magnet", "silver", "thank",
    "branch", "match", "suffix", "especially", "fig", "afraid", "huge", "sister", "steel", "discuss", "forward",
    "similar", "guide", "experience", "score", "apple", "bought", "led", "pitch", "coat", "mass", "card", "band",
    "rope", "slip", "win", "dream", "evening", "condition", "feed", "tool", "total", "basic", "smell", "valley",
    "nor", "double", "seat", "arrive", "master", "track", "parent", "shore", "division", "sheet", "substance",
    "favor", "connect", "post", "spend", "chord", "fat", "glad", "original", "share", "station", "dad", "bread",
    "charge", "proper", "bar", "offer", "segment", "slave", "duck", "instant", "market", "degree", "populate",
    "chick", "dear", "enemy", "reply", "drink", "occur", "support", "speech", "nature", "range", "steam", "motion",
    "path", "liquid", "log", "meant", "quotient", "teeth", "shell", "neck",
]


class RestartWanted(Exception):
    pass


class CapucinType:
    def __init__(self):
        self.words = KNOWN_WORDS
        self.target_text = ""
        self.typed_text = ""
        self.start_time = 0
        self.test_duration = 60
        self.word_count = 50

    def generate_text(self):
        """Generate random text for typing test"""
        selected_words = random.choices(self.words, k=self.word_count)
        self.target_text = " ".join(selected_words)

    def get_char(self):
        """Get a single character from stdin without pressing enter"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return char

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def display_text(self):
        """Display the text with color coding for correct/incorrect characters"""
        width, height = get_terminal_size()
        self.clear_screen()
        print(" " * width)
        print(" " * width)
        print(" " * (width // 2 - 20) + "┌──────────────────────────────────────┐")
        print(" " * (width // 2 - 20) + "│  CapucinType - Terminal Typing Test  │")
        print(" " * (width // 2 - 20) + "└──────────────────────────────────────┘")
        print(" " * width)
        print(" " * width)

        display_text = ""
        typed_len = len(self.typed_text)

        for i, char in enumerate(self.target_text):
            if i < typed_len:
                if self.typed_text[i] == char:
                    # Correct character - green text
                    display_text += f"\033[32m{char}\033[0m"
                else:
                    # Incorrect character - red text
                    display_text += f"\033[31m{char if char != ' ' else "_"}\033[0m"
            elif i == typed_len:
                # Current character - yellow text
                display_text += f"\033[33m{char}\033[0m"
            else:
                # Untyped character - normal
                display_text += f"\033[00m{char}\033[0m"
        # Split lines, won't handle len(word) < target_column_size since all words are known
        parts = []  # we want (start, end) tuples to handle spaces more easily
        target_column_size = max(12, min(80, width - 4))  # no word longer than 12, account for 2 + 2 padding
        print_char_size = 10
        current_start, current_end = 0, target_column_size * print_char_size  # current_end is exclusive
        while current_start < len(display_text):
            if current_end >= len(display_text):
                parts.append((current_start, len(display_text)))
                break
            if display_text[current_end + 5] in " _":  # next char is space
                parts.append((current_start, current_end))
                current_start = current_end + print_char_size
                current_end = min(
                    current_end + print_char_size + target_column_size * print_char_size,
                    len(display_text)
                )
                continue
            if display_text[current_end - print_char_size + 5] in " _":  # actual last char is space
                parts.append((current_start, current_end - print_char_size))
                current_start = current_end
                current_end = min(current_end + target_column_size * print_char_size, len(display_text))
                continue
            current_end -= 1
        for start, end in parts:
            print((" " * ((width - 80) // 2)) + display_text[start:end])
        print("\n" * min(0, 5 - len(parts)))  # at least one newline, complete block of text to at least 5 lines
        # Show stats / start message
        if self.start_time > 0:
            elapsed = time.time() - self.start_time
            if typed_len > 0:
                wpm = self.calculate_wpm(elapsed)
                accuracy = self.calculate_accuracy()
                stats_line = f"Time: {elapsed:.1f}s | WPM: {wpm:.0f} | Accuracy: {accuracy:.1f}%"
            else:
                stats_line = f"Time: {elapsed:.1f}s | Press any key to start typing..."
        else:
            stats_line = "Press any key to start the test!"
        print(" " * ((width - 80) // 2) + stats_line)
        print(" " * width)
        print(" " * ((width - 80) // 2) + "Controls: Ctrl+C to quit, Ctrl+R to start new game, Backspace to delete")
        print(" " * width)

    def calculate_wpm(self, elapsed_time):
        """Calculate words per minute"""
        if elapsed_time == 0:
            return 0
        words_typed = len([c for c in self.typed_text if c == " "]) + (1 if self.typed_text else 0)
        return (words_typed / elapsed_time) * 60

    def calculate_accuracy(self):
        """Calculate typing accuracy"""
        if not self.typed_text:
            return 100.0
        correct_chars = sum(1 for i, char in enumerate(self.typed_text)
                          if i < len(self.target_text) and char == self.target_text[i])
        return (correct_chars / len(self.typed_text)) * 100

    def show_results(self):
        """Show final test results"""
        self.clear_screen()
        width, height = get_terminal_size()

        # Top border (2 rows high, 4 chars wide)
        print(" " * width)
        print(" " * width)
        print(" " * (width // 2 - 20) + "┌──────────────────────────────────────┐")
        print(" " * (width // 2 - 20) + "│            Test Complete!            │")
        print(" " * (width // 2 - 20) + "└──────────────────────────────────────┘")
        print(" " * width)
        print(" " * width)
        elapsed = time.time() - self.start_time
        wpm = self.calculate_wpm(elapsed)
        accuracy = self.calculate_accuracy()

        correct_chars = sum(1 for i, char in enumerate(self.typed_text)
                          if i < len(self.target_text) and char == self.target_text[i])

        time_line = f"Time: {elapsed:.1f} seconds"
        wpm_line = f"Words per minute: {wpm:.1f}"
        accuracy_line = f"Accuracy: {accuracy:.1f}%"
        chars_line = f"Correct characters: {correct_chars}/{len(self.typed_text)}"

        print(" " * (max(width - 50, 0) // 2) + time_line)
        print(" " * (max(width - 50, 0) // 2) + wpm_line)
        print(" " * (max(width - 50, 0) // 2) + accuracy_line)
        print(" " * (max(width - 50, 0) // 2) + chars_line)
        print(" " * width)

        restart_line = "Press enter to restart or Ctrl+C to quit..."
        print(" " * (max(width - 50, 0) // 2) + restart_line)

    def run_test(self):
        """Run the typing test"""
        try:
            while True:
                try:
                    self.generate_text()
                    self.typed_text = ""
                    self.start_time = 0

                    self.display_text()

                    while len(self.typed_text) < len(self.target_text):
                        try:
                            char = self.get_char()

                            # Handle Ctrl+C
                            if ord(char) == 3:
                                raise KeyboardInterrupt

                            if ord(char) == 18:
                                raise RestartWanted

                            # Start timer on first keypress
                            if self.start_time == 0:
                                self.start_time = time.time()

                            # Handle backspace
                            if ord(char) == 127 and self.typed_text:
                                self.typed_text = self.typed_text[:-1]
                            # Handle regular characters (space and printable chars)
                            elif ord(char) >= 32 and ord(char) <= 126:
                                self.typed_text += char

                            self.display_text()

                            # Check if test duration exceeded
                            if self.start_time > 0 and time.time() - self.start_time >= self.test_duration:
                                break

                        except KeyboardInterrupt:
                            print("\nGoodbye!")
                            return

                    # Show results
                    self.show_results()

                    # Wait for restart or quit
                    try:
                        while True:
                            restart_char = self.get_char()
                            if ord(restart_char) == 3:
                                raise KeyboardInterrupt
                            if ord(restart_char) in [ord("\n"), 18]:
                                break
                    except KeyboardInterrupt:
                        break
                except RestartWanted:
                    pass

        except KeyboardInterrupt:
            print("\nGoodbye!")

def main():
    # Hide cursor
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    # Start game
    capucin_type = CapucinType()
    capucin_type.run_test()
    # Show cursor again when done
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
