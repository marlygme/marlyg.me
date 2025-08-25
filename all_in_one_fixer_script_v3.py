import os
import re
from bs4 import BeautifulSoup

def fix_all_html_files(root_dir):
    """
    This script fixes the hardcoded relative paths in HTML files from a Readymag export.
    It ensures all CSS, JS, and image links are absolute paths, and it cleans up
    unnecessary Readymag-specific code that causes issues on external hosts.
    """
    print("Starting a super-robust fix on all HTML files...")
    
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
            if filename.endswith('.html'):
                filepath = os.path.join(subdir, filename)
                print(f"\nProcessing: {filepath}")
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        soup = BeautifulSoup(content, 'html.parser')
                    
                    changed = False
                    
                    # Ensure the file has a complete HTML structure.
                    if not soup.find('html'):
                        new_soup = BeautifulSoup('<html><head></head><body></body></html>', 'html.parser')
                        for tag in soup.contents:
                            new_soup.body.append(tag)
                        soup = new_soup
                        changed = True
                        print("  - Wrapped incomplete HTML in <html> and <body> tags.")
                    
                    # Replace the head section with the correct one from index.html.
                    if soup.head:
                        original_title_tag = soup.title
                        soup.head.replace_with(correct_head_content)
                        if original_title_tag and soup.head:
                            soup.head.insert(0, original_title_tag)
                        changed = True
                        print("  - Replaced existing <head> section.")
                    else:
                        new_head = soup.new_tag('head')
                        for content_tag in correct_head_content.contents:
                            new_head.append(content_tag)
                        if soup.html:
                            soup.html.insert(0, new_head)
                            changed = True
                            print("  - Added missing <head> section.")

                    # Correct all internal paths to be absolute, starting from the root.
                    for tag in soup.find_all(['img', 'script', 'link']):
                        if tag.name == 'img' and tag.get('src'):
                            # Use a more robust regex to find and replace relative paths
                            if re.match(r'^(?!/|http)', tag['src']):
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

                    # Remove old, broken Readymag code.
                    for script in soup.find_all('script'):
                        if script.get('src') and ('rmcdn' in script['src'] or 'screenshoter.js' in script['src']):
                            script.decompose()
                            changed = True
                            print("  - Removed a problematic Readymag script link.")

                    for link_tag in soup.find_all('link', href=True):
                        if 'rmcdn' in link_tag['href']:
                            link_tag.decompose()
                            changed = True
                            print("  - Removed a problematic Readymag link.")

                    for meta_tag in soup.find_all('meta', property='og:image'):
                         if meta_tag.get('content') and 'rmcdn' in meta_tag['content']:
                            meta_tag.decompose()
                            changed = True
                            print("  - Removed a problematic Open Graph meta tag.")

                    # Save the cleaned file.
                    if changed:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(str(soup))
                        print(f"  - Changes saved to {filename}.")
                    else:
                        print(f"  - No significant changes were made to {filename}.")
                
                except Exception as e:
                    print(f"  - ERROR processing file {filepath}: {e}")

    # After processing, add the redirects file to ensure clean URLs.
    redirects_content = """
# Forcing all www traffic to the root domain.
https://www.marlyg.me/* https://marlyg.me/:splat 301!

# Handling clean URL redirects for pages.
/projects /projects.html 301!
/webdesign /webdesign.html 301!
/about /about.html 301!
    """
    redirects_path = os.path.join(root_dir, '_redirects')
    try:
        with open(redirects_path, 'w') as f:
            f.write(redirects_content.strip())
        print(f"\nCreated _redirects file at {redirects_path}")
    except Exception as e:
        print(f"\nError creating _redirects file: {e}")

if __name__ == "__main__":
    project_root = "." 
    fix_all_html_files(project_root)
    print("\nWebsite file fixing complete. Please commit and push changes to GitHub.")
