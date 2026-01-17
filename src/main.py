import os
import sys
import shutil
from copystatic import copy_files_recursive 
from markdown_to_html import generate_pages_recursive

def main():
    static_dir = "./static"
    public_dir = "./docs"
    content_dir = "./content"
    template_path = "./template.html"

    print(f"Copying files from {static_dir} to {public_dir}...")
    copy_files_recursive(static_dir, public_dir)

    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    generate_pages_recursive(os.path.join(content_dir, ""), template_path, os.path.join(public_dir, ""), basepath)

if __name__ == "__main__":
    main()
