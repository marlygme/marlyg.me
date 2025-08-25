import os
import shutil
from bs4 import BeautifulSoup

def fix_website_files(root_dir):
    """
    This script finds all HTML files and ensures they have the correct links
    to the main CSS and JavaScript files, and that their paths are absolute.
    It also removes problematic, Readymag-specific HTML elements and scripts.
    """
    print("Starting final website file fix...")
    
    # We will look for these specific file names to fix.
    css_file = 'dist/viewer.css'
    js_file = 'dist/viewer.js'
    
    # We will also look for font imports that are broken.
    fonts_file = 'dist/css/custom_fonts.css'

    for subdir, dirs, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith('.html'):
                filepath = os.path.join(subdir, filename)
                print(f"\nProcessing: {filepath}")

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        soup = BeautifulSoup(f.read(), 'html.parser')
                    
                    changed = False
                    
                    # Fix the main CSS file link.
                    link_tag = soup.find('link', href=lambda href: href and css_file in href)
                    if link_tag and not link_tag['href'].startswith('/'):
                        link_tag['href'] = '/' + link_tag['href']
                        changed = True
                        print(f"  - Fixed main CSS link in {filename}.")

                    # Fix the main JavaScript file link.
                    script_tag = soup.find('script', src=lambda src: src and js_file in src)
                    if script_tag and not script_tag['src'].startswith('/'):
                        script_tag['src'] = '/' + script_tag['src']
                        changed = True
                        print(f"  - Fixed main JavaScript link in {filename}.")

                    # Fix the custom fonts link.
                    fonts_link = soup.find('link', href=lambda href: href and fonts_file in href)
                    if fonts_link and not fonts_link['href'].startswith('/'):
                        fonts_link['href'] = '/' + fonts_link['href']
                        changed = True
                        print(f"  - Fixed custom fonts link in {filename}.")

                    # Fix image paths. This is a redundant check to ensure all images are fixed.
                    for img_tag in soup.find_all('img'):
                        img_src = img_tag.get('src')
                        if img_src and not img_src.startswith('/'):
                            img_tag['src'] = '/' + img_src
                            changed = True
                            print(f"  - Converted relative image path to absolute: {img_src}")

                    # Remove the old screenshoter script, as it's from Readymag.
                    screenshoter_script = soup.find('script', src=lambda src: src and 'screenshoter.js' in src)
                    if screenshoter_script:
                        screenshoter_script.decompose()
                        changed = True
                        print("  - Removed screenshoter.js script.")

                    # Remove the old, broken typekit link.
                    typekit_link = soup.find('link', href=lambda href: href and 'typekit' in href)
                    if typekit_link:
                        typekit_link.decompose()
                        changed = True
                        print("  - Removed broken Typekit link.")

                    # Save the changes.
                    if changed:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(str(soup))
                        print(f"  - Changes saved to {filename}.")
                    else:
                        print(f"  - No changes were made to {filename}.")

                except Exception as e:
                    print(f"  - ERROR processing file {filepath}: {e}")

if __name__ == "__main__":
    project_root = "." 
    fix_website_files(project_root)
    print("\nWebsite file fixing complete.")
