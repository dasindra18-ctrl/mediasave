# MediaSave public-site starter

This edition converts **user-uploaded authorized media**; it intentionally does not download YouTube videos. A YouTube player can be embedded separately using YouTube's official embed feature.

## Local
Install Python 3.12+, FFmpeg, then `pip install -r requirements.txt` and `python app.py`. Open http://localhost:5000.

## Docker
`docker build -t mediasave .`
`docker run --rm -p 5000:5000 mediasave`

## Deploy on a Docker-compatible host
1. Create a GitHub repository and upload these files.
2. Create a Docker web service at your preferred host (e.g., Render, Railway, or a VPS) and connect the repository.
3. Set the host's HTTP port to 5000 if needed; verify the host supports up to 100 MB uploads, FFmpeg and request times of at least 200 seconds.
4. Purchase a domain from a registrar; configure DNS exactly as your host instructs, and enable HTTPS.
5. Replace the placeholder Contact page, customize the Privacy/Terms pages, test uploads, and set up backups/monitoring.
6. Apply for AdSense only after the website offers substantial original content and meets Google program policies. No approval is guaranteed. Do not place ad code until your publisher account and privacy/consent requirements are ready.

## Before accepting public traffic
This is a **deployment starter, not a hardened production service**. Add authenticated or anonymous per-IP quotas, rate limits, concurrency limits, disk-space quotas, background job queue, periodic cleanup of interrupted jobs, malware scanning, MIME/content inspection, monitoring, abuse reporting, a CSRF strategy as needed, reverse proxy size/time limits, and a consent management solution where required. Public media conversion is CPU-intensive; budget for hosting and egress. Use a separate isolated worker for untrusted files. The current cleanup callback may not run on abruptly terminated workers.

## Easiest Android deployment with Render Blueprint
1. Create a GitHub account if you do not already have one. In your browser create a new repository, then upload the **contents** of the `mediasave-public` folder (not the containing folder).
2. Sign in to https://dashboard.render.com with GitHub, authorize access to that repository.
3. Select **New > Blueprint**, choose the repository, and approve the service creation. The `render.yaml` requests the free plan; if the free plan is not offered, stop before accepting a paid plan.
4. Wait for deployment, then open the `https://...onrender.com` address Render assigns. The URL is not known until Render deploys it.
5. Upload a small file you own and test MP3 conversion. This is a limited demonstration, not a high-traffic production downloader.

The free tier may spin down, impose bandwidth/CPU constraints, or terminate long conversions. Render and GitHub account authorization must be performed by the account owner.
