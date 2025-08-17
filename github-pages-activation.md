# GitHub Pages Activation Guide - Step by Step

## 🚀 Activate GitHub Pages (2 minutes)

### Step 1: Go to Repository Settings
**URL**: https://github.com/jiahknee5/climate-risk-analysis/settings/pages

### Step 2: Configure Source
1. Under **"Source"** section:
   - Select: **"Deploy from a branch"**
   - Branch: **"main"** 
   - Folder: **"/ (root)"**
   - Click **"Save"**

### Step 3: Set Custom Domain  
1. Under **"Custom domain"** section:
   - Enter: **`climate.johnnycchung.com`**
   - Click **"Save"**
   - ✅ The CNAME file is already in the repository

### Step 4: Enable HTTPS (after DNS)
1. Check **"Enforce HTTPS"** (do this AFTER DNS is configured)

## 🌍 DNS Configuration Required

Add this CNAME record to your domain DNS settings:

```
Type: CNAME
Name: climate
Value: jiahknee5.github.io
TTL: 300 (or Auto)
```

**Where to add DNS record:**
- If using Cloudflare: DNS tab → Add record
- If using GoDaddy: DNS Management → Add CNAME
- If using Namecheap: Advanced DNS → Add CNAME

## 📱 Expected Results

After activation, you should see:
- ✅ **"Your site is live at https://climate.johnnycchung.com"**
- 🔄 **"DNS check successful"** (after DNS propagation)
- 🔒 **SSL certificate will be auto-issued**

## 🧪 Test URLs (after setup)

All these should work:
- https://climate.johnnycchung.com
- https://climate.johnnycchung.com/hurricane-risk-map.html
- https://climate.johnnycchung.com/hurricane-season-2026.html  
- https://climate.johnnycchung.com/climate-scenarios.html
- https://climate.johnnycchung.com/real-estate-risk.html

## ⏱️ Timeline

1. **GitHub Pages activation**: Immediate
2. **DNS propagation**: 5-30 minutes
3. **SSL certificate**: 10-60 minutes after DNS
4. **Fully operational**: Within 1 hour

## 🚨 Troubleshooting

### If "Pages" tab is missing:
- Repository must be public (it is ✅)
- Need admin access to repository (you have it ✅)

### If custom domain fails:
- Check DNS with: `nslookup climate.johnnycchung.com`
- Should return GitHub IP addresses
- Wait longer for DNS propagation

### If SSL fails:
- Don't enable "Enforce HTTPS" until DNS is working
- SSL certificate takes time to issue

## 🔄 Backup Option

If GitHub Pages has issues, Surge.sh is already live:
**https://climate-risk-analysis.surge.sh**

Ready to proceed? Navigate to the GitHub Pages settings URL above!