#!/usr/bin/env python3
"""
GitHub Pages Setup via API - Climate Risk Analysis
Requires GitHub personal access token with 'repo' scope
"""

import requests
import json
import os
import base64
from pathlib import Path

class GitHubPagesSetup:
    def __init__(self, token, owner="jiahknee5", repo="climate-risk-analysis"):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Climate-Risk-Deployer/1.0"
        }
    
    def make_request(self, endpoint, method="GET", data=None):
        """Make authenticated GitHub API request"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers)
            
            response.raise_for_status()
            return response.json() if response.content else {}
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 409 and "already exists" in response.text:
                print(f"ℹ️  Resource already exists: {endpoint}")
                return response.json() if response.content else {}
            else:
                print(f"❌ API Error {response.status_code}: {response.text}")
                raise e
        except Exception as e:
            print(f"❌ Request failed: {e}")
            raise e
    
    def enable_github_pages(self):
        """Enable GitHub Pages for the repository"""
        print("📄 Enabling GitHub Pages...")
        
        pages_config = {
            "source": {
                "branch": "main",
                "path": "/"
            },
            "build_type": "legacy"
        }
        
        try:
            result = self.make_request(f"/repos/{self.owner}/{self.repo}/pages", "POST", pages_config)
            print(f"✅ GitHub Pages enabled: {result.get('html_url', 'Success')}")
            return result
        except Exception as e:
            # Check if Pages already exists
            try:
                existing = self.make_request(f"/repos/{self.owner}/{self.repo}/pages")
                print(f"ℹ️  GitHub Pages already enabled: {existing.get('html_url')}")
                return existing
            except:
                print(f"❌ Failed to enable GitHub Pages: {e}")
                raise e
    
    def setup_custom_domain(self, domain="climate.johnnycchung.com"):
        """Set up custom domain for GitHub Pages"""
        print(f"🌍 Setting up custom domain: {domain}")
        
        # Create CNAME file in repository
        cname_content = domain
        cname_data = {
            "message": "Add CNAME for custom domain",
            "content": base64.b64encode(cname_content.encode()).decode()
        }
        
        try:
            # Check if CNAME already exists
            try:
                existing_cname = self.make_request(f"/repos/{self.owner}/{self.repo}/contents/CNAME")
                cname_data["sha"] = existing_cname["sha"]
                print("ℹ️  Updating existing CNAME file")
            except:
                print("📝 Creating new CNAME file")
            
            result = self.make_request(f"/repos/{self.owner}/{self.repo}/contents/CNAME", "PUT", cname_data)
            print(f"✅ CNAME file created/updated")
            
            # Update Pages configuration with custom domain
            pages_update = {
                "cname": domain,
                "https_enforced": True
            }
            
            pages_result = self.make_request(f"/repos/{self.owner}/{self.repo}/pages", "PUT", pages_update)
            print(f"✅ Custom domain configured: {domain}")
            
            return result
            
        except Exception as e:
            print(f"❌ Custom domain setup failed: {e}")
            raise e
    
    def update_repository_files(self):
        """Update repository files for GitHub Pages compatibility"""
        print("📁 Updating repository files for GitHub Pages...")
        
        # Files to update/create for GitHub Pages
        files_to_update = [
            {
                "path": "index.html",
                "source": "public/index.html",
                "message": "Update index.html for GitHub Pages"
            },
            {
                "path": "hurricane-risk-map.html", 
                "source": "public/hurricane-risk-map.html",
                "message": "Add hurricane risk map for GitHub Pages"
            },
            {
                "path": "hurricane-season-2026.html",
                "source": "public/hurricane-season-2026.html", 
                "message": "Add hurricane season simulation for GitHub Pages"
            },
            {
                "path": "climate-scenarios.html",
                "source": "public/climate-scenarios.html",
                "message": "Add climate scenarios comparison for GitHub Pages"
            },
            {
                "path": "real-estate-risk.html",
                "source": "public/real-estate-risk.html",
                "message": "Add enhanced climate risk analysis for GitHub Pages"
            },
            {
                "path": "climate-use-case-tests.md",
                "source": "public/climate-use-case-tests.md",
                "message": "Add use case tests documentation for GitHub Pages"
            }
        ]
        
        for file_info in files_to_update:
            try:
                # Read source file
                source_path = Path(file_info["source"])
                if not source_path.exists():
                    print(f"⚠️  Source file not found: {source_path}")
                    continue
                
                content = source_path.read_text(encoding='utf-8')
                
                # For HTML files, update paths to be GitHub Pages compatible
                if file_info["path"].endswith('.html'):
                    # Update relative paths for GitHub Pages
                    content = content.replace('href="/', 'href="./')
                    content = content.replace('src="/', 'src="./')
                    content = content.replace("href='/", "href='./")
                    content = content.replace("src='/", "src='./")
                
                # Prepare file data for GitHub API
                file_data = {
                    "message": file_info["message"],
                    "content": base64.b64encode(content.encode()).decode()
                }
                
                # Check if file already exists
                try:
                    existing_file = self.make_request(f"/repos/{self.owner}/{self.repo}/contents/{file_info['path']}")
                    file_data["sha"] = existing_file["sha"]
                    print(f"📝 Updating {file_info['path']}")
                except:
                    print(f"📝 Creating {file_info['path']}")
                
                # Update/create file
                result = self.make_request(f"/repos/{self.owner}/{self.repo}/contents/{file_info['path']}", "PUT", file_data)
                print(f"✅ {file_info['path']} updated successfully")
                
            except Exception as e:
                print(f"❌ Failed to update {file_info['path']}: {e}")
                continue
    
    def deploy_to_github_pages(self, custom_domain="climate.johnnycchung.com"):
        """Complete GitHub Pages deployment process"""
        print("🚀 Starting GitHub Pages deployment...")
        print(f"📍 Repository: {self.owner}/{self.repo}")
        print(f"🌍 Custom Domain: {custom_domain}")
        print()
        
        try:
            # Step 1: Update repository files
            self.update_repository_files()
            print()
            
            # Step 2: Enable GitHub Pages
            pages_info = self.enable_github_pages()
            print()
            
            # Step 3: Set up custom domain
            self.setup_custom_domain(custom_domain)
            print()
            
            # Display results
            github_url = f"https://{self.owner}.github.io/{self.repo}"
            custom_url = f"https://{custom_domain}"
            
            print("🎉 GitHub Pages deployment completed!")
            print(f"📱 GitHub Pages URL: {github_url}")
            print(f"🌍 Custom Domain URL: {custom_url}")
            print()
            print("📋 Next Steps:")
            print(f"1. Add DNS CNAME record: {custom_domain} → {self.owner}.github.io")
            print("2. Wait 5-10 minutes for DNS propagation")
            print("3. GitHub will automatically issue SSL certificate")
            print("4. Test all 4 climate applications")
            print()
            print("🧪 Test URLs:")
            print(f"   • Main: {custom_url}")
            print(f"   • Hurricane Risk Map: {custom_url}/hurricane-risk-map.html")
            print(f"   • Hurricane Season: {custom_url}/hurricane-season-2026.html")
            print(f"   • Climate Scenarios: {custom_url}/climate-scenarios.html")
            print(f"   • Enhanced Analysis: {custom_url}/real-estate-risk.html")
            
            return {
                "github_url": github_url,
                "custom_url": custom_url,
                "pages_info": pages_info
            }
            
        except Exception as e:
            print(f"❌ GitHub Pages deployment failed: {e}")
            raise e

def main():
    """Main deployment function"""
    print("🚀 GitHub Pages API Deployment Tool")
    print("=" * 50)
    
    # Get GitHub token
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("❌ GITHUB_TOKEN environment variable required")
        print()
        print("To get a token:")
        print("1. Go to https://github.com/settings/tokens")
        print("2. Create a new token with 'repo' scope")
        print("3. Export it: export GITHUB_TOKEN='your_token_here'")
        return False
    
    # Initialize deployer
    deployer = GitHubPagesSetup(token)
    
    # Deploy to GitHub Pages
    try:
        result = deployer.deploy_to_github_pages()
        print("✅ Deployment successful!")
        return True
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)