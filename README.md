# Physio DietFit Care

Static website for Physio DietFit Care, deployed to
https://www.physiodietfitcare.com via GitHub Pages.

Plain HTML with no build step. Shared styling lives in `index.css`; pages also
load the Tailwind CDN. Nav and footer are hand-copied per page, so a change to
either has to be applied to every page — `tools/verify_site.py` checks that
none were missed.

## Booking forms — one-time activation required

Both booking forms on `index.html` submit to
[FormSubmit](https://formsubmit.co/) and deliver to
`physiodietfitcare@gmail.com`.

**FormSubmit sends a one-time activation email to that address after the first
submission. Until someone opens that email and clicks the activation link, no
form submissions are delivered.**

To activate:

1. Open https://www.physiodietfitcare.com/ and submit the booking form once
   with real details.
2. Open the `physiodietfitcare@gmail.com` inbox and find the email from
   FormSubmit.
3. Click the activation link inside it.
4. Submit the form a second time and confirm the submission arrives.

This has to be done by whoever controls the Gmail account. It cannot be done
from the codebase.

## Verifying the site

```bash
python tools/verify_site.py
```

Six checks, all of which must pass before deploying:

| Check | What it catches |
|---|---|
| local assets exist | any `href`/`src` pointing at a file that is not in the repo |
| no dummy links | leftover `action="#"`, `href="#"`, `href=""`, `src=""` |
| form fields named | a booking-form field with no `name`, which would submit blank |
| legal text verbatim | legal copy that was paraphrased instead of reproduced |
| nav and footer consistency | a page missing the Events or legal links |
| SEO head tags | a missing or duplicated description, canonical, OG or Twitter tag |

To preview locally:

```bash
python -m http.server 8765
```

## Re-extracting the client images

`tools/extract_docx.py` pulls the client-supplied images out of the
requirements `.docx` and writes them to their destinations in `image/`:

```bash
python tools/extract_docx.py "path/to/requirements.docx"
```
