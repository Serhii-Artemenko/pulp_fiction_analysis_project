import re
import pandas as pd

SCRIPT_PATH = "../scripts_From_Movie/pf.txt"
OUTPUT_CSV = "../scripts_From_Movie/pulp_fiction_dialogue.csv"

def is_speaker_line(line: str) -> bool:
    line = line.rstrip()

    stripped = line.strip()

    if not stripped:
        return False

    # Ignore non-speaker stuff
    bad_prefixes = [
        "INT.", "EXT.", "CUT TO", "CREDIT", "FADE", "DISSOLVE",
        "SUPER:", "ANGLE ON", "CLOSE ON"
    ]
    if any(stripped.startswith(p) for p in bad_prefixes):
        return False

    # Scene headings often have " MORNING", " DAY", etc. with periods
    if " COFFEE SHOP" in stripped or " APARTMENT " in stripped:
        return False

    # Must be mostly uppercase letters / spaces / punctuation
    # and not too long
    if len(stripped) > 30:
        return False

    # At least 2 letters
    if len(re.sub(r"[^A-Z]", "", stripped)) < 2:
        return False

    # Only uppercase letters, numbers, spaces, etc.
    if not re.fullmatch(r"[A-Z0-9 '&\-.]+", stripped):
        return False

    return True


def parse_script_to_rows(lines):
    rows = []
    current_speaker = None
    current_text_parts = []

    def flush():
        nonlocal current_speaker, current_text_parts
        if current_speaker and current_text_parts:
            text = " ".join(p.strip() for p in current_text_parts if p.strip())
            if text:  # avoid empty rows
                rows.append({"name": current_speaker, "text": text})
        current_speaker = None
        current_text_parts = []

    for raw_line in lines:
        line = raw_line.rstrip("\n")

        # Blank line = often end of a speech chunk
        if not line.strip():
            # end of current speech block
            if current_speaker is not None:
                flush()
            continue

        if is_speaker_line(line):
            # New speaker, flush previous one
            flush()
            current_speaker = line.strip()
            continue

        if current_speaker is not None:
            current_text_parts.append(line)
        else:
            # Narrative / directions we ignore
            continue

    # Flush last one
    flush()
    return rows


def main():
    with open(SCRIPT_PATH, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    rows = parse_script_to_rows(lines)

    df = pd.DataFrame(rows, columns=["name", "text"])
    # drop very short lines or non dialogue
    df = df[df["text"].str.strip() != ""]
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {len(df)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
