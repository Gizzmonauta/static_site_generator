import os
import shutil

def copy_files_recursive(source_dir_path: str, dest_dir_path: str, is_top_level: bool = True) -> None:
    """
    Recursively copies all files and directories from source_dir_path to dest_dir_path.

    Args:
        source_dir_path (str): The path to the source directory.
        dest_dir_path (str): The path to the destination directory.
    """
    if not os.path.exists(source_dir_path):
        raise FileNotFoundError(f"Source directory '{source_dir_path}' does not exist.")

    source_abs: str = os.path.abspath(source_dir_path)
    dest_abs: str = os.path.abspath(dest_dir_path)
    if dest_abs == source_abs or dest_abs.startswith(source_abs + os.sep):
        raise ValueError("Destination directory cannot be the same as or a subdirectory of the source directory.")
    
    if is_top_level and os.path.exists(dest_dir_path):
        shutil.rmtree(dest_dir_path)
        os.makedirs(dest_dir_path)
        print(f"Destination directory '{dest_dir_path}' already exists. It has been cleared.")

    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
        print(f"Created destination directory: {dest_dir_path}")

    for item in os.listdir(source_dir_path):
        source_item_path = os.path.join(source_dir_path, item)
        dest_item_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(source_item_path):
            shutil.copy(source_item_path, dest_item_path)
            print(f"Copied file: {source_item_path} -> {dest_item_path}")
        elif os.path.isdir(source_item_path):
            copy_files_recursive(source_item_path, dest_item_path, is_top_level=False)
            print(f"Copied directory: {source_item_path} -> {dest_item_path}")
        else:
            print(f"Skipped unknown item type: {source_item_path}")

def main():
    source = "./static"
    destination = "./public"
    copy_files_recursive(source, destination)

if __name__ == "__main__":
    main()
    