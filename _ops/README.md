# Website operations

Edit guide content in guides.json, comparisons in comparisons.json, shared markup in build.py, and base URL in config.json. Render with `python3 _ops/build.py` then require `python3 _ops/validate.py` to print OK. This is a plain static site; no install or runtime build is needed by GitHub Pages.

The app repo's site/ directory is the source of truth. Preserve search verification files in the deployment checkout. Never publish private app docs, keys, or analytics exports. The original OG image can be rebuilt from the app checkout using _ops/og.mjs; production serves the existing PNG and does not need that helper.
