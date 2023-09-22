import os

def scraper(dir_path, pretext=[], info=True, filters=[], kill_filter=[], file_filter=[], output_name="output.txt", filter_mode="Single"):

    #Filter handling
    if filters == []:
        pretext.append("\nNo Filters\n\n")
    else:
        search_keys = "\nSearch Keys: Filter 1 = " + str(filters[0])
        for x in range(1, len(filters)):
            search_keys += " | Filter " + str(x+1) + " = " + str(filters[x])
        pretext.append(search_keys + "\n\n")

    print("\nStarting Search...\n")

    file_list = os.listdir(dir_path)
    files_to_search = []

    if file_filter == []:
        files_to_search = file_list
    else:
        for file_name in file_list:
            for entry in file_filter:
                if entry in file_name:
                    files_to_search.append(file_name)
                    break # exit the loop so that it doesnt add this file again if another filter matches


    output = []
    
    files_searched = 0
    line_total_count = 0
    
    #Searching the files in chosen directory
    for file_name in files_to_search:
        if logging:
            print("Searching: ", file_name)
        line_count = 0
        match = False
        matching_lines = []
        if filters ==[]:
            with open(dir_path+'\\'+file_name, 'r+', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    matching_lines.append(line)
                    line_count += 1
                    match = True
                files_searched += 1

        #Filtering by checking if all entries match
        if filter_mode == "All":               
            with open(dir_path+'\\'+file_name, 'r+', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    for entry in filters:
                        if entry not in line:
                            break # if one filter is not present do not write
                    else:
                        line_count += 1
                        matching_lines.append(line)
                        match = True
                files_searched += 1

        #Filtering by checking if all entries match for a list of entries
        elif filter_mode == "Multi":
            with open(dir_path+'\\'+file_name, 'r+', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    for entry_list in filters:
                        for entry in entry_list:
                            if entry not in line:
                                break # if one filter is not present do not write
                        else:
                            line_count += 1
                            matching_lines.append(line)
                            match = True
                            break # break to stop duplicate lines since a filter matched
                files_searched += 1

        #Filtering by checking if any entries match        
        else:
            with open(dir_path+'\\'+file_name, 'r+', encoding='utf-8', errors='ignore') as file:
                if filters ==[]:
                    for line in file:
                        matching_lines.append(line)
                        line_count += 1
                        match = True
                else:
                    for line in file:
                        for entry in filters:
                            if entry in line:
                                matching_lines.append(line)
                                line_count += 1
                                match = True
                                break # exit the inner loop on the first match
                files_searched += 1

        if match:
            if info: output.append("\nFile: "+file_name+"\n")
            for line in matching_lines:
                for entry in kill_filter:
                    if entry in line:
                        line_count -= 1
                        break
                else:
                    output.append(line)

        if logging:
            print(" ", line_count, " Matches Found")
        line_total_count += line_count

    print("\nSearch Complete! Total Files Searched: ", files_searched,
          " | Total Matches Found: ", line_total_count,
          "\nSaving Results...")

    pretext.append("Results ("+str(line_total_count)+"):\n")
    

    #writing txt
    if logging:
        with open(output_name, 'w', encoding='utf-8', errors='ignore') as file:
            if info:
                for line in pretext:
                    file.write(line)
            for line in output:
                file.write(line)
                
        print("Results saved in ",output_name)
        
    return output

def dict_creator(raw_data, dumb_techs):
    tree = []
    tech_dict = {}
    for line in raw_data:
        if '#' in line[:2]:
            line = line.split('#')[1]
        if '\t' in line[:2]:
            line = line.split('\t')[1]

        if 'tech_' == line[:5]:
            tree.append(tech_dict) # Append previous tech
            tech_dict = {'name': line.split(' = {')[0], 'tier': '', 'prerequisites': [], 'unlocks' : []}

        elif 'tier' == line[:4]:
            tech_dict['tier'] = line.split()[2]

        elif 'prerequisites' == line[:13]:
            tech_dict['prerequisites'] = []
            if '"' in line:
                split_string = line.split('"')
            else:
                split_string = line.split()
            for string in split_string:
                if 'tech_' == string[:5]:
                    tech_dict['prerequisites'] += [string]
        else:
            tree.append(tech_dict) # Append previous tech
            print("This tech is dumb: ", line.split(' = {')[0])
            for dumb_tech in dumb_techs:
                if dumb_tech in line:
                    tech_dict = {'name': line.split(' = {')[0], 'tier': '', 'prerequisites': [], 'unlocks' : []}

    return tree[1:]

def unlock_mapping(tree):
    unlocked_tree = tree
    for branch in tree:
        prerequisites = branch['prerequisites']
        for leaf in prerequisites:
            for i in range(len(unlocked_tree)):
                if unlocked_tree[i]['name'] == leaf:
                    unlocked_tree[i]['unlocks'] += [branch['name']]

    return unlocked_tree

def composite(file, layer1, layer2, path):    
    file.write(f'magick composite -gravity center -size 64x64 -quality 100 -define dds:compression=none "{layer2}" "{layer1}" "{path}"\n')
    #run cmd line to composite layer2 onto layer1 and save result as os.path.join(sub_path.replace("Source", "Output"), img)


def make_batch_file(structure, source_icons, mega_list, ecu_list, temp_icons=r'.\icons'):
    #Create the file
    batch_file = open("run_composition.bat", "w")
    destination_folder = r'.\TTE Mod\gfx\interface\icons\technologies'
    batch_file.write(f"@echo off\nmkdir \"{destination_folder}\"\n")
    cwd = os.getcwd()
    try: 
        os.chdir(temp_icons)
    except:
        batch_file.write(f'xcopy "{source_icons}" "{temp_icons}" /I\n') # copies icons into a temporary folder to be moved

    #Copy overwrite default tech icons with tier numbers tech icons
    overwrite_icons = r'.\Templates\overwrite_icons'
    os.chdir(cwd)
    try:
        os.chdir(overwrite_icons)
        batch_file.write(f'xcopy "{overwrite_icons}" "{temp_icons}" /I /Y\n') # copies tier number tech icons and overwrites base icons
    except:
        print("\n\n#####\n\nCheck Tier Number Tech icons folder\n\n#####\n\n")
        
    #Iterate through the structure and add command lines to make composites through each tier
    tier_list = ["Tier 0", "Tier 1", "Tier 2", "Tier 3", "Tier 4", "Tier 5", "Repeatable", "Event"]
    tc = 0
    for tier in structure:
        uc = 0
        for unlocks in tier:
            if str(tier_list[tc]) == "Repeatable":
                composite(batch_file, f'.\\Templates\\{str(tier_list[tc])}.dds', f'.\\Templates\\{str(tier_list[tc])}.dds', '.\\Templates\\current_template.dds')
            else:
                composite(batch_file, f'.\\Templates\\{str(tier_list[tc])}.dds', f'.\\Templates\\Unlocks {str(uc)}.dds', '.\\Templates\\current_template.dds')
            for tech in structure[tc][uc]:
                composite(batch_file, ".\\Templates\\current_template.dds", f'{temp_icons}\\{tech}', f'{destination_folder}\\{tech}') 
            uc += 1
        tc += 1

    for tech in mega_list:
        composite(batch_file, f'{destination_folder}\\{tech}.dds', ".\\Templates\\mega_engineering.dds", f'{destination_folder}\\{tech}.dds')
    for tech in ecu_list:
        composite(batch_file, f'{destination_folder}\\{tech}.dds', ".\\Templates\\ecumonopolis.dds", f'{destination_folder}\\{tech}.dds')

    #Cleanup
    batch_file.write('rd /s /q "icons"\n')
    batch_file.write('del /q "%~f0"\n')

    batch_file.close()

def make_structure(data):

    structure = [
    # 0  1  2  3+
    [[],[],[],[]], # Tier 0
    [[],[],[],[]], # Tier 1
    [[],[],[],[]], # Tier 2
    [[],[],[],[]], # Tier 3
    [[],[],[],[]], # Tier 4
    [[],[],[],[]], # Tier 5
    [[],[],[],[]], # Repeatable
    [[],[],[],[]]] # Event


    for tech_dict in data:
        image_name = tech_dict['name']+'.dds'

        unlocks = len(tech_dict['unlocks'])
        if unlocks > 3: unlocks = 3  

        if tech_dict['tier'] in "012345":
            structure[int(tech_dict['tier'])][unlocks].append(image_name)
        elif tech_dict['tier'] == "@repeatableTechTier":
            structure[6][unlocks].append(image_name)
        else:
            structure[7][unlocks].append(image_name)

    return structure

def get_prerequisites(tree, tech_name):
    return list(set(get_raw_prerequisites(tree, tech_name)))
    

def get_raw_prerequisites(tree, tech_name, requirements_list=None):
    if requirements_list is None:
        requirements_list = []
    for i in range(len(tree)):
        if tree[i]['name'] == tech_name:
            leaf = tree[i]['prerequisites']
            for prereq_name in leaf:
                requirements_list.append(prereq_name)

            if leaf != []:
                for prereq_name in leaf:
                    requirements_list = get_raw_prerequisites(tree, prereq_name, requirements_list)

            return requirements_list


def main(tech_info_path, tech_icon_path):
    dumb_techs = ["null_void_beam"]
    data = scraper(tech_info_path, info=False, filters=[["tech_","= {"],["tier ="],["prerequisites ="], dumb_techs], kill_filter=["member", "{}","{ }"], file_filter=["00"], output_name="object_list.txt", filter_mode="Multi")

    tree = dict_creator(data, dumb_techs)

    unlocked_tree = unlock_mapping(tree)

    if logging:
        with open('dicts.txt', 'w', encoding='utf-8', errors='ignore') as file:
            file.write('Tech names, their tiers, the required techs to unlock them and what they unlock:')
            for tech in unlocked_tree:
                file.write('\n\nName: '+str(tech['name']))
                file.write('\nTier: '+str(tech['tier']))
                file.write('\nRequired: '+str(tech['prerequisites']))
                file.write('\nUnlocks: '+str(tech['unlocks']))

    structure = make_structure(unlocked_tree)


    mega_list = get_prerequisites(tree, "tech_mega_engineering")
    ecu_list = get_prerequisites(tree, "tech_housing_2") + ["tech_housing_2"]
    if logging:
        print("Mega list", mega_list)
        print("Ecu list", ecu_list)

    make_batch_file(structure, tech_icon_path, mega_list, ecu_list)


if __name__ == '__main__':
    global logging
    logging = False
    stellaris_game_path = r"C:\Program Files (x86)\Steam\steamapps\common\Stellaris"

    tech_info_path = stellaris_game_path + r"\common"
    if str("technology") not in str(os.listdir(tech_info_path)):
        print("\n\n#####\n\nVerify Stellaris tech_info folder path\n\n#####\n\n")
        
    tech_icons_path = stellaris_game_path + r"\gfx\interface\icons"
    if str("technologies") not in str(os.listdir(tech_icons_path)):
        print("\n\n#####\n\nVerify Stellaris tech_icons folder path\n\n#####\n\n")

    main(tech_info_path+r"\technology", tech_icons_path+r"\technologies")
    input("ENTER to exit")
