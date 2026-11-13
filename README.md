# Batter N' Life

Website for Batter N' Life: custom celebration cakes, baking tips, and life as a mom of four.

Hosted on Cloudflare Workers (worker "batternlife"). The `worker/` code adds /api/reels, which reads the IG_TOKEN secret set in Cloudflare (never stored in this repo). Every change saved to this repository goes live automatically.

- `index.html`: the whole site (all six pages)
- `img/`: photos and logos
