# Deploying the Personal Website to Vercel

The website is a single static file (`index.html`) with no build step.
`vercel.json` configures clean URLs and security headers, and
`.vercelignore` keeps the Python AI-agents code out of the deployment.

## Option 1: Vercel Dashboard (recommended)

1. Go to [vercel.com/new](https://vercel.com/new) and sign in with GitHub.
2. Import the `rgowrigari/AiAgents` repository.
3. Leave all settings at their defaults:
   - **Framework Preset:** Other
   - **Build Command:** (none)
   - **Output Directory:** (none — the site is served from the repo root)
4. Click **Deploy**. The site will be live at `https://<project-name>.vercel.app`.

Every push to the production branch redeploys automatically, and other
branches get preview deployments.

## Option 2: Vercel CLI

```bash
npm install -g vercel
cd AiAgents
vercel          # first run: link the project, accept defaults
vercel --prod   # deploy to production
```

## Custom domain

After deploying, add a custom domain (e.g. `ravindar.dev`) under
**Project → Settings → Domains** in the Vercel dashboard.
