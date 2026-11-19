# File-Triage-Hash-Analysis
## Project Overview
A python tool that analyses files using SHA-256 hashes, identifies known files and detects duplicates

### Features
- Searches a selected folder for .txt and .bin files.

- Displays each file's name, size, extension and last-modified time.

- Calculates a SHA-256 hash for each file.

- Classifies files as KNOWN or UNKNOWN using hashes_reference.csv.

- Identifies duplicate files by comparing their hashes.

- Saves the results to triage_report.txt.

- Handles missing folders, empty folders and reference CSV errors.

### Requirements
- Python3
- No other python packages are needed

  ## How to Run
  1. Download project files into one folder
  2. Open the project folder in a code editor e.g. VS code
  3. Open in the terminal
  4. Run the following command
     - python3 file triage.py
  5. Press enter to analyse sample files, or enter your desired file path
  6. Results can be viewed in the terminal and open the triage_report.txt to see the saved report
 
### Project Files
-file_triage.py - main python program
-hashes_reference.csv  - reference SHA-256 hashes and lables
-sample_a.txt to sample_e.bin - five safe samples
-README.txt - dataset info
triage_report.txt - generated file-analysis report

### Results
sample_a.txt and sample_b.txt are identified as duplicate files because they both have identical SHA-256 hashes

The program classifies whether files are classified as either KNOWN or UNKNOWN depending on their hashes 

### Limitations
SHA-256 hash can identify identical files, but not whether a file is malicious

UNKNOWN result means that a hash wasn't found in the reference list. It doesn't really mean that the file is dangerous

The program doesn't execute or investigate real malware, its only intended for analysing safe files





