# Batch 18 — the GitHub banner and the link-preview image

Branch `build/batch-18-github-banner`, 19 Nov 2026. **Awaiting Vincent's merge.** No firmware change.

- `assets/brand/dog5-github-banner.png`: 1280 × 320, on a 640 × 160 pixel grid (each pixel 2 × 2). The dog head
  mark, then the pixel wordmark (Sun Yellow, black outline, Acid Chartreuse shadow), the tagline "the runt bastard
  no one wanted" in Ray Pink and "free firmware for the M-VAVE FM-1 synth" in Grime Olive, on black. It is now the
  first thing in `README.md` (the `# DØG-5` heading stays under it).
- `assets/brand/dog5-social-preview.png`: 1280 × 640, the same lockup larger. This is the picture shown when the
  repo link is pasted into Slack, WhatsApp, X, Discord and so on.

**The link preview is not set by a file in the repo.** GitHub only takes it from the repo's settings page:
Settings → General → Social preview → Edit → Upload an image, and choose `dog5-social-preview.png`. It is under
GitHub's 1 MB limit (14 KB).

The head mark in both is reduced automatically from the 240 px favicon (to 136 px and 196 px). Hand-pixelled sizes,
if they are ever drawn, would replace them.
