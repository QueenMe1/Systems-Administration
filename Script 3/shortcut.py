#! /usr/bin/python3
# Susan Olayemi
# Thursay, October 23rd, 2025

import os
from pathlib import Path
import subprocess

def get_home():
    # returns the user's current home directory.
    return Path.home()

def create_symlink():
    print("="*20 + " Create a Symbolic Link " + "="*20)
    target_path = input("Enter the full path of the file you want to create a symbolic link for:\n>").strip()
    target = Path(target_path)

    if not target.exists():
        print("Error: File not found. Check the filename and try again.")
        return

    home = get_home()
    desktop = home / "Desktop"
    desktop.mkdir(exist_ok=True)

    link_name = input("Enter a name for the symbolic link (leave a blank if you want the same name as the file:\n>)").strip()
    if not link_name:
        link_name = target.name
    link_path = desktop / link_name

    try:
        os.symlink(target, link_path)
        print(f"Success!! The symbolic link is created on Desktop -> {link_path} -> {target}\n")
    except FileExistsError:
        print("Error: A file or link with this name already exist on your desktop")
    except PermissionError:
        print("Error: Permission Error. Try running this script with the appropriate priviledge")
    except Exception as e:
        print(f"Unexpected Error: {e}")

def delete_symlink():
    print("\n=== Delete a Symbolic Link ===")
    home = get_home()
    desktop = home / "Desktop"

    link_name = input("Enter the name of symbolic link you want to delete (It must be on your desktop:\n>)").strip()
    link_path = desktop / link_name

    if not link_path.exists():
        print("Error: No such file or link on your desktop")
    if not link_path.is_symlink():
        print("Error This specified file is not a symbolic link")
    
    try:
        link_path.unlink()
        print("Link has been Successfully deleted")
    except Exception as e:
        print(f"Unexpected Error: {e}")

def generate_report():
    print("="*50)
    print("Report".center(50))
    print("="*50)

    home = get_home()
    desktop = home / "Desktop"

    if not desktop.exists():
        print("Desktop not found on this device\n")
        return

    links = [f for f in desktop.iterdir() if f.is_symlink()]
    if not links:
        print("There is no symbolic link in desktop\n")
    else:
        print("Symbolic link in desktop are:")
        for link in links:
            try:
                target = os.readlink(link)
                print(f"Link name: {link.name} -> Target: {target}")
            except Exception as e:
                print(f"Link name: {link.name} -> Error reading the target: {e}")
        
        print()
        sum_links = sum(1 for p in home.rglob('*') if p.is_symlink())

        print(f"Total Symbolic link in {home}: {sum_links}")
        print("-" *60)


def main():
    subprocess.run("clear")
    while True:
        print("="*50)
        print("MAKE A SUYMBOLIC LINK".center(50))
        print("="*50)

        print()

        print("[1] Create a Symbolic Link\n"
        "[2] Delete a Symbolic Link\n"
        "[3] Generate a Symbolic Link Report\n"
        "[4] Quit")

        u_input = input("Enter a choice (1 - 4). To Quit either enter 4 or quit.\n>")

        if u_input in ["4","quit"]:
            print("Byeeeeeeeeeeeeeeeeee!!!!!!!!")
            break
        elif u_input == "1":
            create_symlink()
        elif u_input == "2":
            delete_symlink()
        elif u_input == "3":
            generate_report()
        else:
            print("Please enter the appropriate numbers between 1 - 4") 



if __name__ == "__main__":
    main()

