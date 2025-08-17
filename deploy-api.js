#!/usr/bin/env node
/**
 * Vercel API Deployment Script
 * Deploy climate risk analysis platform via REST API
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

class VercelAPIDeployer {
    constructor(token) {
        this.token = token;
        this.baseUrl = 'https://api.vercel.com';
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
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json',
                    'User-Agent': 'Climate-Risk-Deployer/1.0'
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
                        const parsed = JSON.parse(responseData);
                        if (res.statusCode >= 200 && res.statusCode < 300) {
                            resolve(parsed);
                        } else {
                            reject(new Error(`API Error ${res.statusCode}: ${parsed.error?.message || responseData}`));
                        }
                    } catch (e) {
                        reject(new Error(`Parse Error: ${responseData}`));
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

    async getProjectInfo() {
        try {
            const projects = await this.makeRequest('/v9/projects');
            const climateProject = projects.projects.find(p => 
                p.name === 'climate-deployment' || p.name.includes('climate')
            );
            return climateProject;
        } catch (error) {
            console.log('No existing project found, will create new one');
            return null;
        }
    }

    async createDeployment(files) {
        const deploymentData = {
            name: 'climate-risk-analysis',
            files: files,
            projectSettings: {
                framework: null,
                buildCommand: null,
                outputDirectory: 'public',
                installCommand: null
            },
            target: 'production',
            gitSource: {
                type: 'github',
                repo: 'jiahknee5/climate-risk-analysis',
                ref: 'main'
            }
        };

        try {
            const result = await this.makeRequest('/v13/deployments', 'POST', deploymentData);
            return result;
        } catch (error) {
            console.error('Deployment failed:', error.message);
            throw error;
        }
    }

    async setupCustomDomain(projectId, domain) {
        try {
            // Add domain to project
            const domainResult = await this.makeRequest(
                `/v10/projects/${projectId}/domains`,
                'POST',
                { name: domain }
            );
            
            console.log(`Domain ${domain} added to project`);
            
            // Verify domain
            const verifyResult = await this.makeRequest(
                `/v9/projects/${projectId}/domains/${domain}/verify`,
                'POST'
            );
            
            return { domainResult, verifyResult };
        } catch (error) {
            console.error('Domain setup failed:', error.message);
            throw error;
        }
    }

    readFilesFromDirectory(dir) {
        const files = [];
        
        function readDir(currentDir, relativePath = '') {
            const entries = fs.readdirSync(currentDir);
            
            for (const entry of entries) {
                const fullPath = path.join(currentDir, entry);
                const stat = fs.statSync(fullPath);
                const relativeFilePath = path.join(relativePath, entry);
                
                if (stat.isDirectory()) {
                    readDir(fullPath, relativeFilePath);
                } else {
                    const content = fs.readFileSync(fullPath);
                    files.push({
                        file: relativeFilePath.replace(/\\/g, '/'), // Normalize path separators
                        data: content.toString('base64')
                    });
                }
            }
        }
        
        readDir(dir);
        return files;
    }

    async deploy() {
        try {
            console.log('🚀 Starting API-based deployment...');
            
            // Read files from public directory
            console.log('📁 Reading files from public directory...');
            const files = this.readFilesFromDirectory('./public');
            console.log(`Found ${files.length} files to deploy`);
            
            // Create deployment
            console.log('🌐 Creating deployment...');
            const deployment = await this.createDeployment(files);
            
            console.log(`✅ Deployment created: ${deployment.url}`);
            console.log(`🔗 Deployment ID: ${deployment.id}`);
            
            return deployment;
            
        } catch (error) {
            console.error('❌ Deployment failed:', error.message);
            throw error;
        }
    }
}

// Main execution
async function main() {
    // Check for token in environment or prompt
    const token = process.env.VERCEL_TOKEN;
    
    if (!token) {
        console.error('❌ VERCEL_TOKEN environment variable required');
        console.log('Get your token from: https://vercel.com/account/tokens');
        process.exit(1);
    }
    
    const deployer = new VercelAPIDeployer(token);
    
    try {
        const deployment = await deployer.deploy();
        
        // Optionally set up custom domain
        if (process.argv.includes('--domain')) {
            const domainIndex = process.argv.indexOf('--domain');
            const customDomain = process.argv[domainIndex + 1];
            
            if (customDomain && deployment.projectId) {
                console.log(`🌍 Setting up custom domain: ${customDomain}`);
                await deployer.setupCustomDomain(deployment.projectId, customDomain);
            }
        }
        
        console.log('\n🎉 Deployment completed successfully!');
        console.log(`📱 Live URL: ${deployment.url}`);
        
    } catch (error) {
        console.error('\n💥 Deployment failed:', error.message);
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}

module.exports = VercelAPIDeployer;