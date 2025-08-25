import os
import shutil
from bs4 import BeautifulSoup

def fix_head_sections_with_index_template(root_dir):
    """
    Copies the complete <head> section from index.html and inserts it into
    all other HTML files to ensure all styling and scripts are correctly linked.
    It is now more robust and can handle incomplete HTML fragments.
    """
    print("Starting to fix head sections across all HTML files...")
    
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

    # Walk through the directory tree.
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
                    if not soup.html:
                        # Find the first child, which should be the article.
                        body_content = soup.contents[0]
                        new_body = BeautifulSoup('<body></body>', 'html.parser').body
                        new_body.append(body_content)
                        
                        new_html = BeautifulSoup('<html></html>', 'html.parser').html
                        new_html.append(new_body)
                        
                        soup = BeautifulSoup(str(new_html), 'html.parser')
                        changed = True
                        print(f"  - Incomplete HTML detected. Wrapping content with <html> and <body> tags.")
                    
                    # Create a new <head> tag with the correct content.
                    new_head = BeautifulSoup('<html></html>', 'html.parser').new_tag('head')
                    for content_tag in correct_head_content.contents:
                        # Append the content of the head from the index file.
                        new_head.append(content_tag)
                        
                    # Remove any existing head and replace it with the new one.
                    if soup.head:
                        soup.head.replace_with(new_head)
                    else:
                        # Insert the new head tag at the beginning of the <html> tag.
                        soup.html.insert(0, new_head)
                    
                    # Check and fix any hardcoded Readymag links.
                    for script_tag in soup.find_all('script', src=True):
                        if 'rmcdn' in script_tag['src']:
                            script_tag.decompose()
                            changed = True
                            print(f"  - Removed a hardcoded Readymag script link.")
                    
                    for link_tag in soup.find_all('link', href=True):
                        if 'rmcdn' in link_tag['href']:
                            link_tag.decompose()
                            changed = True
                            print(f"  - Removed a hardcoded Readymag link.")

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
    # The root directory of your project.
    project_root = "." 
    fix_head_sections_with_index_template(project_root)
    print("\nWebsite file fixing complete.")
