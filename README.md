# space-dedupe
Mass Merge Duplicate Objects in Space SD
These scripts are based on the work of Sandeep Rajan.  So all credit to him, and blame to me.
The goal is to merge duplicate objects for consistent naming.  There is no way in the GUI to do this in bulk and my customer has 1200+ duplicates so doing manually was not an option.


#duplicate_addresses.py 
Will connect to Space/SD and merge duplicate address items to a single item named after the first deplicate found in the list

#duplicate_services.py 
Will connect to Space/SD and merge duplicate service objects to a single item named after the first deplicate found in the list

#Server.py
Function definitions imported by above scripts
