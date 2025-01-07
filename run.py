import os
from pathlib import Path

def consolidate_files(directory_path, output_file):
   try:
       directory = Path(directory_path).resolve()
       print(f"Scanning directory: {directory}")
       
       if not directory.exists():
           print(f"Error: Directory '{directory}' not found")
           return

       excluded_dirs = {'.next', 'node_modules'}
       
       with open(output_file, 'w', encoding='utf-8') as outfile:
           files_processed = 0
           for filepath in directory.rglob('*'):
               # Skip excluded directories
               if any(excluded in filepath.parts for excluded in excluded_dirs):
                   continue
                   
               if filepath.is_file():
                   try:
                       relative_path = filepath.relative_to(directory)
                       print(f"Processing: {relative_path}")
                       with open(filepath, 'r', encoding='utf-8') as infile:
                           outfile.write(f"// {relative_path}\n")
                           outfile.write(infile.read())
                           outfile.write("\n\n")
                           files_processed += 1
                   except UnicodeDecodeError:
                       print(f"Skipping binary file: {relative_path}")
                   except Exception as e:
                       print(f"Error processing {relative_path}: {str(e)}")
           
           print(f"Processed {files_processed} files")

   except Exception as e:
       print(f"Error: {str(e)}")

consolidate_files('.', 'consolidated_output.txt')