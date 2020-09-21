# coding=utf-8
import json
from time import sleep

DEBUG = False

print("Loading file... ", end="")
try:
    mod_list_file = open("parsed_mod_list.json", "r")
    mod_list = json.load(mod_list_file)
    mod_list_file.close()
    if DEBUG:
        sleep(5)
except json.JSONDecodeError:
    print("Failed to load file! Invalid JSON.")
    exit(1)
except OSError:
    print("Failed to load file! OSError.")
    exit(1)
else:
    del mod_list_file
    print("Done!")

while True:
    search_term = input("Enter your search term, quit to quit > ")
    search_term = search_term.lower()
    if search_term == "quit":
        break
    results = []
    for mod in mod_list:
        if search_term in mod["name"].lower():
            results.append(mod)
    if len(results) == 0:
        print("Didn't find any mods.")
        continue
    print("\n")
    for mod in results:
        print("Mod Name: {}\nMod ID: {}\n".format(mod["name"], mod["id"]))

if DEBUG:
    del mod_list
