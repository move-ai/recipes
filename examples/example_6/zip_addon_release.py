import os
import zipfile
from pathlib import Path


def zip_dir(directory: Path, zip_path: str, exclude_folders, exclude_files, addon_name):
    """
    Compress a directory (ZIP file).
    """
    if os.path.exists(directory):
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as out_zip_file:
            # The root directory within the ZIP file.
            rootdir = addon_name

            for dirpath, dirnames, filenames in os.walk(directory):
                dirnames[:] = [d for d in dirnames if d not in exclude_folders]
                for filename in filenames:
                    if filename in exclude_files:
                        continue
                    # Write the file named filename to the archive,
                    # giving it the archive name 'arcname'.
                    filepath = os.path.join(dirpath, filename)
                    parentpath = os.path.relpath(filepath, directory)
                    arcname = os.path.join(rootdir, parentpath)

                    out_zip_file.write(filepath, arcname)


def get_ints_from_str(string: str):
    """
    Get all the integers from a string.
    """
    return [int(s) for s in string if s.isdigit()]


def get_version(line_num: int = 19):
    """
    Get the version number from the __init__.py file.

    Parameters
    ----------
    line_num : int
        The number of the line in the __init__.py file that contains the version number.
        Default is 19. If you change the line of version number in the __init__.bl_info,
        you must change this number to match.
    """

    current_dir = Path(__file__).resolve().parent
    init_file_path = current_dir / "__init__.py"

    with open(init_file_path, "r") as f:
        lines = f.readlines()
        version_line = lines[line_num - 1]
        version = get_ints_from_str(version_line)
        print(version)

        version = "_".join(str(num) for num in version)

    return version


def get_addon_name(line_num=15):
    """
    Get the name of the addon from the __init__.py file.
    """
    current_dir = Path(__file__).resolve().parent
    init_file_path = current_dir / "__init__.py"

    with open(init_file_path, "r") as f:
        lines = f.readlines()
        name_line = lines[line_num - 1]
        name = name_line.split('"')[3].lower().replace(" ", "_")
        print(name)

    return name


if __name__ == "__main__":
    version = get_version()
    print(version)

    exclude_folders = [
        "non-public",
        "releases",
        "__pycache__",
        ".git",
        ".vscode",
        ".gitignore",
        "zip_addon_release.py",
        "unused",
    ]

    exclude_files = [".gitignore", "zip_addon_release.py"]

    addon_name = get_addon_name()

    current_dir = Path(__file__).resolve().parent
    releases_dir = current_dir / "releases"
    releases_dir.mkdir(exist_ok=True)
    zip_name = f"{addon_name}_{version}.zip"
    zip_path = releases_dir / zip_name

    zip_dir(
        directory=current_dir,
        zip_path=zip_path,
        exclude_folders=exclude_folders,
        exclude_files=exclude_files,
        addon_name=addon_name,
    )
