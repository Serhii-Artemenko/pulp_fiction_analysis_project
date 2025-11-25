import re
from collections import defaultdict

INPUT_FILE = "pf.txt"  

CHARACTERS = {
    "Winston Wolfe": ["WOLFE", "THE WOLF"],
    "Captain Koons": ["CAPTAIN KOONS", "KOONS", "CAPT. KOONS"],
    "Lance": ["LANCE"]
}

NON_TRIVIAL_MIN_WORDS = 4  # ignore tiny banter lines like “Yeah”


def load_script():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return f.read()


def extract_dialog(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    dialog_by_character = defaultdict(list)
    current_char = None

    for line in lines:

        for canonical, variants in CHARACTERS.items():
            if any(re.fullmatch(v, line.upper()) for v in variants):
                current_char = canonical
                break
        else:
            if current_char:
                if len(line.split()) >= NON_TRIVIAL_MIN_WORDS:
                    dialog_by_character[current_char].append(line)

    return dialog_by_character


def save_dialog(dialog):
    for character, lines in dialog.items():
        filename = character.lower().replace(" ", "_") + ".txt"
        with open(filename, "w", encoding="utf-8") as f:
            for l in lines:
                f.write(l + "\n")
        print(f"Saved {len(lines)} lines for {character} → {filename}")


def main():
    text = load_script()

    dialog = extract_dialog(text)

    save_dialog(dialog)

    print("Done")


if __name__ == "__main__":
    main()
