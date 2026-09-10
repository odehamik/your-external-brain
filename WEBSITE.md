# Publish the workshop guide

The complete, prebuilt website is in `site/`. No installation, account key, or build command is needed to serve it. The site does not connect to an AI service. All participant downloads and starter text are bundled locally.

## Netlify: send people one welcoming link

1. Sign in to your intended Netlify account/team, then open https://app.netlify.com/drop.
2. Drop the `site` folder (the one containing `index.html`) onto the page. If using the prepared Netlify Site ZIP, unzip it and drop the extracted `Your External Brain - Site` folder instead.
3. Open the resulting Netlify address. Check the project's visibility settings: some teams default to private. Make it public for participants, then test the address in a signed-out/private browser window and download an edition before sharing.

Netlify account and plan terms still apply. No live Netlify address has been created by preparing these files. Official guide, checked 10 September 2026: https://docs.netlify.com/start/quickstarts/netlify-drop-quickstart/

Alternatively, connect this GitHub repository to Netlify. The included `netlify.toml` points to the prebuilt `site` folder. No build command is required.

## Maintain the files together

After changing participant content, run `python3 tools/build.py`, then `python3 tools/build-site.py`. The second copies the verified ZIPs and the identical starter text into the site and makes `.artifacts/Your External Brain - Netlify Site.zip`. Commit the refreshed site files with the content changes. Participants do not run these tools.

Edit the guide in `site/index.html`, `site/style.css`, and `site/app.js`. Native links and download files remain available without JavaScript; the copy button and section switching use JavaScript. There are no analytics, remote fonts, uploads, user accounts, or AI API calls in the site. Ordinary hosting logs and external sites' policies still apply.

The illustrative artwork was generated with AI and compressed for delivery. It is decorative, with empty alt text. The original generated master is preserved in the author's local build history; the public site ships the compressed derivative.

## Verification limits

Desktop and narrow-screen browser checks cover navigation, copy feedback, wording/text controls, local download links, layout, and console errors. These are not a participant accessibility study or evidence that every model follows the opening. Token savings are possible through selective context, not measured or guaranteed by this kit.
