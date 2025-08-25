import os
from bs4 import BeautifulSoup

def convert_to_relative_paths(root_dir):
    """
    This script finds all HTML files and converts any image source paths
    that start with '/img/' to 'img/' to fix broken links after flattening
    the directory structure.
    """
    print("Starting to convert image paths to relative...")
    
    # We will search for image paths to fix.
    old_path_segment = 'src="/img/'
    new_path_segment = 'src="img/'
    
    # Walk through all files and directories in the project.
    for subdir, dirs, files in os.walk(root_dir):
        for filename in files:
            # Only process HTML files.
            if filename.endswith('.html'):
                filepath = os.path.join(subdir, filename)
                print(f"Processing: {filepath}")

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Check if the old path segment exists and replace it.
                    if old_path_segment in content:
                        new_content = content.replace(old_path_segment, new_path_segment)
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        print(f"  - Converted image paths in {filename}")
                    else:
                        print(f"  - No changes needed in {filename}")
                
                except Exception as e:
                    print(f"  - ERROR processing file {filepath}: {e}")

if __name__ == "__main__":
    project_root = "." 
    convert_to_relative_paths(project_root)
    print("\nImage path fixing complete.")
