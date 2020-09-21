# coding=utf-8
# https://curse.nikky.moe
import json
import time

total_start_time = time.time()

# Start reading mod list
read_start_time = time.time()

mod_list_file = open("mod_list.json", "r")
mod_list = json.load(mod_list_file)
mod_list_file.close()

read_end_time = time.time()
read_time_taken = read_end_time - read_start_time
print(f"It took {read_time_taken * 1000}ms to read the mod list.")

# Start parsing mod list
parse_start_time = time.time()

parsed_mod_list = []
for mod in mod_list["data"]["addons"]:
    mod_details = {"name": mod["name"],
                   "url": mod["websiteUrl"],
                   "downloads": int(mod["downloadCount"]),
                   "date_created": mod["dateCreated"],
                   "date_released": mod["dateReleased"],
                   "date_modified": mod["dateModified"],
                   "short_description": mod["summary"]}
    try:
        mod_details["latest_supported_version"] = mod["gameVersionLatestFiles"][0]["gameVersion"]
    except IndexError:
        mod_details["latest_supported_version"] = None
    parsed_mod_list.append(mod_details)

print(f"Mod list is {len(parsed_mod_list)} mods long!")

parse_end_time = time.time()
parse_time_taken = parse_end_time - parse_start_time
print(f"It took {parse_time_taken * 1000}ms to parse the mod list.")

# Start sorting the mod list
sort_start_time = time.time()

sorted_parsed_mod_list = sorted(parsed_mod_list, key=lambda k: k["name"].lower())

sort_end_time = time.time()
sort_time_taken = sort_end_time - sort_start_time
print(f"It took {sort_time_taken * 1000}ms to sort the mod list.")

# Start adding IDs to the mod list
id_add_start_time = time.time()

sorted_parsed_mod_list_with_ids = []
for mod, i in zip(sorted_parsed_mod_list, range(1, len(sorted_parsed_mod_list))):
    mod["id"] = i
    sorted_parsed_mod_list_with_ids.append(mod)

id_add_end_time = time.time()
id_add_time_taken = id_add_end_time - id_add_start_time
print(f"It took {id_add_time_taken * 1000}ms to add IDs to the mod list.")

# Start writing the file
write_file_start_time = time.time()

parsed_mod_list_file = open("parsed_mod_list.json", "w")
json.dump(sorted_parsed_mod_list_with_ids, parsed_mod_list_file, indent=2)
parsed_mod_list_file.close()

write_file_end_time = time.time()
write_file_time_taken = write_file_end_time - write_file_start_time
print(f"It took {write_file_time_taken * 1000}ms to write the mod list.")

# Finish everything
total_end_time = time.time()
total_time_taken = total_end_time - total_start_time
print(f"It took {total_time_taken * 1000}ms to do all operations.")
