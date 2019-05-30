import os 
import shutil
import time
import errno
import time
import sys
import logging
import logging.config



source = r'C:\Users\Desktop\BetaSource'
dest = r'C:\Users\Desktop\BetaDest'
#Gets the current time from the time module
now = time.time()
#Timer of when to purge files
cutoff = now - (14 * 86400)
source_list = []
all_sources = []
all_dest_dirty = []
logging.basicConfig(level = logging.INFO, filename = time.strftime("main-%Y-%m-%d.log"))

def main():
	dest_files()
	purge_files()
#I used the dess_files function to get all of the destination files
def dest_files():
	for dest_root, dest_subdirs, dest_files in os.walk(dest):
		for f in dest_files:
			global All_dest_dirty
			all_dest_dirty.append(f)	
			
def purge_files():
	logging.info('invoke purge_files method')
	#I removed all duplicates from dest because cleaning up duplicates in dest is out of the scope
	all_dest_clean = list(dict.fromkeys(all_dest_dirty))
	#os.walk used to get all files in the source location 
	for source_root, source_subdirs, source_files in os.walk(source):
		#looped through every file in source_files
		for f in source_files:
			#appending all_sources to get the application name from the file path
			all_sources.append(os.path.abspath(f).split('\\')[-1]) 
			#looping through each element of all_source
			for i in all_sources:
				#logical check to see if file in the source folder exists in the destination folder
				if i not in all_dest_clean:
					#src is used to get the path of the source file this will be needed to move the file in shutil.move
					src =  os.path.abspath(os.path.join(source_root, i))
					#the two variables used below are to get the creation time of the files
					t = os.stat(src)
					c = t.st_ctime
					#logical check to see if the file is older than the cutoff
					if c<cutoff:
						logging.info(f'File has been succesfully moved: {i}')
						print(f'File has been succesfully moved: {i}')
						shutil.move(src,dest)
						#removing the allready checked source files for the list this is also used in other spots within the loop
						all_sources.remove(i)
					else:
						logging.info(f'File is not older than 14 days: {i}')
						print(f'File is not older than 14 days: {i}')
						all_sources.remove(i)
				else:
					all_sources.remove(i)
					logging.info(f'File: {i} allready exists in the destination')
					print(f'File: {i} allready exists in the destination')
if __name__ == '__main__':
    main()
