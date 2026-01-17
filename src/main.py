from copystatic import copy_files_recursive 
from markdown_to_html import generate_page

def main():
    source = "./static"
    destination = "./public"
    copy_files_recursive(source, destination)
    generate_page("./content/index.md", "./template.html", "./public/index.html")

if __name__ == "__main__":
    main()
