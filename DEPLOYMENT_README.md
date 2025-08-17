# Climate Risk Analysis Platform - Deployment Guide

## 🚀 Live Deployments

### Primary Deployment
- **Surge.sh**: https://climate-risk-analysis.surge.sh ✅ LIVE
- **Vercel**: https://climate-risk-analysis.vercel.app (Access restricted)
- **GitHub Repository**: https://github.com/jiahknee5/climate-risk-analysis

## 🌀 Climate Applications

The platform features 4 distinct climate risk analysis applications:

1. **Hurricane Risk Map** (`/hurricane-risk-map.html`)
   - Interactive property risk mapping with Leaflet
   - 5-tier risk classification system
   - Property clustering and detailed popup data

2. **Hurricane Season Simulation** (`/hurricane-season-2026.html`)
   - Real-time hurricane season forecasting
   - Storm tracking and categorization
   - Temporal analysis and statistics

3. **Climate Scenarios Comparison** (`/climate-scenarios.html`)
   - Dual-map RCP scenario comparison
   - Long-term climate projections (2020-2100)
   - Side-by-side impact visualization

4. **Enhanced Climate Risk Analysis** (`/real-estate-risk.html`)
   - CLIMADA framework integration
   - Unified analysis combining all 3 approaches
   - Business impact assessment and recommendations

## 📋 Use Case Tests & Analysis

Comprehensive testing documentation available at:
- `/climate-use-case-tests.md` - Detailed analysis of all 4 applications

## 🛠️ API-Based Deployment Options

This project includes multiple deployment scripts for different platforms:

### 1. Surge.sh (Currently Live) ✅
```bash
python3 simple-deploy.py surge
```
- **URL**: https://climate-risk-analysis.surge.sh
- **Status**: ✅ Successfully deployed and accessible
- **Pros**: Free, instant deployment, no authentication issues
- **Cons**: Limited custom domain options

### 2. Vercel via API
```bash
# Requires VERCEL_TOKEN environment variable
node deploy-api.js
```
- **Features**: Production-grade CDN, automatic HTTPS
- **Status**: ⚠️ Currently has team permission issues (401 errors)
- **Solution**: Use personal Vercel account instead of team

### 3. GitHub Pages via API
```bash
# Requires GITHUB_TOKEN environment variable  
node deploy-github-pages.js github
```
- **Features**: Free hosting, custom domain support
- **Custom Domain**: climate.johnnycchung.com (requires DNS setup)
- **Status**: Ready to deploy with token

### 4. Local Development Server
```bash
python3 simple-deploy.py local 8080
```
- **URL**: http://localhost:8080
- **Features**: Hot reload, CORS headers, SPA routing

## 🌍 Custom Domain Setup

For `johnnycchung.com/climate` subdomain:

### Option 1: GitHub Pages (Recommended)
1. Deploy using GitHub Pages script
2. Add DNS CNAME record: `climate.johnnycchung.com` → `jiahknee5.github.io`
3. Enable HTTPS in GitHub Pages settings

### Option 2: Surge.sh Custom Domain
```bash
# Deploy with custom domain
surge public climate.johnnycchung.com
```
1. Add DNS CNAME record: `climate.johnnycchung.com` → `na-west1.surge.sh`

### Option 3: Direct Subdirectory
1. Upload files to `johnnycchung.com/climate/` directory
2. Ensure server handles SPA routing properly

## 🔧 API Deployment Architecture

### Why API Deployment?

Traditional CLI deployment tools (Vercel CLI, Netlify CLI) often face authentication and permission issues in team/organizational contexts. API-based deployment provides:

1. **Direct Control**: Bypass CLI authentication issues
2. **Programmatic Deployment**: Automate via CI/CD pipelines  
3. **Error Handling**: Better debugging and error recovery
4. **Multi-Platform**: Single script for multiple deployment targets

### Vercel REST API Implementation
```javascript
// Example: Create deployment via API
const deployment = await fetch('https://api.vercel.com/v13/deployments', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${VERCEL_TOKEN}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'climate-risk-analysis',
    files: files, // Base64 encoded file contents
    target: 'production'
  })
});
```

### GitHub Pages API Implementation
```javascript
// Example: Deploy files via GitHub API
await fetch(`https://api.github.com/repos/owner/repo/contents/path`, {
  method: 'PUT',
  headers: {
    'Authorization': `token ${GITHUB_TOKEN}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: 'Deploy to GitHub Pages',
    content: Buffer.from(fileContent).toString('base64')
  })
});
```

## 📊 Deployment Comparison

| Platform | Status | Custom Domain | HTTPS | API Deploy | Cost |
|----------|--------|---------------|-------|------------|------|
| Surge.sh | ✅ Live | ✅ Supported | ✅ Free | ✅ Available | Free |
| Vercel | ⚠️ Auth Issues | ✅ Full Support | ✅ Automatic | ✅ Available | Free Tier |
| GitHub Pages | 🟡 Ready | ✅ Supported | ✅ Free | ✅ Available | Free |
| Local Dev | ✅ Available | ❌ localhost | ❌ HTTP only | N/A | Free |

## 🔐 Environment Variables Required

For full deployment capabilities, set these environment variables:

```bash
# Vercel API deployment
export VERCEL_TOKEN="your_vercel_token"

# GitHub Pages deployment  
export GITHUB_TOKEN="your_github_token"

# Optional: Custom domain
export CUSTOM_DOMAIN="climate.johnnycchung.com"
```

## 🧪 Testing Deployed Applications

After deployment, test each application:

1. **Main Landing Page**: Should load with project overview
2. **Hurricane Risk Map**: Interactive Leaflet map with property clustering
3. **Hurricane Season**: Live statistics and timeline simulation
4. **Climate Scenarios**: Dual-map comparison interface
5. **Enhanced Analysis**: Multi-panel CLIMADA integration

All applications should be mobile-responsive and load within 3 seconds.

## 🚨 Troubleshooting

### Vercel 401 Errors
- **Issue**: Team permission restrictions
- **Solution**: Deploy under personal account or use Surge.sh

### GitHub Pages 404 Errors  
- **Issue**: File paths not properly configured
- **Solution**: Run the GitHub Pages deployment script (handles path updates)

### CORS Issues in Local Development
- **Issue**: Cross-origin requests blocked
- **Solution**: Use the Python deployment server (includes CORS headers)

### Large File Issues
- **Issue**: Some platforms have file size limits
- **Solution**: Optimize images and use CDN links for large assets

## 📈 Performance Monitoring

Monitor deployed applications:
- **Uptime**: Use UptimeRobot or similar service
- **Performance**: Google PageSpeed Insights
- **Analytics**: Google Analytics integration
- **Error Tracking**: Sentry or LogRocket for client-side errors

## 🔄 Continuous Deployment

Set up automated deployment:
1. GitHub Actions for automated deployment on push
2. Webhook integration for content updates
3. Staging environment for testing before production
4. Rollback capabilities for quick recovery

The API-based deployment approach ensures reliable, automated deployment regardless of platform-specific CLI issues.