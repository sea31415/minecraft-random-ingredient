import sys
import os
import re
import random
import shutil


def read_ings_from_file(ingredients_dir):
    with open(ingredients_dir, mode='r', encoding='utf-8') as file:
        ingredients_list = file.readlines()
    ingredients_list = [[x.split(':')[0], x.split(':')[1][:-1] if x.split(':')[1][-1]=='\n' else x.split(':')[1]] for x in ingredients_list]
    return ingredients_list


def read_filter_from_file(filter_dir):
    with open(filter_dir, mode='r', encoding='utf-8') as file:
        filter_lst = file.readlines()
    filter_lst = [x[:-1] if x[-1]=='\n' else x for x in filter_lst]
    return filter_lst


def read_tags_from_file(tag_dir):
    with open(tag_dir, mode='r', encoding='utf-8') as file:
        tags_lst = file.readlines()
    tags_lst = [x[:-1] if x[-1] == '\n' else x for x in tags_lst]
    tags_lst = [x.replace(' ', '') for x in tags_lst]
    tags_lst = [x.replace('\t', '') for x in tags_lst]

    for tag_i in range(len(tags_lst)):
        tag = tags_lst[tag_i]
        tag = tag.split(':')
        tag[1] = tag[1].split(',')
        tags_lst[tag_i] = tag

    return tags_lst


def read_recipe(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        cont = file.read()
    cont = cont.replace('\n', '')

    # keep spaces in the pattern, because they're needed for crafting_shaped
    has_pattern = re.search(r'"pattern":\s*\[\s*(".{1,3}",\s*){0,2}(".{1,3}")\s*]', cont)
    if has_pattern:
        old_patterns = re.findall(r'"pattern":\s*\[\s*(".{1,3}",\s*)?(".{1,3}",\s*)?(".{1,3}")\s*]', cont)[0]
        old_patterns = [x.strip() for x in old_patterns if x != '']
        cont = cont.replace(' ', '')
        wrong_patterns = re.findall(r'"pattern":\[(".{1,3}",\s*)?(".{1,3}",\s*)?(".{1,3}")]', cont)[0]
        wrong_patterns = [x for x in wrong_patterns if x != '']


        start = 0
        for pattern in range(len(old_patterns)):
            old_pattern = old_patterns[pattern]
            wrong_pattern = wrong_patterns[pattern]
            start = cont.index(wrong_pattern, start + 1)
            cont = cont[:start] + cont[start:].replace(wrong_pattern, old_pattern, 1)
    else:
        cont = cont.replace(' ', '')

    return cont


def get_items_from_list(tag, tags_lst):
    tags_lst_tags = [x[0] for x in tags_lst]
    lst = tags_lst[tags_lst_tags.index(tag)][1]

    ing_i = 0
    while ing_i < len(lst):
        if lst[ing_i][0] == "#":
            add_ings = get_items_from_list(lst.pop(ing_i)[1:], tags_lst)
            for ing in range(len(add_ings)):
                lst.insert(ing_i+ing, add_ings[ing])
            ing_i += len(add_ings)
        else:
            ing_i += 1

    return lst


def remake_tmp(tmp_dir, mk_dir=True):
    try:
        shutil.rmtree(tmp_dir)
    except FileNotFoundError:
        pass

    if mk_dir:
        os.mkdir(tmp_dir)


def prepare_tmp(tmp_dir):
    remake_tmp(tmp_dir)

    # recipes
    os.mkdir(os.path.join(tmp_dir, "data"))
    os.mkdir(os.path.join(tmp_dir, "data/minecraft"))
    os.mkdir(os.path.join(tmp_dir, "data/minecraft/recipes"))

    # functions general
    os.mkdir(os.path.join(tmp_dir, "data/minecraft/tags"))
    os.mkdir(os.path.join(tmp_dir, "data/minecraft/tags/functions"))
    with open(os.path.join(tmp_dir, "data/minecraft/tags/functions/tick.json"), mode='w', encoding='utf-8') as tick:
        tick.write('{"values":["rando_ings:tick"]}')

    # custom functions
    os.mkdir(os.path.join(tmp_dir, "data/rando_ings"))
    os.mkdir(os.path.join(tmp_dir, "data/rando_ings/functions"))


def add_datapack_stuff(seed, tmp_dir, script_dir, original_list, new_list):
    with open(os.path.join(tmp_dir, "pack.mcmeta"), mode='w', encoding='utf-8') as meta:
        meta.write('{"pack":{"pack_format":15,"description":"Crafting Ingredient Randomizer\\nSeed: ' + str(seed) + '"}}')

    with open(os.path.join(tmp_dir, "cheatsheet.txt"), mode='w', encoding='utf-8') as cheatsheet:
        for ing in range(len(new_list)):
            ing_string = new_list[ing][1] + " is used for " + original_list[ing][1] + "\n"
            cheatsheet.write(ing_string)

    # todo: make pack.png (in files folder)
    # shutil.copyfile(os.path.join(script_dir, "files/pack.png"), os.path.join(tmp_dir, "pack.png"))


def make_zip(seed, tmp_dir):
    try:
        os.remove("random_ingredients_" + str(seed) + ".zip")
    except FileNotFoundError:
        pass
    shutil.make_archive("random_ingredients_" + str(seed), 'zip', "tmp")
    remake_tmp(tmp_dir, False)


def finalize(seed, tmp_dir, script_dir, original_list, new_list):
    add_datapack_stuff(seed, tmp_dir, script_dir, original_list, new_list)

    make_zip(seed, tmp_dir)


def all_random_shuffle(x, seed):
    if len(x) == 1:
        raise Exception
    for i in reversed(range(1, len(x))):
        # pick an element in x[:i] with which to exchange x[i]
        random.seed(seed)
        j = int(random.random() * i)
        x[i], x[j] = x[j], x[i]


def shuffle_ingredients(ingredients_list, seed=False, all_random=True):
    if not seed:
        seed = random.randint(-2**63, 2**63-1)

    if all_random:
        all_random_shuffle(ingredients_list, seed)
    else:
        random.Random(seed).shuffle(ingredients_list)
    return ingredients_list, seed


def list_replace(og_list, new_list, txt):
    items = re.findall(r'\{"(item|tag)":"minecraft:(.*?)"}', txt)
    items = [[x[0], x[1]] for x in items]

    index = 0
    for item in items:
        old_string = f'"{item[0]}":"minecraft:{item[1]}"'
        index = txt.index(old_string, index+1)

        new_item = new_list[og_list.index(item)]
        new_string = f'"{new_item[0]}":"minecraft:{new_item[1]}"'

        txt = txt[:index-1] + txt[index-1:].replace(old_string, new_string, 1)

    # for ing in range(len(og_list)):
    #     og = f'"{og_list[ing][0]}":"minecraft:{og_list[ing][1]}"'
    #     new = f'"{new_list[ing][0]}":"minecraft:{new_list[ing][1]}"'
    #     txt = txt.replace(og, new)

    return txt


def change_text(og_list, new_list, text):  # change to use normal type detection
    typ = re.search(r'"type":"minecraft:(.*?)"', text).group(1)

    match = ""
    t = ""

    if typ == "crafting_shaped":
        match = re.search(r'"key":(\{(".":\{"(item|tag)":"minecraft:(.*?)"},|".":\[(\{"(item|tag)":"minecraft:(.*?)"},)*\{"(item|tag)":"minecraft:(.*?)"}],)*(".":\{"(item|tag)":"minecraft:(.*?)"}|".":\[(\{"(item|tag)":"minecraft:(.*?)"},)*\{"(item|tag)":"minecraft:(.*?)"}]))}', text).group(1)

    elif typ == "crafting_shapeless":
        match = re.search(r'"ingredients":\[((\{"(item|tag)":"minecraft:(.*?)"},)*\{"(item|tag)":"minecraft:(.*?)"})]', text).group(1)

    else:  # type_1
        match = re.search(r'"ingredient":(\[(\{"(item|tag)":"minecraft:(.*?)"},)*\{"(item|tag)":"minecraft:(.*?)"}]|\{"(item|tag)":"minecraft:(.*?)"})', text).group(1)

    t = list_replace(og_list, new_list, match)
    text = text.replace(match, t)
    return text, t


def add_command_to_function(file, item, recipe_name, comms_list):
    comm = 'execute as @a if entity @s[nbt={Inventory:[{id:"minecraft:' + item + '"}]}] run recipe give @s minecraft:' + recipe_name + '\n'
    if comm not in comms_list:
        file.write(comm)
        comms_list.append(comm)
    return comms_list


def add_commands_to_function(file, items, recipe_name, comms_list, tags_lst):
    item_i = 0
    while item_i < len(items):
        if items[item_i][0] == "tag":
            # items[item_i] = get_items_from_list(items[item_i][1], tags_lst)

            add_ings = get_items_from_list(items.pop(item_i)[1], tags_lst)
            for ing in range(len(add_ings)):
                items.insert(item_i+ing, add_ings[ing])
            item_i += len(add_ings)
        else:
            items[item_i] = items[item_i][1]
            item_i += 1

    for item in items:
        comms_list = add_command_to_function(file, item, recipe_name, comms_list)

    return comms_list


if __name__ == "__main__":
    script_directory = os.path.dirname(__file__)
    tmp_directory = os.path.join(script_directory, "tmp")
    filter_directory = os.path.join(script_directory, "files/filter.txt")
    tag_directory = os.path.join(script_directory, "files/tags.txt")
    ingredients_directory = os.path.join(script_directory, "files/ingredients.txt")
    recipes_directory = os.path.join(script_directory, "files/recipes")

    prepare_tmp(tmp_directory)

    if len(sys.argv) == 3:
        all_notifs = sys.argv[2].lower in ["true", "t", "yes", "y"]

        if sys.argv[1] == "auto_seed":
            user_seed = False
        elif sys.argv[1].isnumeric():
            user_seed = int(sys.argv[1])
        else:
            user_seed = input("Seed (leave empty for random seed): ")
            if user_seed == "":
                user_seed = False

    else:
        user_seed = input("Seed (leave empty for random seed): ")
        if user_seed == "":
            user_seed = False

    ings_list = read_ings_from_file(ingredients_directory)
    # sh_ings_list, user_seed = shuffle_ingredients(ings_list[:])
    sh_ings_list, user_seed = shuffle_ingredients(ings_list[:], user_seed)

    # print(sh_ings_list[ings_list.index(['item', 'oak_log'])])


    filter_list = read_filter_from_file(filter_directory)
    tags_list = read_tags_from_file(tag_directory)
    recipes = os.listdir(recipes_directory)

    commands_list = []
    tick_func_file = open(os.path.join(tmp_directory, "data/rando_ings/functions/tick.mcfunction"), mode='w', encoding='utf-8')

    for file_name in recipes:
        if file_name not in filter_list:
            content = read_recipe(os.path.join(recipes_directory, file_name))
            sh_content, new_ing_text = change_text(ings_list, sh_ings_list, content)

            # todo: add "show_notification" to all recipes that don't already include it if all_notifs is True

            recipes_path = os.path.join(tmp_directory, "data/minecraft/recipes")
            with open(os.path.join(recipes_path, file_name), mode='w', encoding='utf-8') as sh_file:
                sh_file.write(sh_content)

            new_ings = re.findall(r'\{"(item|tag)":"minecraft:(.*?)"}', new_ing_text)
            commands_list = add_commands_to_function(tick_func_file, new_ings, file_name[:-5], commands_list, tags_list)

    tick_func_file.close()

    finalize(user_seed, tmp_directory, script_directory, ings_list, sh_ings_list)

    # todo: find way to not have the recipe book auto-populate