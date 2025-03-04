import os
import shutil
import sys

def uninstall():
    install_dir = os.path.dirname(os.path.abspath(sys.executable)) # dynamic folder path find
    print(f"Uninstalling from {install_dir}")

    try:
        os.chdir("..") # ek level var jaycha curr directory nahi karnya sathi
        shutil.rmtree(install_dir) # folder gone
        print("Uninstall completed!")

    except Exception as e:
        print(f"Error : {e}")

if __name__ == "__main__":
    uninstall()