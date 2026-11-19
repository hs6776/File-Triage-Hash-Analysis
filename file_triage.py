from pathlib import Path
from datetime import datetime 
import hashlib
import csv

BASE = Path(__file__).resolve().parent
folder = BASE 
choice = input("Enter folder path (or press Enter for sample): ").strip()

if choice:
    folder = Path(choice).resolve()

# Reads the reference CSV and stores the known SHA-256 hashes
def load_reference_hashes():
    reference_hashes = {}

    try:
        with open(BASE / "hashes_reference.csv", "r", newline = "", encoding = "utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                reference_hashes[row["sha256"]] = row["label"]

    except (OSError, KeyError) as error:
        raise SystemExit("Cannot load reference CSV: " + str(error))

    return reference_hashes


reference_hashes = load_reference_hashes()

# Collects file info and calculates its SHA-256 hash
def analyse_file(path):
    try:
        info = path.stat()
        print("\nName: ", path.name)
        print("Size (bytes):", info.st_size)
        print("Modified: ", datetime.fromtimestamp(info.st_mtime))
        print("Filename extension: ", path.suffix or "none")

        data = path.read_bytes()
        sha256 = hashlib.sha256(data).hexdigest()
        print("SHA-256: ", sha256)
# Groups files with the same Sha-256 hash to find duplicates
        if sha256 not in hash_groups:
            hash_groups[sha256] = []

        hash_groups[sha256].append(path.name) 

# Checks whether the file matches a know reference hash
        if sha256 in reference_hashes:
            status = "KNOWN"
            print("Status: KNOWN")
            print("Label:", reference_hashes[sha256])
        else:
            status = "UNKNOWN"
            print("Status: UNKNOWN")

        result = {
            "filename": path.name,
            "size": info.st_size,
            "extension": path.suffix,
            "modified": str(datetime.fromtimestamp(info.st_mtime)),
            "sha256": sha256,
            "status": status
        }

        results.append(result)
                
    except OSError as error:
        print("Cannot read", path.name, "-", error)

# Saves the file analysis and duplicate summary to a text report
def write_report(results, hash_groups):
    with open(BASE / "triage_report.txt", "w", encoding = "utf-8") as file:
        for result in results:
            file.write("Filename: " + result["filename"] + "\n")
            file.write("Size (bytes): " + str(result["size"]) + "\n")
            file.write("Extension: " + result["extension"] +  "\n")
            file.write("Modified: " + result["modified"] + "\n")
            file.write("SHA-256: " + result["sha256"] + "\n")
            file.write("Status: "+ result["status"] + "\n\n")
            
        file.write("\nDuplicate File Summary:\n")

        for file_hash, filenames in hash_groups.items():
            if len(filenames) > 1:
                file.write("SHA-256: " + file_hash + "\n")
                file.write("Duplicate files: " + str(filenames) + "\n")

# Checks whether the selected folder exists
if not folder.is_dir():
    print("Folder not found", folder)

        
else:
    matches = []

# Searches the folder for text and binary files
    for path in folder.rglob("*"):
        if path.is_file() and path.suffix.lower() in (".txt", ".bin") and path.name not in ("README.txt", "triage_report.txt"):
            matches.append(path)

    if not matches:
        print("No matching files found")

    hash_groups = {}
    results = []

    for path in matches:
            analyse_file(path)

        
    print("\nDuplicate File Summary:")

# Identifies files that have the same SHA-256
    for file_hash, filenames in hash_groups.items():
        if len(filenames) > 1:
            print("SHA-256:", file_hash)
            print("Duplicate files:", filenames)

    write_report(results, hash_groups)

        




            