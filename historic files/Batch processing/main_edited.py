import os

def get_directory(fp):
    directory = os.listdir(fp)
    if "desktop.ini" in directory:
        directory.remove("desktop.ini")
    directory.sort()
    return directory

def get_folders(directory):
    folders = []
    for item in directory:
        if "." not in item:
            folders.append(item)
    return folders

def composite(layer1, layer2, path):    
    batch_file.write(f'magick composite -gravity center -size 64x64 -quality 100 -define dds:compression=none "{layer2}" "{layer1}" "{path}"\n')
    #run cmd line to composite layer2 onto layer1 and save result as os.path.join(sub_path.replace("Source", "Output"), img)

def process_images():
    for img in images:
        img_path = os.path.join(sub_path, img)
        img_output = os.path.join("Output", img)
        #Apply the Tier + Unlocks template to the image and save to Output folder
        composite(current_temp_path, img_path, img_output)
        
        #If show_mega_req is True then add the M to all required technologies based on .txt list
        if show_mega_req:
            if img in mega_filter:
                composite(img_output, 'Source\\m.dds', img_output)

###

show_mega_req = True #Toggle for adding letter M to techs that are required for Mega Engineering

if show_mega_req:
    with open('Source\\mega requirements.txt') as mega_list:
        mega_filter = mega_list.read().split("\n")

print(mega_filter)
    
batch_file = open("run_composition.bat", "w")
batch_file.write("@echo off\nmkdir Output\n")

top_folder = "Source"
current_temp_path = os.path.join(top_folder, "current_template.dds")

###

file_path = os.path.realpath(__file__).replace(r"main_edited.py", top_folder)
print(f"\nFile path:\n{file_path}")

main_dir = get_directory(file_path)
#print(f"\nMain Directory:\n{main_dir}")

main_folders = get_folders(main_dir)
print(f"\nMain Folders:\n{main_folders}")

for folder in main_folders:
    current_path = os.path.join(top_folder, folder)
    tier_template = os.path.join(current_path, "template.dds")
    tier_folders = get_folders(get_directory(current_path))
    print(f"\n{folder}:\n{tier_folders}")
    
    for sub_folder in tier_folders:
        sub_path = os.path.join(current_path, sub_folder)
        images = get_directory(sub_path)
        print(f"{sub_folder}: {str(len(images))}")
        #Create temporary template for Tier + Unlocks together
        composite(os.path.join(top_folder, folder+".dds"), os.path.join(top_folder, sub_folder+".dds"), current_temp_path)

        process_images()
        

batch_file.close()
