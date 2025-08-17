# Manual GitHub Pages Setup Guide

Since we need a GitHub token for API deployment, here's how to set up GitHub Pages manually:

## Quick Setup (5 minutes)

### Step 1: Enable GitHub Pages
1. Go to https://github.com/jiahknee5/climate-risk-analysis/settings/pages
2. Under "Source", select "Deploy from a branch"
3. Choose "main" branch and "/ (root)" folder
4. Click "Save"

### Step 2: Set Custom Domain
1. In the same Pages settings page
2. Under "Custom domain", enter: `climate.johnnycchung.com`
3. Click "Save" 
4. Check "Enforce HTTPS" (after DNS is configured)

### Step 3: Configure DNS
Add this CNAME record to your domain DNS:
```
Type: CNAME
Name: climate
Value: jiahknee5.github.io
TTL: 300 (or Auto)
```

## File Structure Already Ready
The repository already has all files in the correct structure:
- ✅ `index.html` - Main landing page
- ✅ `hurricane-risk-map.html` - Interactive property risk map
- ✅ `hurricane-season-2026.html` - Hurricane season simulation  
- ✅ `climate-scenarios.html` - Climate scenarios comparison
- ✅ `real-estate-risk.html` - Enhanced CLIMADA analysis
- ✅ `climate-use-case-tests.md` - Use case tests documentation

## Expected URLs After Setup
- **Main Site**: https://climate.johnnycchung.com
- **Hurricane Risk Map**: https://climate.johnnycchung.com/hurricane-risk-map.html
- **Hurricane Season**: https://climate.johnnycchung.com/hurricane-season-2026.html
- **Climate Scenarios**: https://climate.johnnycchung.com/climate-scenarios.html
- **Enhanced Analysis**: https://climate.johnnycchung.com/real-estate-risk.html

## Verification Steps
1. GitHub Pages should show "Your site is live at https://climate.johnnycchung.com"
2. DNS check: `nslookup climate.johnnycchung.com` should return GitHub IPs
3. SSL certificate will be automatically issued by GitHub
4. All 4 climate applications should be accessible

## Alternative: Automated Setup with Token
If you have a GitHub token with 'repo' scope:
```bash
export GITHUB_TOKEN="your_token_here"
python3 setup-github-pages.py
```

This will automatically:
- Enable GitHub Pages
- Create CNAME file
- Optimize file paths
- Configure custom domain
- Display setup instructions