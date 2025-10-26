#!/usr/bin/env python

"""
Fixes the greCy model installation by manually downloading,
renaming, and installing the .whl package from Hugging Face.

Version 4: Now caches downloads in ~/.cache/grecy_models
to avoid re-downloading. It also uses a .part file
to prevent installing corrupt/partial downloads.

Usage:
    python fix_grecy_install.py <model_name>

Example:
    python fix_grecy_install.py grc_proiel_trf
"""

import sys
import subprocess
import os
import re
import platform
import shutil

def run_command(cmd_list, capture=False):
    """
    Helper function to run a subprocess, print its output,
    and exit on failure.
    If 'capture' is True, it returns the stdout.
    """
    print(f"Running: {' '.join(cmd_list)}")
    try:
        result = subprocess.run(
            cmd_list,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if not capture:
            if result.stdout and result.stdout.strip():
                print(result.stdout)
            if result.stderr and result.stderr.strip():
                print(result.stderr, file=sys.stderr)
        return result.stdout
            
    except subprocess.CalledProcessError as e:
        print(f"\nError: Command failed with return code {e.returncode}", file=sys.stderr)
        print(f"Command: {' '.join(e.cmd)}", file=sys.stderr)
        if e.stdout:
            print(f"STDOUT: {e.stdout}", file=sys.stderr)
        if e.stderr:
            print(f"STDERR: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"\nError: Command not found: {e.filename}", file=sys.stderr)
        sys.exit(1)

def get_download_command(url, output_path):
    system = platform.system()
    if system in ("Linux", "Darwin"):
        return ["curl", "-f", "-sL", "-o", output_path, url]
    elif system == "Windows":
        return ["powershell", "-Command", f"Invoke-WebRequest -Uri '{url}' -OutFile '{output_path}'"]
    else:
        print(f"Unsupported operating system: {system}", file=sys.stderr)
        sys.exit(1)

def get_install_info(package_name, model_name):
    """
    Runs 'pip show' to find the model path and calculates its total size.
    """
    print(f"\n--- Model Installation Details ---")
    try:
        pip_show_cmd = [sys.executable, "-m", "pip", "show", package_name]
        output = run_command(pip_show_cmd, capture=True)
        
        location_match = re.search(r"^Location: (.+)$", output, re.MULTILINE)
        if not location_match:
            print(f"Could not find 'Location:' in 'pip show {package_name}' output.")
            return

        location = location_match.group(1).strip()
        model_path = os.path.join(location, model_name)
        
        if not os.path.isdir(model_path):
            print(f"Error: Could not find model directory at: {model_path}")
            return

        print(f"Model: {model_name}")
        print(f"Install Path: {model_path}")

        total_size = 0
        for dirpath, dirnames, filenames in os.walk(model_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        
        size_in_mb = total_size / (1024 * 1024)
        print(f"Total Size on Disk: {size_in_mb:.2f} MB")

    except Exception as e:
        print(f"Error while getting install info: {e}")

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <model_name>", file=sys.stderr)
        sys.exit(1)
    
    model_name = sys.argv[1]
    package_name = model_name.replace('_', '-')
    
    print(f"--- Starting manual install for model: {model_name} ---")

    # --- Define Cache Directory ---
    cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "grecy_models")
    os.makedirs(cache_dir, exist_ok=True)
    print(f"Using cache directory: {cache_dir}")

    # --- Determine filenames ---
    if model_name == "grc_proiel_trf":
        print("Detected 'grc_proiel_trf'. Using special case filename.")
        file_name_to_download = "grc_proiel_trf-3.7.5-py3-none-any.whl"
        file_to_install = "grc_proiel_trf-3.7.5-py3-none-any.whl"
        needs_rename = False
    else:
        file_name_to_download = f"{model_name}-any-py3-none-any.whl"
        file_to_install = f"{model_name}-0.0.0-py3-none-any.whl"
        needs_rename = True
    
    url = f"https://huggingface.co/Jacobo/{model_name}/resolve/main/{file_name_to_download}"
    
    # Final path for the installable wheel
    installable_path = os.path.join(cache_dir, file_to_install)
    
    # --- Check Cache ---
    if os.path.exists(installable_path):
        print(f"\nFound cached model. Skipping download.")
        print(f"Using file: {installable_path}")
    else:
        print(f"\nCached model not found. Starting download...")
        
        # Path for the file as named on Hugging Face
        download_path_hf = os.path.join(cache_dir, file_name_to_download)
        # Temporary path for downloading
        download_path_tmp = f"{download_path_hf}.part"

        try:
            # 4. Download
            print(f"Downloading {model_name} from {url}...")
            print(f"To: {download_path_tmp}")
            download_cmd = get_download_command(url, download_path_tmp)
            run_command(download_cmd)
            
            # Move from .part to final download name (atomic operation)
            shutil.move(download_path_tmp, download_path_hf)
            print("Download complete.")

            # 5. Rename (if needed)
            if needs_rename:
                print(f"\nRenaming to valid wheel name for pip...")
                shutil.move(download_path_hf, installable_path)
                print(f"Renamed: {download_path_hf} -> {installable_path}")
            
            # If no rename is needed, download_path_hf IS installable_path
            # (e.g., for grc_proiel_trf)
            
        except Exception as e:
            print(f"\nAn unexpected error occurred during download: {e}", file=sys.stderr)
            # Clean up partial file on error
            if os.path.exists(download_path_tmp):
                os.remove(download_path_tmp)
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nDownload interrupted. Cleaning up partial file.", file=sys.stderr)
            if os.path.exists(download_path_tmp):
                os.remove(download_path_tmp)
            sys.exit(1)

    # --- Install ---
    print(f"\nInstalling '{installable_path}' using pip...")
    pip_command = [sys.executable, "-m", "pip", "install", "--user", installable_path]
    run_command(pip_command)
    
    print(f"\n--- Successfully downloaded and installed {package_name} ---")
    
    get_install_info(package_name, model_name)

if __name__ == "__main__":
    main()