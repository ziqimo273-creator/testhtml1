# Three-site offline mirror

This workflow downloads the sites into three separate folders on your Windows computer.

## Important
Only mirror sites you own or have permission to archive, and respect each site's robots.txt and terms. The script waits between requests. A crawl cannot guarantee that every JavaScript-generated route, API-backed feature, or protected page is captured.

## Run on Windows
1. Install GNU Wget and Python 3.
2. Download this repository (Code → Download ZIP) and extract it.
3. Open PowerShell in the extracted folder.
4. Run:
   ```powershell
   Set-ExecutionPolicy -Scope Process Bypass
   .\mirror-sites.ps1
   python .\check-links.py
   ```
5. The downloaded mirrors will be under `offline-sites\namestyles`, `offline-sites\diagonalcalculator`, and `offline-sites\stylenamegenerator`. Open each site's downloaded `index.html`.

## Results
Check Wget output for HTTP errors, robots exclusions, redirects, and blocked resources. The link checker detects missing local targets referenced by HTML. It does not validate every remote URL or JavaScript-generated link. Some dynamic features may require the original backend and may not work offline.
