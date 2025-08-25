import os
import shutil

def flatten_html_files(root_dir):
    """
    Recursively finds all .html files in subdirectories and moves them
    to the root directory. It handles potential filename conflicts.
    """
    print(f"Starting to flatten directory from: {root_dir}")
    
    # Walk through the directory tree from the bottom up.
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # We only want to process subdirectories, not the root itself.
        if dirpath == root_dir:
            continue

        for filename in filenames:
            # Only move HTML files.
            if filename.endswith('.html'):
                source_path = os.path.join(dirpath, filename)
                destination_path = os.path.join(root_dir, filename)

                # Check for a filename conflict.
                if os.path.exists(destination_path):
                    name, ext = os.path.splitext(filename)
                    counter = 1
                    # Append a number until a unique filename is found.
                    while os.path.exists(os.path.join(root_dir, f"{name}_{counter}{ext}")):
                        counter += 1
                    new_filename = f"{name}_{counter}{ext}"
                    destination_path = os.path.join(root_dir, new_filename)
                    print(f"Conflict found for {filename}. Renaming to {new_filename}")
                
                # Move the file.
                shutil.move(source_path, destination_path)
                print(f"Moved {source_path} to {destination_path}")

        # After moving all files, check if the subdirectory is now empty and remove it.
        try:
            if not os.listdir(dirpath):
                os.rmdir(dirpath)
                print(f"Removed empty directory: {dirpath}")
        except OSError as e:
            # This handles cases where the directory isn't empty (e.g., has other file types).
            print(f"Could not remove directory {dirpath}: {e}")

if __name__ == "__main__":
    # The root directory of your project.
    project_root = "." 
    flatten_html_files(project_root)
    print("\nDirectory flattening complete.")
