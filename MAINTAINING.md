# Maintaining this kit

Edit `editions/markdown/` as the source. `START-HERE.txt` and `00 OPEN ME FIRST.txt` are plain text in both editions and copied unchanged. Keep the opening self-contained: no prerequisite chain of uploaded files before the model can help.

Run `python3 tools/build.py` with Python 3.10 or later. It uses the standard library, converts Markdown into the Plain Text edition, validates local links and text destinations, checks for accidental local paths and removed exercises, and builds both ZIPs. It verifies ZIP contents against the actual folders. No network calls or installations.

The generator does not silently delete unexpected files. If removing a source file, inspect and deliberately handle its generated counterpart before rebuilding. Participants should never be asked to run this builder.

`downloads/CHECKS.json` records package checksums and check results. Structural checks do not demonstrate a model following the handshake. Actual model and accessibility feedback should be recorded accurately, with no participant transcripts copied without permission.

Provider settings were checked on the dates stated in the relevant file. Recheck official help when changing them. Do not change a dated note to today without verification.

This kit was developed from Maya Chacaby’s directions, the prior external-brain folder, and a review of her Sanctum Method onboarding. The separate private source repository and MythOS vault are not dependencies. Do not copy their private context or live runtime into participant releases.

After building the participant editions, run `python3 tools/build-site.py` to refresh the website downloads, starter, and Netlify ZIP. See WEBSITE.md for publishing.
