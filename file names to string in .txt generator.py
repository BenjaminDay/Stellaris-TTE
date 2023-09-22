import os

# Specify the folder path
folder_path = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\281990\2645604702\gfx\interface\icons\technologies"

# Get a list of all files in the folder
file_list = os.listdir(folder_path)

# Specify the output text file name
output_file = "file_names.txt"

# Open the text file in write mode and write the file names with line breaks
with open(output_file, "w") as f:
    for file_name in file_list:
        f.write(file_name + "\n")

print(f"File names written to {output_file}")
