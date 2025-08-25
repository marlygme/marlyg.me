import os
from bs4 import BeautifulSoup

def remove_srcset_from_html(root_dir):
    """
    This script finds all HTML files in a directory and removes the 'srcset'
    attribute from all 'img' tags.
    """
    print("Starting to remove srcset attributes...")
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
                        # Check if the srcset attribute exists and remove it.
                        if 'srcset' in img_tag.attrs:
                            del img_tag['srcset']
                            changed = True
                            print(f"  - Removed srcset from an <img> tag.")

                    # Save the changes if any were made.
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
    remove_srcset_from_html(project_root)
    print("\nsrcset removal complete.")
