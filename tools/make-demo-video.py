#!/usr/bin/env python3
"""
Build the 90-second demo video for GERMLINE.

Subcommands:
    slides    render scene PNGs (1280x720) into dist/video/frames/
    assemble  combine frames (+ optional narration) into dist/germline-demo-90s.mp4

Everything is reproducible: fixed palette, fixed scene list, Pillow + static ffmpeg.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "video"
W, H = 1280, 720

BG = (11, 18, 32)
CARD = (17, 27, 46)
FG = (248, 250, 252)
MUTED = (148, 163, 184)
CYAN = (34, 211, 238)
AMBER = (245, 158, 11)
GREEN = (52, 211, 153)
RED = (248, 113, 113)

F_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def center(d: ImageDraw.ImageDraw, y: int, text: str, f=None, fill=FG, font=None) -> int:  # noqa: A002
    f = font or f
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)
    return y + f.size + 16


def card(d: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, radius=18) -> None:
    d.rounded_rectangle((x, y, x + w, y + h), radius=radius, fill=CARD, outline=(30, 41, 59), width=2)


SCENES: list[tuple[str, int]] = [
    ("01_title", 7),
    ("02_problem", 12),
    ("03_antibody", 12),
    ("04_corpus", 12),
    ("05_abx", 13),
    ("06_evidence", 11),
    ("07_gate", 12),
    ("08_close", 10),
]


def scene_title(d: ImageDraw.ImageDraw) -> None:
    y = center(d, 210, "GERMLINE", font(F_BOLD, 96), CYAN)
    y = center(d, y + 6, "Immune inheritance for software", font(F_REG, 34), FG)
    center(d, y + 30, "100 executable antibodies  ·  ABX v0.1  ·  open source", font(F_MONO, 20), MUTED)


def scene_problem(d: ImageDraw.ImageDraw) -> None:
    y = center(d, 120, "AI rewrites code fast.", font(F_BOLD, 54))
    y = center(d, y + 8, "Its security memory does not survive the rewrite.", font(F_REG, 34), FG)
    card(d, 240, y + 60, 800, 150)
    lines = [
        ("C library · 20 years of fixes", MUTED),
        ("→ AI-assisted rewrite →", CYAN),
        ("new language, old tests pass … but old attacks may work again", AMBER),
    ]
    yy = y + 95
    for text, color in lines:
        tw = d.textlength(text, font=font(F_MONO, 24))
        d.text(((W - tw) / 2, yy), text, font=font(F_MONO, 24), fill=color)
        yy += 44


def scene_antibody(d: ImageDraw.ImageDraw) -> None:
    y = center(d, 90, "An antibody is a permanent test", font(F_BOLD, 54))
    y = center(d, y + 6, "one historical vulnerability → one discriminating experiment", font(F_REG, 28), MUTED)
    card(d, 140, y + 40, 460, 190)
    d.text((180, y + 70), "VULNERABLE BUILD", font=font(F_BOLD, 26), fill=RED)
    d.text((180, y + 115), "must  F A I L", font=font(F_MONO, 30), fill=FG)
    d.text((180, y + 160), "crash + sanitizer marker", font=font(F_REG, 22), fill=MUTED)
    card(d, 680, y + 40, 460, 190)
    d.text((720, y + 70), "FIXED BUILD", font=font(F_BOLD, 26), fill=GREEN)
    d.text((720, y + 115), "must stay  C L E A N", font=font(F_MONO, 30), fill=FG)
    d.text((720, y + 160), "no marker, exit clean", font=font(F_REG, 22), fill=MUTED)
    center(d, y + 260, "no discrimination → not an antibody (RFC-0, INV-1)", font=font(F_MONO, 20), fill=MUTED)


def scene_corpus(d: ImageDraw.ImageDraw) -> None:
    y = center(d, 90, "The corpus today", font(F_BOLD, 54))
    stats_ = [
        ("100", "antibodies", CYAN),
        ("17", "critical projects", FG),
        ("3", "verified end-to-end\non real Docker (CI)", GREEN),
        ("100", "ABX v0.1 documents", AMBER),
    ]
    x = 90
    for value, label, color in stats_:
        card(d, x, y + 30, 275, 230)
        d.text((x + 30, y + 60), value, font=font(F_BOLD, 76), fill=color)
        yy = y + 155
        for ln in label.split("\n"):
            d.text((x + 30, yy), ln, font=font(F_REG, 22), fill=MUTED)
            yy += 30
        x += 295
    center(d, y + 300, "libxml2 · ffmpeg · imagemagick · curl · openssl · wireshark · …", font=font(F_MONO, 20), fill=MUTED)


def scene_abx(d: ImageDraw.ImageDraw) -> None:
    y = center(d, 80, "ABX v0.1 — a format that travels", font(F_BOLD, 52))
    center(d, y + 6, "RFC-0 · strict JSON Schema · reference validator · canonical + signable", font=font(F_REG, 26), fill=MUTED)
    card(d, 170, y + 60, 940, 300)
    code = [
        ('"id": "AB-000001",', FG),
        ('"challenge": { "expect": { "vulnerable": "crash", "fixed": "clean" } },', CYAN),
        ('"detector":  { "type": "sanitizer-report", "match": "WARNING: MemorySanitizer" },', CYAN),
        ('"environments": { "vulnerable": "…:42470114-vul", "fixed": "…:42470114-fix" },', FG),
        ('"integrity": { "algorithm": "sha256", "value": "9df04776…" }', GREEN),
    ]
    yy = y + 95
    for text, color in code:
        d.text((210, yy), text, font=font(F_MONO, 21), fill=color)
        yy += 48


def scene_evidence(d: ImageDraw.ImageDraw) -> None:
    y = center(d, 90, "Evidence, not marketing", font(F_BOLD, 54))
    card(d, 220, y + 50, 840, 300)
    lines = [
        ("$ bash tools/run-corpus-checks.sh --sample 3", MUTED),
        ("  ✅ AB-000001 verified   crash on vulnerable / clean on fixed", GREEN),
        ("  ✅ AB-000002 verified   repeated across independent runs", GREEN),
        ("  ✅ AB-000003 verified   total: 3 verified · 0 mismatch", GREEN),
        ("", FG),
        ("# append-only log · corpus/VERIFICATION.md", CYAN),
    ]
    yy = y + 90
    for text, color in lines:
        d.text((250, yy), text, font=font(F_MONO, 21), fill=color)
        yy += 42


def scene_gate(d: ImageDraw.ImageDraw) -> None:
    y = center(d, 100, "The Immune Gate", font(F_BOLD, 54))
    center(d, y, "replay every ancestor's antibodies against every new generation", font=font(F_REG, 27), fill=MUTED)
    steps = ["g0  C reference", "g1  patch", "g2  AI rewrite (Rust)", "IMMUNE GATE", "signed passport"]
    x = 70
    for i, s in enumerate(steps):
        w = 230 if i < 3 else 250
        color = CYAN if i < 3 else (AMBER if i == 3 else GREEN)
        card(d, x, y + 70, w, 120, radius=14)
        tw = d.textlength(s, font=font(F_MONO, 19))
        d.text((x + (w - tw) / 2, y + 115), s, font=font(F_MONO, 19), fill=color)
        if i < len(steps) - 1:
            d.text((x + w + 8, y + 110), "→", font=font(F_BOLD, 34), fill=MUTED)
            x += w + 44
    center(d, y + 230, "passed 6/6 antibodies → Immune Parity VERIFIED", font=font(F_MONO, 22), fill=FG)


def scene_close(d: ImageDraw.ImageDraw) -> None:
    y = center(d, 180, "Everything above is public today.", font(F_BOLD, 50))
    y = center(d, y + 40, "github.com/FerasFuad34/germline", font=font(F_MONO, 40), fill=CYAN)
    center(d, y + 40, "Apache-2.0 (code)  ·  CC-BY-4.0 (data)  ·  spec open", font=font(F_REG, 26), fill=MUTED)
    center(d, y + 100, "SBOM tells you what's in your code.", font=font(F_REG, 24), fill=MUTED)
    center(d, y + 140, "GERMLINE tells you what your code survived.", font=font(F_REG, 24), fill=FG)


BUILDERS = {
    "01_title": scene_title,
    "02_problem": scene_problem,
    "03_antibody": scene_antibody,
    "04_corpus": scene_corpus,
    "05_abx": scene_abx,
    "06_evidence": scene_evidence,
    "07_gate": scene_gate,
    "08_close": scene_close,
}


def cmd_slides(_args) -> int:
    frames = OUT / "frames"
    frames.mkdir(parents=True, exist_ok=True)
    for name, _ in SCENES:
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, W, 6), fill=CYAN)
        BUILDERS[name](d)
        d.text((44, H - 52), "GERMLINE", font=font(F_BOLD, 20), fill=MUTED)
        d.text((W - 260, H - 52), "RFC-0 · corpus v0.1", font=font(F_MONO, 16), fill=MUTED)
        img.save(frames / f"{name}.png")
        print(f"  ✓ {name}.png")
    print(f"✅ slides in {frames}")
    return 0


def ffmpeg() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def cmd_assemble(args) -> int:
    frames = OUT / "frames"
    audio = Path(args.audio).resolve() if args.audio else None
    total = args.total
    durations = [d for _, d in SCENES]
    if total:  # scale scene durations so the video matches the narration length
        scale = total / sum(durations)
        durations = [max(4.5, d * scale) for d in durations]
        durations[-1] += total - sum(durations)  # absorb rounding in the last scene

    listfile = OUT / "concat.txt"
    with listfile.open("w", encoding="utf-8") as fh:
        for (name, _), dur in zip(SCENES, durations):
            fh.write(f"file 'frames/{name}.png'\n")
            fh.write(f"duration {dur:.3f}\n")
        fh.write(f"file 'frames/{SCENES[-1][0]}.png'\n")

    out = OUT / f"germline-demo-90s.mp4"
    cmd = [
        ffmpeg(), "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(listfile),
    ]
    if audio and audio.exists():
        cmd += ["-i", str(audio)]
    cmd += [
        "-fps_mode", "cfr", "-pix_fmt", "yuv420p",
        "-vf", "scale=1280:720",
        "-r", "30",
    ]
    if audio and audio.exists():
        cmd += ["-c:a", "aac", "-b:a", "160k", "-shortest"]
    cmd += ["-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True, cwd=OUT)
    print(f"✅ {out}  ({out.stat().st_size/1024:.0f} KB, ≈{sum(durations):.0f}s)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="GERMLINE demo video builder")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("slides"); s.set_defaults(func=cmd_slides)
    a = sub.add_parser("assemble")
    a.add_argument("--audio", help="narration file (mp3/wav) to embed")
    a.add_argument("--total", type=float, help="target total duration (scales scenes)")
    a.set_defaults(func=cmd_assemble)
    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
