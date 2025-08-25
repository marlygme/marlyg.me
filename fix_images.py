import os
from bs4 import BeautifulSoup

def fix_image_paths(root_dir):
    """
    This script finds all HTML files in a directory and replaces their
    Readymag-hosted image URLs with local, relative paths.
    This version is more robust and handles case-sensitivity and different file extensions.
    """
    # The base path where all the ripped images are stored.
    # The script will search for image files here.
    image_base_path = "img/6666f57326be89003f9494ae/5214402"
    
    print("Starting a super-robust image link fix...")
    
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
                        
                        # We are looking for any source that is a Readymag URL
                        if img_src and "i-p.rmcdn.net" in img_src:
                            # The script extracts the unique file ID from the URL.
                            filename_from_url = img_src.split('/')[-1].split('.')[0]
                            
                            # It then searches the image directory for a matching file.
                            local_image_file = find_local_image_robustly(root_dir, image_base_path, filename_from_url)

                            if local_image_file:
                                # This is where the path is built, ensuring it is a relative path.
                                new_src = os.path.join(image_base_path, local_image_file).replace('\\', '/')
                                img_tag['src'] = new_src
                                changed = True
                                print(f"  - Replaced {img_src} with {new_src}")
                            else:
                                print(f"  - WARNING: Could not find a local file for {img_src}")
                        
                        # Additionally, check for a `srcset` attribute, as Readymag uses this.
                        srcset = img_tag.get('srcset')
                        if srcset and "i-p.rmcdn.net" in srcset:
                            # This is a bit more complex, we'll try to find the base image.
                            # For simplicity, this script will point to a single image source.
                            # You may need to manually adjust `srcset` for responsive images.
                            image_urls = srcset.split(',')
                            first_url = image_urls[0].split(' ')[0]
                            filename_from_url = first_url.split('/')[-1].split('.')[0]
                            
                            local_image_file = find_local_image_robustly(root_dir, image_base_path, filename_from_url)

                            if local_image_file:
                                new_src = os.path.join(image_base_path, local_image_file).replace('\\', '/')
                                img_tag['src'] = new_src
                                # We remove the srcset attribute to avoid broken links.
                                del img_tag['srcset']
                                changed = True
                                print(f"  - Replaced srcset with src: {new_src}")

                    # Save the changes if any links were fixed.
                    if changed:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(str(soup))
                        print(f"Finished processing {filepath}. Changes saved.")
                    else:
                        print(f"Finished processing {filepath}. No changes needed.")

                except Exception as e:
                    print(f"  - ERROR processing file {filepath}: {e}")

def find_local_image_robustly(root_dir, image_base_path, filename_part):
    """
    Helper function to find the local image file, handling case-insensitivity
    and checking for common image file extensions.
    """
    full_image_dir = os.path.join(root_dir, image_base_path)
    if not os.path.exists(full_image_dir):
        print(f"  - ERROR: Image directory {full_image_dir} not found. Check your file paths.")
        return None

    # Check for common extensions.
    extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp']

    for f in os.listdir(full_image_dir):
        # The script now checks if the filename_part is in the local filename, case-insensitively.
        # It's looking for a match within the first part of the filename before the `_`.
        if filename_part.lower() in f.lower():
            for ext in extensions:
                if f.lower().endswith(ext):
                    return f
    return None

if __name__ == "__main__":
    # The root directory of your project.
    project_root = "." 
    fix_image_paths(project_root)
    print("\nImage link fixing complete.")
