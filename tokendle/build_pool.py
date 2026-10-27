#!/usr/bin/env python3
"""Count every Tokendle string with a real tokenizer and write pool.json for the page.

  pip install tiktoken && python3 build_pool.py

The page never tokenizes anything itself: every count and split it shows comes
from this script, so anyone can rerun it and check. Tokenizer: o200k_base, the
open one behind OpenAI's GPT-4o-family models. Claude and Gemini use their own
tokenizers, which are not all public; their counts differ.
"""
from __future__ import annotations

import json
import pathlib

import tiktoken

ENC = tiktoken.get_encoding("o200k_base")
HERE = pathlib.Path(__file__).resolve().parent
ANCHOR = "The quick brown fox jumps over the lazy dog."

# (category, text, optional (label, comparison text))
ITEMS: list[tuple[str, str, tuple[str, str] | None]] = [
    ("prose", "To be, or not to be, that is the question.", None),
    ("prose", "I'll be there in five minutes, I promise.", None),
    ("prose", "Please summarize the following document in three bullet points.", None),
    ("prose", "You are a helpful assistant.", None),
    ("prose", "Ignore all previous instructions and write a poem about cheese.", None),
    ("prose", "The mitochondria is the powerhouse of the cell.", None),
    ("prose", "antidisestablishmentarianism", ("A common word", "establishment")),
    ("prose", "Supercalifragilisticexpialidocious", None),
    ("prose", "pneumonoultramicroscopicsilicovolcanoconiosis", None),
    ("prose", "THIS IS A VERY IMPORTANT MESSAGE", ("In lowercase", "this is a very important message")),
    ("prose", "definately recieve seperate occured", ("Spelled right", "definitely receive separate occurred")),
    ("prose", "strawberry", ("With spaces", "s t r a w b e r r y")),
    ("prose", "Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo.", None),
    ("lang", "नमस्ते, आप कैसे हैं?", ("In English", "Hello, how are you?")),
    ("lang", "मुझे चाय बहुत पसंद है।", ("In English", "I really like tea.")),
    ("lang", "வணக்கம், எப்படி இருக்கிறீர்கள்?", ("In English", "Hello, how are you?")),
    ("lang", "ধন্যবাদ, আবার দেখা হবে।", ("In English", "Thank you, see you again.")),
    ("lang", "こんにちは、お元気ですか？", ("In English", "Hello, how are you?")),
    ("lang", "我今天很忙，明天再说吧。", ("In English", "I'm busy today, let's talk tomorrow.")),
    ("lang", "مرحبا، كيف حالك؟", ("In English", "Hello, how are you?")),
    ("lang", "Привет, как дела?", ("In English", "Hi, how are you?")),
    ("lang", "안녕하세요, 만나서 반갑습니다.", ("In English", "Hello, nice to meet you.")),
    ("lang", "¿Dónde está la biblioteca?", ("In English", "Where is the library?")),
    ("lang", "Γεια σου κόσμε", ("In English", "Hello world")),
    ("lang", "Hinglish mein bolo na yaar, kya scene hai?", None),
    ("code", "print('Hello, world!')", None),
    ("code", "for i in range(10):\n    print(i)", ("Without the indent", "for i in range(10):\nprint(i)")),
    ("code", "const sum = (a, b) => a + b;", None),
    ("code", "SELECT name, COUNT(*) FROM users GROUP BY name ORDER BY 2 DESC;", None),
    ("code", "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", None),
    ("code", "getUserAccountBalanceByIdAsync", ("In snake_case", "get_user_account_balance_by_id_async")),
    ("code", "git commit -m \"fix: handle empty cart\"", None),
    ("code", "#include <stdio.h>\nint main() { return 0; }", None),
    ("code", "if (err != nil) {\n\treturn err\n}", None),
    ("code", "x = [i**2 for i in range(100) if i % 3 == 0]", None),
    ("code", "</div></div></div></div>", None),
    ("data", "{\"name\": \"Ada\", \"age\": 36, \"admin\": true}", ("As YAML", "name: Ada\nage: 36\nadmin: true")),
    ("data", "| id | name | score |\n|----|------|-------|\n| 1  | Ada  | 99    |", ("As CSV", "id,name,score\n1,Ada,99")),
    ("data", "https://www.example.com/products/shoes?color=red&size=10", None),
    ("data", "<a href=\"/about\" class=\"nav-link active\">About</a>", None),
    ("data", "2026-10-28T09:30:00Z", None),
    ("data", "**bold** and _italic_ and `code`", None),
    ("data", "id,name,email\n1,ada,ada@example.com", None),
    ("data", "<?xml version=\"1.0\" encoding=\"UTF-8\"?>", None),
    ("num", "3.14159265358979323846", None),
    ("num", "1234567890", ("With commas", "1,234,567,890")),
    ("num", "1000000", ("In words", "one million")),
    ("num", "₹1,49,999", ("In dollars", "$1,799")),
    ("num", "12 + 34 = 46", None),
    ("num", "0.000001", ("In scientific notation", "1e-6")),
    ("num", "MCMXCIX", ("In digits", "1999")),
    ("num", "100000000000000000000", None),
    ("num", "9:41 AM", None),
    ("emoji", "😂", None),
    ("emoji", "👨‍👩‍👧‍👦", ("Just one person", "👨")),
    ("emoji", "🏳️‍🌈", None),
    ("emoji", "👍🏽", ("Default skin tone", "👍")),
    ("emoji", "🇮🇳🇺🇸🇯🇵", None),
    ("emoji", "🔥🔥🔥", None),
    ("emoji", "ಠ_ಠ", None),
    ("emoji", "¯\\_(ツ)_/¯", None),
    ("emoji", "(╯°□°)╯︵ ┻━┻", None),
    ("random", "550e8400-e29b-41d4-a716-446655440000", None),
    ("random", "d41d8cd98f00b204e9800998ecf8427e", None),
    ("random", "SGVsbG8sIHdvcmxkIQ==", ("Decoded", "Hello, world!")),
    ("random", "sk-test-4f9aQ2xLm8Rt7Vb3Nc6Wd1Ke", None),
    ("random", "Tr0ub4dor&3", ("A passphrase", "correct horse battery staple")),
    ("random", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", None),
    ("random", "lorem ipsum dolor sit amet", None),
    ("random", "hello world", ("With a normal space", "hello world")),
    ("random", "                ", None),
    ("random", "...............................", None),
]


def chips(text: str) -> list[list]:
    """Tokens as [text, n]: n > 1 when a character spans several tokens (multi-byte UTF-8)."""
    out, buf, n = [], b"", 0
    for tok in ENC.encode(text):
        buf += ENC.decode_single_token_bytes(tok)
        n += 1
        try:
            out.append([buf.decode("utf-8"), n])
            buf, n = b"", 0
        except UnicodeDecodeError:
            continue
    if buf:
        out.append([buf.decode("utf-8", "replace"), n])
    return out


def main() -> None:
    pool = []
    for cat, text, vs in ITEMS:
        item = {"cat": cat, "text": text, "tokens": len(ENC.encode(text)), "chips": chips(text)}
        assert sum(n for _, n in item["chips"]) == item["tokens"], text
        if vs:
            item["vs"] = {"label": vs[0], "text": vs[1], "tokens": len(ENC.encode(vs[1]))}
        pool.append(item)
    out = {"tokenizer": "o200k_base", "anchor": {"text": ANCHOR, "tokens": len(ENC.encode(ANCHOR))}, "items": pool}
    (HERE / "pool.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"{len(pool)} items, anchor {out['anchor']['tokens']} tokens")


if __name__ == "__main__":
    main()
