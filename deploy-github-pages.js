#!/usr/bin/env node
/**
 * GitHub Pages Deployment Script
 * Alternative deployment using GitHub Pages API
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

class GitHubPagesDeployer {
    constructor(token, owner, repo) {
        this.token = token;
        this.owner = owner;
        this.repo = repo;
        this.baseUrl = 'https://api.github.com';
    }

    async makeRequest(endpoint, method = 'GET', data = null) {
        return new Promise((resolve, reject) => {
            const url = new URL(endpoint, this.baseUrl);
            
            const options = {
                hostname: url.hostname,
                port: 443,
                path: url.pathname + url.search,
                method: method,
                headers: {
                    'Authorization': `token ${this.token}`,
                    'Content-Type': 'application/json',
                    'User-Agent': 'Climate-Risk-Deployer/1.0',
                    'Accept': 'application/vnd.github.v3+json'
                }
            };

            if (data) {
                const jsonData = JSON.stringify(data);
                options.headers['Content-Length'] = Buffer.byteLength(jsonData);
            }

            const req = https.request(options, (res) => {
                let responseData = '';
                
                res.on('data', (chunk) => {
                    responseData += chunk;
                });
                
                res.on('end', () => {
                    try {
                        const parsed = responseData ? JSON.parse(responseData) : {};
                        if (res.statusCode >= 200 && res.statusCode < 300) {
                            resolve(parsed);
                        } else {
                            reject(new Error(`GitHub API Error ${res.statusCode}: ${parsed.message || responseData}`));
                        }
                    } catch (e) {
                        if (res.statusCode >= 200 && res.statusCode < 300) {
                            resolve({}); // Empty response is OK for some endpoints
                        } else {
                            reject(new Error(`Parse Error: ${responseData}`));
                        }
                    }
                });
            });

            req.on('error', (err) => {
                reject(err);
            });

            if (data) {
                req.write(JSON.stringify(data));
            }
            
            req.end();
        });
    }

    async enableGitHubPages() {
        try {
            // Enable GitHub Pages
            const pagesConfig = {
                source: {
                    branch: 'main',
                    path: '/'
                }
            };
            
            const result = await this.makeRequest(
                `/repos/${this.owner}/${this.repo}/pages`,
                'POST',
                pagesConfig
            );
            
            return result;
        } catch (error) {
            if (error.message.includes('409')) {
                console.log('📄 GitHub Pages already enabled');
                // Get existing pages info
                const existingPages = await this.makeRequest(`/repos/${this.owner}/${this.repo}/pages`);
                return existingPages;
            }
            throw error;
        }
    }

    async createOrUpdateFile(filePath, content, message) {
        try {
            // First, try to get the file to see if it exists
            let sha = null;
            try {
                const existingFile = await this.makeRequest(`/repos/${this.owner}/${this.repo}/contents/${filePath}`);
                sha = existingFile.sha;
            } catch (error) {
                // File doesn't exist, that's fine
            }

            const fileData = {
                message: message,
                content: Buffer.from(content).toString('base64'),
                ...(sha && { sha })
            };

            const result = await this.makeRequest(
                `/repos/${this.owner}/${this.repo}/contents/${filePath}`,
                'PUT',
                fileData
            );

            return result;
        } catch (error) {
            console.error(`Failed to update ${filePath}:`, error.message);
            throw error;
        }
    }

    async deployToGitHubPages() {
        try {
            console.log('🚀 Starting GitHub Pages deployment...');

            // Enable GitHub Pages
            console.log('📄 Setting up GitHub Pages...');
            const pagesInfo = await this.enableGitHubPages();
            
            // Create CNAME file for custom domain
            const customDomain = 'climate.johnnycchung.com';
            console.log(`🌍 Setting up custom domain: ${customDomain}`);
            await this.createOrUpdateFile('CNAME', customDomain, 'Add custom domain for GitHub Pages');

            // Update index.html with GitHub Pages friendly paths
            console.log('📝 Updating file paths for GitHub Pages...');
            let indexContent = fs.readFileSync('./public/index.html', 'utf8');
            
            // Update paths to be relative
            indexContent = indexContent.replace(/href="\//g, 'href="./');
            indexContent = indexContent.replace(/src="\//g, 'src="./');
            
            await this.createOrUpdateFile('index.html', indexContent, 'Update index.html for GitHub Pages');

            // Deploy all other files
            const publicDir = './public';
            const files = this.getAllFiles(publicDir);
            
            for (const file of files) {
                if (file.name === 'index.html') continue; // Already handled
                
                console.log(`📁 Uploading ${file.path}...`);
                await this.createOrUpdateFile(
                    file.path,
                    file.content,
                    `Deploy ${file.name} to GitHub Pages`
                );
            }

            const githubPagesUrl = `https://${this.owner}.github.io/${this.repo}`;
            const customDomainUrl = `https://${customDomain}`;
            
            console.log('\n🎉 GitHub Pages deployment completed!');
            console.log(`📱 GitHub Pages URL: ${githubPagesUrl}`);
            console.log(`🌍 Custom Domain URL: ${customDomainUrl}`);
            console.log('\n⚠️  Note: DNS setup required for custom domain:');
            console.log(`   Add CNAME record: climate.johnnycchung.com → ${this.owner}.github.io`);

            return { githubPagesUrl, customDomainUrl, pagesInfo };

        } catch (error) {
            console.error('❌ GitHub Pages deployment failed:', error.message);
            throw error;
        }
    }

    getAllFiles(dir, basePath = '') {
        const files = [];
        const entries = fs.readdirSync(dir);

        for (const entry of entries) {
            const fullPath = path.join(dir, entry);
            const stat = fs.statSync(fullPath);
            const relativePath = basePath ? `${basePath}/${entry}` : entry;

            if (stat.isDirectory()) {
                files.push(...this.getAllFiles(fullPath, relativePath));
            } else {
                const content = fs.readFileSync(fullPath, 'utf8');
                files.push({
                    name: entry,
                    path: relativePath,
                    content: content
                });
            }
        }

        return files;
    }
}

// Alternative: Netlify deployment
class NetlifyDeployer {
    constructor(token) {
        this.token = token;
        this.baseUrl = 'https://api.netlify.com';
    }

    async deployToNetlify() {
        console.log('🚀 Starting Netlify deployment...');
        
        // Create zip file of public directory
        const { execSync } = require('child_process');
        execSync('cd public && zip -r ../site.zip .');
        
        const siteData = fs.readFileSync('./site.zip');
        
        // Deploy to Netlify
        const deployment = await this.makeRequest('/v1/sites', 'POST', {
            files: {
                '/': siteData.toString('base64')
            }
        });
        
        console.log(`✅ Netlify deployment: ${deployment.ssl_url}`);
        return deployment;
    }

    async makeRequest(endpoint, method = 'GET', data = null) {
        // Similar implementation to GitHub API requests
        // Implementation details...
    }
}

// Main execution
async function main() {
    const deployMethod = process.argv[2] || 'github';
    
    if (deployMethod === 'github') {
        const token = process.env.GITHUB_TOKEN;
        if (!token) {
            console.error('❌ GITHUB_TOKEN environment variable required');
            console.log('Get your token from: https://github.com/settings/tokens');
            process.exit(1);
        }
        
        const deployer = new GitHubPagesDeployer(token, 'jiahknee5', 'climate-risk-analysis');
        await deployer.deployToGitHubPages();
        
    } else if (deployMethod === 'netlify') {
        const token = process.env.NETLIFY_TOKEN;
        if (!token) {
            console.error('❌ NETLIFY_TOKEN environment variable required');
            process.exit(1);
        }
        
        const deployer = new NetlifyDeployer(token);
        await deployer.deployToNetlify();
    }
}

if (require.main === module) {
    main();
}

module.exports = { GitHubPagesDeployer, NetlifyDeployer };