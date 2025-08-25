import os
from bs4 import BeautifulSoup

def fix_image_paths_to_absolute(root_dir):
    """
    This script finds all HTML files in a directory and replaces their
    Readymag-hosted image URLs with local, absolute paths starting from the root.
    """
    # The absolute path where all the ripped images are stored, starting with '/'.
    image_base_path = "/img/6666f57326be89003f9494ae/5214402"
    
    print("Starting to convert image links to absolute paths...")
    
    # Walk through all files and directories in the project.
    for subdir, dirs, files in os.walk(root_dir):
        for filename in files:
            # Only process HTML files.
            if filename.endswith(".html"):
                filepath = os.path.join(subdir, filename)
                print(f"Processing: {filepath}")

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        soup = BeautifulSoup(f, 'html.parser')

                    changed = False
                    # Find all image tags in the HTML.
                    for img_tag in soup.find_all('img'):
                        img_src = img_tag.get('src')
                        
                        # Check if the image source is a local relative path.
                        if img_src and "img/6666" in img_src and not img_src.startswith('/'):
                            # Construct the new, correct absolute path.
                            new_src = "/" + img_src
                            img_tag['src'] = new_src
                            changed = True
                            print(f"  - Converted relative path to absolute: {new_src}")

                    # Save the changes if any links were fixed.
                    if changed:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(str(soup))
                        print(f"Finished processing {filepath}. Changes saved.")
                    else:
                        print(f"Finished processing {filepath}. No changes needed.")

                except Exception as e:
                    print(f"  - ERROR processing file {filepath}: {e}")

if __name__ == "__main__":
    # The root directory of your project.
    project_root = "." 
    fix_image_paths_to_absolute(project_root)
    print("\nImage link fixing complete.")
