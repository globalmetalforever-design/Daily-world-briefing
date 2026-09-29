DAILY WORLD BRIEFING — GITHUB PAGES WEB MODULE

What it does
- A responsive website for World, India, Technology, Science and Business headlines.
- Shows the publisher's short RSS description, publisher name, date/time (when supplied), and a link to the original story.
- GitHub Actions collects RSS updates every four hours and updates data/news.json.
- No APK, API key, backend server, Wi-Fi setup, or user account is needed for visitors. Visitors need internet access.

IMPORTANT ABOUT SUMMARIES AND RIGHTS
This first build displays short descriptions supplied by RSS publishers; it does not generate AI summaries or reproduce full articles. RSS feeds can change, block requests, or have different terms. The collector records source names and links, but check each publisher's current RSS terms before making the site public or commercial. The app cannot promise every feed will always be available.

ONE-TIME PUBLISHING STEPS (GitHub website)
1. Download and extract this ZIP on your PC.
2. On GitHub, create a new public repository, for example: daily-world-briefing. Leave it empty (do not add README/license/gitignore).
3. On the new repository page, use Add file > Upload files.
4. Upload the CONTENTS of the extracted folder, including index.html, scripts, data, and the .github folder. If Windows does not show .github, enable hidden items in File Explorer. Make sure the folder structure is preserved; do not upload the whole parent folder as a nested directory.
5. Commit the upload to the main branch.
6. Open repository Settings > Pages. Under Build and deployment, select “Deploy from a branch”, branch “main”, folder “/(root)”, then Save.
7. Open Actions tab. If GitHub asks to enable workflows, enable them. Select “Update briefing feed” and click “Run workflow” once to populate the first news file. Wait for it to finish.
8. Open Settings > Actions > General. Under Workflow permissions, select “Read and write permissions” and save if the workflow cannot push the generated JSON file.
9. Open the Pages URL shown in Settings > Pages. The site should load; after the workflow completes, stories should appear. You can also rerun the workflow manually from Actions.

Troubleshooting
- Blank/no stories: open Actions > Update briefing feed and inspect the latest run. A feed may be temporarily unavailable. Try Run workflow again later.
- Workflow cannot push: set Actions workflow permissions to Read and write as above.
- GitHub Pages may take several minutes to publish after first setup.
- Automatic schedule uses UTC and GitHub may delay scheduled runs. The schedule is every four hours, not an exact breaking-news guarantee.

Project layout
index.html                         Website
scripts/fetch_news.py              RSS collection script (Python standard library only)
data/news.json                     Data file populated by the workflow
.github/workflows/update-news.yml  Scheduled workflow

This is a standalone module. It can be integrated into the larger project later.
