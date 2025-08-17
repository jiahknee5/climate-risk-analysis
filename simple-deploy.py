#!/usr/bin/env python3
"""
Simple HTTP deployment server for climate risk analysis
Can be used as a fallback when other deployment methods fail
"""

import http.server
import socketserver
import os
import webbrowser
import threading
import time
from pathlib import Path

class ClimateRiskHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="public", **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()
    
    def do_GET(self):
        # Handle routing for single page applications
        if self.path == '/' or self.path == '/index.html':
            self.path = '/index.html'
        elif not os.path.exists(f"public{self.path}") and not self.path.startswith('/static'):
            self.path = '/index.html'
        
        return super().do_GET()

def deploy_local(port=8080):
    """Deploy locally for testing"""
    print(f"🚀 Starting local deployment on port {port}...")
    
    # Change to deployment directory
    os.chdir(Path(__file__).parent)
    
    with socketserver.TCPServer(("", port), ClimateRiskHandler) as httpd:
        print(f"📱 Server running at: http://localhost:{port}")
        print(f"🌍 Access climate apps at:")
        print(f"   • Main: http://localhost:{port}")
        print(f"   • Hurricane Risk Map: http://localhost:{port}/hurricane-risk-map.html")
        print(f"   • Hurricane Season: http://localhost:{port}/hurricane-season-2026.html") 
        print(f"   • Climate Scenarios: http://localhost:{port}/climate-scenarios.html")
        print(f"   • Enhanced Analysis: http://localhost:{port}/real-estate-risk.html")
        print(f"   • Use Case Tests: http://localhost:{port}/climate-use-case-tests.md")
        print(f"\n⏹️  Press Ctrl+C to stop")
        
        # Open browser automatically
        def open_browser():
            time.sleep(1)
            webbrowser.open(f"http://localhost:{port}")
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

def deploy_to_surge():
    """Deploy to Surge.sh (free static hosting)"""
    import subprocess
    import json
    
    print("🚀 Deploying to Surge.sh...")
    
    try:
        # Check if surge is installed
        subprocess.run(["surge", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📦 Installing Surge.sh...")
        subprocess.run(["npm", "install", "-g", "surge"], check=True)
    
    # Deploy to surge
    domain = "climate-risk-analysis.surge.sh"
    
    try:
        result = subprocess.run([
            "surge", "public", domain
        ], capture_output=True, text=True, input="\n\n")  # Auto-confirm prompts
        
        if result.returncode == 0:
            print(f"✅ Deployed to Surge.sh: https://{domain}")
            return f"https://{domain}"
        else:
            print(f"❌ Surge deployment failed: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ Surge deployment error: {e}")
        return None

def deploy_to_firebase():
    """Deploy to Firebase Hosting"""
    import subprocess
    import json
    
    print("🚀 Deploying to Firebase Hosting...")
    
    # Create firebase.json config
    firebase_config = {
        "hosting": {
            "public": "public",
            "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
            "rewrites": [
                {
                    "source": "**",
                    "destination": "/index.html"
                }
            ],
            "headers": [
                {
                    "source": "**/*.@(js|css)",
                    "headers": [
                        {
                            "key": "Cache-Control",
                            "value": "max-age=31536000"
                        }
                    ]
                }
            ]
        }
    }
    
    with open("firebase.json", "w") as f:
        json.dump(firebase_config, f, indent=2)
    
    try:
        # Initialize if needed
        if not os.path.exists(".firebaserc"):
            subprocess.run(["firebase", "init", "hosting"], check=True)
        
        # Deploy
        result = subprocess.run(["firebase", "deploy"], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Extract URL from output
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Hosting URL:' in line:
                    url = line.split('Hosting URL:')[1].strip()
                    print(f"✅ Deployed to Firebase: {url}")
                    return url
        else:
            print(f"❌ Firebase deployment failed: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ Firebase deployment error: {e}")
        return None

def deploy_to_render():
    """Deploy to Render using their API"""
    import requests
    import zipfile
    import io
    
    print("🚀 Deploying to Render...")
    
    # Create zip of public directory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk('public'):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, 'public')
                zip_file.write(file_path, arcname)
    
    zip_buffer.seek(0)
    
    # Note: This would require Render API token and proper setup
    print("⚠️  Render deployment requires API token setup")
    print("   Visit: https://render.com for manual deployment")
    
    return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        method = sys.argv[1].lower()
        
        if method == "local":
            port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
            deploy_local(port)
        elif method == "surge":
            deploy_to_surge()
        elif method == "firebase":
            deploy_to_firebase()
        elif method == "render":
            deploy_to_render()
        else:
            print("❌ Unknown deployment method")
            print("Usage: python simple-deploy.py [local|surge|firebase|render] [port]")
    else:
        print("🚀 Climate Risk Analysis Deployment Tool")
        print("\nAvailable deployment methods:")
        print("  local [port]  - Local development server (default: 8080)")
        print("  surge         - Deploy to Surge.sh (free)")
        print("  firebase      - Deploy to Firebase Hosting")
        print("  render        - Deploy to Render")
        print("\nExample: python simple-deploy.py local 3000")
        
        # Default to local deployment
        deploy_local()