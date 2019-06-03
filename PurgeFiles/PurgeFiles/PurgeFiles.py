import os 
import shutil
import time
import errno
import time
import sys
import logging
import logging.config



source = r'C:\Users\q155344\Desktop\BetaSource'
dest = r'C:\Users\q155344\Desktop\BetaDest'
#A timer was needed to know when to purge files 
cutoff = time.time() - (14 * 86400)
source_list = []
all_sources = []
logging.basicConfig(level = logging.INFO, filename = time.strftime("main-%Y-%m-%d.log"))
#I had to create a funciton that would grab all the destination files.
def dest_files():
	dirty_files = []
	for dest_root, dest_subdirs, dest_files in os.walk(dest):
		for f in dest_files:
			dirty_files.append(f)
	return dirty_files		
all_dest_dirty = dest_files()
def purge_files():
	logging.info('invoke purge_files method')
	#I removed all duplicates from dest because cleaning up duplicates in dest is out of the scope
	all_dest_clean = set(all_dest_dirty)
	#os.walk was used because I needed to get a lost of all the files in the source location
	for source_root, source_subdirs, source_files in os.walk(source):
		for f in source_files:
			#I needed just the application name from the full path to compare its value to the destination. The destination set is just the application name not the full path.
			all_sources.append(os.path.abspath(f).split('\\')[-1]) 
			for i in all_sources:
				# I needed to check if the source file was in the destination. 
				if i not in all_dest_clean:
					src =  os.path.abspath(os.path.join(source_root, i))
					t = os.stat(src)
					c = t.st_ctime
					#I only want to move the files that are older then the defined cutoff
					if c<cutoff:
						logging.info(f'File has been succesfully moved: {i}')
						print(f'File has been succesfully moved: {i}')
						shutil.move(src,dest)
						all_sources.remove(i)
					else:
						logging.info(f'File is not older than 14 days: {i}')
						print(f'File is not older than 14 days: {i}')
						all_sources.remove(i)
				else:
					all_sources.remove(i)
					logging.info(f'File: {i} allready exists in the destination')
					print(f'File: {i} allready exists in the destination')

def main():
	dest_files()
	purge_files()

if __name__ == '__main__':
    main()
