#!/usr/bin/env python3
"""
Deploy climate risk analysis to main domain johnnycchung.com
This script fixes paths and prepares files for deployment to the root domain
"""

import os
import re
from pathlib import Path

def fix_localhost_links(content, file_path):
    """Fix localhost and relative path issues"""
    
    # Remove localhost references
    content = re.sub(r'http://localhost:\d+/', '', content)
    content = re.sub(r'https://localhost:\d+/', '', content)
    
    # Fix common localhost patterns
    content = content.replace('localhost:8080', 'johnnycchung.com')
    content = content.replace('localhost:3000', 'johnnycchung.com')
    content = content.replace('localhost:8000', 'johnnycchung.com')
    
    # Ensure relative paths for same-domain resources
    if file_path.suffix == '.html':
        # Fix relative links to work from root domain
        content = re.sub(r'href="\./', 'href="', content)
        content = re.sub(r'src="\./', 'src="', content)
        
        # Fix absolute paths to be relative
        content = re.sub(r'href="/', 'href="', content)
        content = re.sub(r'src="/', 'src="', content)
    
    return content

def prepare_for_main_domain():
    """Prepare all files for deployment to johnnycchung.com"""
    
    public_dir = Path("public")
    
    print("🚀 Preparing files for johnnycchung.com deployment...")
    
    # Process all HTML files
    html_files = list(public_dir.glob("*.html"))
    
    for html_file in html_files:
        print(f"📝 Processing {html_file.name}...")
        
        try:
            # Read file
            content = html_file.read_text(encoding='utf-8')
            
            # Fix links
            content = fix_localhost_links(content, html_file)
            
            # Write back
            html_file.write_text(content, encoding='utf-8')
            
            print(f"✅ Fixed {html_file.name}")
            
        except Exception as e:
            print(f"❌ Error processing {html_file.name}: {e}")
    
    # Create .htaccess for proper routing (if needed)
    htaccess_content = """# Climate Risk Analysis - Main Domain Setup
RewriteEngine On

# Handle climate risk app routing
RewriteRule ^climate/?$ index.html [L]
RewriteRule ^climate/(.*)$ $1 [L]

# Ensure HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Add security headers
<IfModule mod_headers.c>
    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options DENY
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
</IfModule>

# Enable compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript application/json
</IfModule>
"""
    
    htaccess_file = public_dir / ".htaccess"
    htaccess_file.write_text(htaccess_content)
    print("✅ Created .htaccess file")
    
    print("\n🎉 Files prepared for johnnycchung.com deployment!")
    print("📋 Next steps:")
    print("1. Upload public/ contents to johnnycchung.com root directory")
    print("2. Or use GitHub Pages with johnnycchung.com as custom domain")
    print("3. Test all 4 climate applications")

def create_subdirectory_structure():
    """Create climate subdirectory structure for johnnycchung.com/climate/"""
    
    print("🗂️  Creating /climate/ subdirectory structure...")
    
    # Create climate subdirectory
    climate_dir = Path("climate_subdirectory")
    climate_dir.mkdir(exist_ok=True)
    
    public_dir = Path("public")
    
    # Copy all files to climate subdirectory
    for file_path in public_dir.rglob("*"):
        if file_path.is_file():
            relative_path = file_path.relative_to(public_dir)
            dest_path = climate_dir / relative_path
            
            # Create parent directories
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy and fix file
            content = file_path.read_text(encoding='utf-8')
            content = fix_localhost_links(content, file_path)
            
            dest_path.write_text(content, encoding='utf-8')
    
    print("✅ Climate subdirectory created")
    print("📁 Upload climate_subdirectory/ contents to johnnycchung.com/climate/")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "subdirectory":
        create_subdirectory_structure()
    else:
        prepare_for_main_domain()