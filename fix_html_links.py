import os
import shutil
from bs4 import BeautifulSoup

def fix_html_links(root_dir):
    """
    This script finds all HTML files in a directory and fixes their links
    to CSS and JavaScript files by converting relative paths to absolute paths.
    """
    print("Starting to fix HTML link paths...")
    
    # These are the paths to the CSS and JS files that need to be corrected.
    css_path = 'dist/viewer.css'
    js_path = 'dist/viewer.js'
    
    for subdir, dirs, files in os.walk(root_dir):
        for filename in files:
            # Only process HTML files.
            if filename.endswith('.html'):
                filepath = os.path.join(subdir, filename)
                print(f"Processing: {filepath}")

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        soup = BeautifulSoup(f, 'html.parser')
                    
                    changed = False
                    
                    # Find and fix the main CSS link.
                    link_tag = soup.find('link', href=lambda href: href and css_path in href)
                    if link_tag and not link_tag['href'].startswith('/'):
                        link_tag['href'] = '/' + link_tag['href']
                        changed = True
                        print(f"  - Fixed CSS link in {filename}.")
                        
                    # Find and fix the main JavaScript script tag.
                    script_tag = soup.find('script', src=lambda src: src and js_path in src)
                    if script_tag and not script_tag['src'].startswith('/'):
                        script_tag['src'] = '/' + script_tag['src']
                        changed = True
                        print(f"  - Fixed JavaScript link in {filename}.")
                        
                    # Save the changes if any were made.
                    if changed:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(str(soup))
                        print(f"  - Fixed links in {filename}. Changes saved.")
                    else:
                        print(f"  - No changes needed in {filename}")
                
                except Exception as e:
                    print(f"  - ERROR processing file {filepath}: {e}")

if __name__ == "__main__":
    project_root = "." 
    fix_html_links(project_root)
    print("\nHTML link fixing complete.")
