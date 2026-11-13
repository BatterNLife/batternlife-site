// Cloudflare Worker for batternlife.com
// Serves the static site, plus GET /api/reels
// Returns Melinda's 4 newest Instagram videos for the Bake Life "Latest Videos" section.
// Needs one secret in the Worker settings: IG_TOKEN (Instagram system-user token, never expires).
const IG_ID = '17841408703301552';   // @batternlife
const API = 'v27.0';
const TTL = 3 * 3600;                // re-check Instagram at most every 3 hours

async function reels(request, env, ctx) {
  const headers = { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'public, max-age=' + TTL };
  const noStore = { ...headers, 'cache-control': 'no-store' };
  const cache = caches.default;
  const key = new Request(new URL('/api/reels?c=1', request.url).toString());
  const hit = await cache.match(key);
  if (hit) return hit;
  if (!env.IG_TOKEN) return new Response('{"posts":[],"error":"not_configured"}', { status: 503, headers: noStore });
  try {
    const url = `https://graph.facebook.com/${API}/${IG_ID}/media?fields=media_type,permalink,thumbnail_url,caption,timestamp&limit=25&access_token=${encodeURIComponent(env.IG_TOKEN)}`;
    const r = await fetch(url);
    const d = await r.json();
    if (!r.ok || d.error) throw new Error('instagram');
    const posts = (d.data || [])
      .filter(p => p.media_type === 'VIDEO' && p.thumbnail_url && p.permalink)
      .slice(0, 4)
      .map(p => ({ u: p.permalink, i: p.thumbnail_url, c: (p.caption || '').split('\n')[0].slice(0, 110), t: p.timestamp }));
    if (!posts.length) throw new Error('empty');
    const res = new Response(JSON.stringify({ posts }), { headers });
    ctx.waitUntil(cache.put(key, res.clone()));
    return res;
  } catch (e) {
    return new Response('{"posts":[],"error":"upstream"}', { status: 502, headers: noStore });
  }
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === '/api/reels') return reels(request, env, ctx);
    return env.ASSETS.fetch(request);
  }
};
