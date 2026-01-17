from copystatic import copy_files_recursive 
from markdown_to_html import generate_pages_recursive

def main():
    source = "./static"
    destination = "./public"
    copy_files_recursive(source, destination)

    from_path = "./content"
    template_path = "./template.html"
    dest_path = "./public"
    generate_pages_recursive(from_path, template_path, dest_path)

if __name__ == "__main__":
    main()
