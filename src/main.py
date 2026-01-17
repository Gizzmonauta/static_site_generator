from copystatic import copy_files_recursive 

def main():
    source = "./static"
    destination = "./public"
    copy_files_recursive(source, destination)

if __name__ == "__main__":
    main()
