#!/usr/bin/env python3
"""Extract the client-supplied images from the requirements .docx.

Usage:  python tools/extract_docx.py "<path to .docx>"

A .docx is a zip; images live in word/media/. Image numbering follows
document order, which is how IMAGE_MAP below was derived.

Three of the images replace ones the client flagged as blurred; those keep
their existing filenames so no markup has to change. The other eight are
event posters.
"""
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

IMAGE_MAP = {
    # Flagged "blurred image / missing" in the client document.
    "image1.jpeg": "image/microbe.jpeg",
    "image2.jpg": "image/genetic.jpeg",
    "image3.jpg": "image/pain.jpeg",
    # Event posters.
    "image4.jpeg": "image/events/webinar-ai-readiness.jpeg",
    "image5.jpeg": "image/events/seminar-burns-gym.jpeg",
    "image6.jpg": "image/events/poshan-maah-2025.jpg",
    "image7.jpg": "image/events/camp-ecocity.jpg",
    "image8.jpg": "image/events/camp-vridhcare.jpg",
    "image9.jpg": "image/events/webinar-disability-awareness.jpg",
    "image10.jpeg": "image/events/webinar-psychology-of-muscle.jpeg",
    "image11.jpeg": "image/events/webinar-beyond-back-pain.jpeg",
}


def main(docx_path):
    source = Path(docx_path)
    if not source.is_file():
        print("error: not a file: %s" % source)
        return 1

    with zipfile.ZipFile(source) as archive:
        media = {
            Path(n).name: n for n in archive.namelist() if n.startswith("word/media/")
        }
        missing = set(IMAGE_MAP) - set(media)
        if missing:
            print("error: docx is missing expected media: %s" % sorted(missing))
            return 1

        for media_name, dest_rel in IMAGE_MAP.items():
            dest = ROOT / dest_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(media[media_name]) as src, dest.open("wb") as out:
                shutil.copyfileobj(src, out)
            print("wrote %s" % dest_rel)

    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
