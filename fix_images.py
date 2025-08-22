import os
from bs4 import BeautifulSoup

def fix_image_paths(root_dir):
    """
    This script finds all HTML files in a directory and replaces their
    Readymag-hosted image URLs with local, relative paths.
    """
    # The base path where all the ripped images are stored.
    # We get this from the user's provided folder structure.
    image_base_path = "img/6666f57326be89003f9494ae/5214402"

    print("Starting to fix image links...")
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
                        # Check if the image source is a Readymag URL.
                        if img_src and "i-p.rmcdn.net" in img_src:
                            # Extract the unique file ID from the URL.
                            # Example URL: https://.../image-0ded3fb1-3cfa...png
                            filename_from_url = img_src.split('/')[-1].split('.')[0]
                            
                            # Find the matching local image file in the images folder.
                            local_image_file = find_local_image(root_dir, image_base_path, filename_from_url)

                            if local_image_file:
                                # Construct the new, correct relative path.
                                new_src = os.path.join(image_base_path, local_image_file).replace('\\', '/')
                                img_tag['src'] = new_src
                                changed = True
                                print(f"  - Replaced {img_src} with {new_src}")
                            else:
                                print(f"  - WARNING: Could not find a local file for {img_src}")

                    # Save the changes if any links were fixed.
                    if changed:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(str(soup))
                        print(f"Finished processing {filepath}. Changes saved.")
                    else:
                        print(f"Finished processing {filepath}. No changes needed.")

                except Exception as e:
                    print(f"  - ERROR processing file {filepath}: {e}")

def find_local_image(root_dir, image_base_path, filename_part):
    """
    Helper function to find the local image file that matches the Readymag URL.
    """
    full_image_dir = os.path.join(root_dir, image_base_path)
    if not os.path.exists(full_image_dir):
        print(f"  - ERROR: Image directory {full_image_dir} not found. Check your file paths.")
        return None

    for f in os.listdir(full_image_dir):
        if filename_part in f:
            return f
    return None

if __name__ == "__main__":
    # The root directory of your project.
    project_root = "." 
    fix_image_paths(project_root)
    print("\nImage link fixing complete.")
