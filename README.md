# Tibia Look Loot Calculator

This is yet another loot calculator for the Tibia MMORPG. If you've ever used Tibia Wiki's loot calculator, this is pretty much like that one, except way simpler. It works by reading the text you get from looking at items, parsing each item and quantity, and then summing it all up in the end.

There are probably some corner cases I haven't considered, so take the results with a grain of salt. Feel free to report bugs.

## Usage


### With the "paste.txt" file:

 1. On the Tibia client, clear your server log channel and look at every item you want to sell to NPCs. This includes looking at ALL items you want to sell, even if they're duplicates.
 2. Copy everything in your server log and paste it into a text file called "paste.txt". Place this text file in the same directory as the `lootcalc.py` script. An example file is provided.
 3. Run the `lootcalc.py` script. It will print out the total gold value of the items you looked at.

### With the clipboard (Windows only):

 1. On the Tibia client, clear your server log channel and look at every item you want to sell to NPCs. This includes looking at ALL items you want to sell, even if they're duplicates.
 2. Copy everything in your server log to your clipboard (simply press Ctrl+C).
 3. Run the `lootcalc.py` script with the `-c` option, e.g. `python lootcalc.py -c`. It will print out the total gold value of the items you looked at.


## Important Notes

 - The `sorted_items_and_values.csv` file includes each item's name and their NPC value in the `singular_name,plural_name,weight,value` format. It was built using the [tibiawiki-sql](https://github.com/Galarzaa90/tibiawiki-sql) project.
 - This calculator has not yet been updated with the new look message format, which includes the quantity of every item, like "10 ham" or "16 meat", but it still works regardless.

## Future Features

The calculator is still very simple. It only reads your logs and spits out the total value. Someday, it might:

 - Also print the amount of each item and their value;
 - Show which NPC buys each item;
 - Have a simple GUI;
 - ... more? Who knows!
