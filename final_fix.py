import os
import shutil
from bs4 import BeautifulSoup, Comment

def fix_all_html_files(root_dir):
    """
    This script performs a full fix on HTML files by ensuring a correct <head>
    section is present and that all file paths are absolute and correct.
    It also removes old, problematic Readymag-specific code and handles
    incomplete HTML fragments.
    """
    print("Starting a super-robust fix on all HTML files...")
    
    # Path to the main stylesheet and scripts from the dist folder
    main_css_path = '/dist/viewer.css'
    custom_fonts_path = '/dist/css/custom_fonts.css'
    main_js_path = '/dist/viewer.js'
    screenshoter_path = 'screenshoter.js' # This is a known Readymag script to remove

    index_path = os.path.join(root_dir, 'index.html')
    if not os.path.exists(index_path):
        print("Error: index.html not found in the root directory. Aborting.")
        return

    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            soup_index = BeautifulSoup(f.read(), 'html.parser')
            correct_head_content = soup_index.head
    except Exception as e:
        print(f"Error reading index.html: {e}. Aborting.")
        return

    for subdir, dirs, files in os.walk(root_dir):
        for filename in files:
            # Only process HTML files, and skip index.html as it's the template.
            if filename.endswith('.html') and filename != 'index.html':
                filepath = os.path.join(subdir, filename)
                print(f"\nProcessing: {filepath}")
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        soup = BeautifulSoup(content, 'html.parser')
                    
                    changed = False
                    
                    # If there's no <html> tag, it's an incomplete file.
                    # We'll wrap the entire content in <html> and <body> tags.
                    if not soup.find('html'):
                        body_content = soup.contents[0]
                        new_html = BeautifulSoup('<html><head></head><body></body></html>', 'html.parser')
                        new_html.body.append(body_content)
                        soup = new_html
                        changed = True
                        print("  - Wrapped incomplete HTML in <html> and <body> tags.")
                    
                    # Remove any old <head> and replace with the correct version.
                    if soup.head:
                        soup.head.replace_with(correct_head_content)
                        changed = True
                        print("  - Replaced existing <head> section.")
                    else:
                        new_head = soup.new_tag('head')
                        for content_tag in correct_head_content.contents:
                            new_head.append(content_tag)
                        soup.html.insert(0, new_head)
                        changed = True
                        print("  - Added missing <head> section.")

                    # Remove other problematic tags.
                    for script in soup.find_all('script'):
                        if script.get('src') and 'rmcdn' in script['src']:
                            script.decompose()
                            changed = True
                            print("  - Removed Readymag script link.")
                    
                    for link_tag in soup.find_all('link', href=True):
                        if 'rmcdn' in link_tag['href']:
                            link_tag.decompose()
                            changed = True
                            print("  - Removed Readymag link.")

                    # Ensure all CSS, JS and image paths are absolute from the root.
                    # This is the most crucial step for fixing your issues.
                    for tag in soup.find_all(['img', 'script', 'link']):
                        if tag.name == 'img' and tag.get('src'):
                            if not tag['src'].startswith('/'):
                                tag['src'] = '/' + tag['src']
                                changed = True
                                print(f"  - Converted relative image path to absolute: {tag['src']}")
                        elif tag.name == 'script' and tag.get('src'):
                             if not tag['src'].startswith('/') and 'dist' in tag['src']:
                                tag['src'] = '/' + tag['src']
                                changed = True
                                print(f"  - Converted relative script path to absolute: {tag['src']}")
                        elif tag.name == 'link' and tag.get('href'):
                            if not tag['href'].startswith('/') and 'dist' in tag['href']:
                                tag['href'] = '/' + tag['href']
                                changed = True
                                print(f"  - Converted relative CSS link path to absolute: {tag['href']}")
                                
                    if changed:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(str(soup))
                        print(f"  - Changes saved to {filename}.")
                    else:
                        print(f"  - No significant changes were made to {filename}.")

                except Exception as e:
                    print(f"  - ERROR processing file {filepath}: {e}")

if __name__ == "__main__":
    project_root = "." 
    fix_all_html_files(project_root)
    print("\nWebsite file fixing complete. Please commit and push changes to GitHub.")
