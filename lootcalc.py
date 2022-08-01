# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

# Feel free to contact me at GitHub

import math
import re
import os
import sys

item_data = []
item_names = set()

def load_csv_into_memory():
    with open ("./sorted_items_and_values.csv", "r") as f:
        for line in f:
            line = line[:-1].split(",")
            object = {
                "name": line[0],
                "plural": line[1],
                "weight": float(line[2]),
                "value": int(line[3])
            }
            item_data.append(object)
            item_names.add(line[0])
            item_names.add(line[1])


def parse_input(file,clipboard = None):
    with open(f"{file}", "r") as f:
        itemlist = []
        parsed_item = []
        if clipboard != None:
            f = clipboard
        for line in f:
            item = re.findall(r"You see (\d*)[\s]*([^.\(]+)", line)
            if item:
                item = list(item[0])
                # Now, item[0] holds the amount and item[1] holds item name

                # Remove "a", "an" and whitespaces
                if item[0] == "" and item[1][0] == "a":
                    if item[1][1:3] == "n ":
                        item[1] = item[1][3:]
                    elif item[1][1] == " ":
                        item[1] = item[1][2:]
                if item[1][-1] == " ":
                    item[1] = item[1][:-1]

                # Remove "that..." for rings
                if "that is" in item[1] or "that will" in item[1]:
                    aux = ""
                    item[1] = item[1].split(" ")
                    for word in item[1]:
                        if word == "that":
                            break
                        else:
                            aux = aux + word + " "
                    item[1] = aux[:-1]
                if item[0] == "":
                    parsed_item.append(item[0])
                else:
                    parsed_item.append(int(item[0])) # amount
                parsed_item.append(item[1]) # name

            weight = re.findall(r"weighs? (\d+.\d\d)", line)
            if weight:
                parsed_item.append(float(weight[0])) # weight
                itemlist.append(parsed_item)
                parsed_item = []

    return itemlist


def calculate_value(item_list):
    # item[0] = amount
    # item[1] = name
    # item[2] = weight
    total_value = 0
    for item in item_list:
        if item[1] in item_names:
            singular_item = next((it for it in item_data if it["name"] == item[1]), False)
            if singular_item:
                if math.isclose(item[2], singular_item["weight"], abs_tol=0.001):
                    total_value += singular_item["value"]
                else:
                    total_value += (item[2]/singular_item["weight"]) * singular_item["value"]
            else:
                plural_item = next((it for it in item_data if (it["plural"] == item[1]) and math.isclose(item[2], item[0] * it["weight"], abs_tol=0.001)), False)
                if plural_item:
                    total_value += plural_item["value"] * item[0]
    return int(total_value)


load_csv_into_memory()
#use -c to read input from clipboard and also spit out to it
#note: this is only for windows mostly because i couldnt get the tkinter function that writes to the clipboard to work
if os.name == "nt" and len(sys.argv) >= 2 and sys.argv[1] == "-c":
    from tkinter import Tk
    r = Tk()
    r.withdraw()
    s = r.clipboard_get()
    r.destroy()
    
    item_list = parse_input("paste.txt",s.splitlines())
    loot_value = calculate_value(item_list)
    
    os.system('echo | set /p result=' + str(loot_value) + '| clip')
#read from file
else:
    item_list = parse_input("paste.txt")
    loot_value = calculate_value(item_list)
print(loot_value)
