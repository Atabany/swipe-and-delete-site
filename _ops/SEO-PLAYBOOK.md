# Photo Cleaner: Swipe & Delete website playbook

Official app: 6754815949, bundle com.atabany.Clarity, developer Mohamed Elatabany. Source of truth: site/ in Atabany/clarity. Public deployment: Atabany/swipe-and-delete-site. Never use getphotocleaner.com or the sibling app's ID or creative.

## Facts and user decisions

Read _ops/facts.json and the live listing before writing product copy. Photo analysis is on-device; Apple/RevenueCat purchase information is processed off-device. Do not claim Data Not Collected, video compression, guaranteed space, system cleaning, rankings, endorsements or invented review counts. Never publish prices. There is one real written review in the initial fact snapshot; use only real review text.

The user explicitly requested a visible 5-star rating without its low count on October 4, 2026. Omit rating count from visible copy and LLM summaries. Keep actual rating/count accurate in MobileApplication structured data and facts.json. This overrides the skill's visible-count instruction.

## Weekly routine — Monday 09:00 Asia/Dubai

1. Check live HTTPS, home, sitemap, crawler rules and the app destination. Read app docs/KB.md and docs/TASKS.md where available.
2. Read real Search Console queries/positions, App Store Connect web referrals/campaign attribution, and RevenueCat aggregate conversion data when available. Missing data is unavailable, never zero. Record aggregate dated evidence in the private app docs, not this public repository. Do not publish customer identifiers or private dashboard screenshots.
3. Finish pending custom-domain, Search Console and Bing verification when authorized and accessible. Never buy a domain, log in for the user, grant OAuth permissions, or accept terms. Use DNS/HTML verification. Keep all existing URLs.
4. Choose one focused improvement informed by data or one useful guide from topics.md. Research primary sources. Provide the built-in iOS method first; identify edition-specific menu paths and iCloud syncing consequences. Guides: 800–1,300 original words, direct answer in first two sentences, real author, visible FAQ, correction link, sources and updated date.
5. Update guides.json/comparisons.json and render with python3 _ops/build.py. If facts change, update every visible rating and fact statement while preserving the user preference. Update config date and CSS cache version only as warranted; do not pretend unchanged guides were newly reviewed.
6. Run python3 _ops/validate.py and require OK. Inspect mobile and desktop layout for changed UI; test any changed tool logic with useful boundary cases. Publish only site files to this public repository; never sync the app repo or private documentation.
7. Ping IndexNow using _ops/indexnow.py for changed URLs. Record response status; accepted submission is not proof of indexing. Preserve prior verification files during synchronization.
8. Record the outcome and next question in private KB/tasks. Stay quiet if nothing meaningful changed or an already-reported blocker is unchanged. Notify only a useful published improvement, meaningful results, failure, or required user action.

## Quarterly review

Review stale Apple menus and competitor features, rating accuracy, campaigns, broken sources, privacy statements and crawlability. Training crawler controls and search crawlers have different roles. llms.txt is an optional reference aid, not evidence of ranking or AI citations. An allowed crawler is not an endorsement.

## Deployment

GitHub Pages initially: https://atabany.github.io/swipe-and-delete-site/. No CNAME until a domain is actually purchased. Proposed getswipeanddelete.com is not owned. Change config base, rerender, preserve every page pathname, update AppLinks, configure DNS and HTTPS, and verify GitHub's old-path redirects after purchase.
