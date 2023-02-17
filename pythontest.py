#!/usr/bin/env python3

import argparse, logging, os, shutil, io
from git import Repo
 
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("DIR", help="parent folder of this script")
	parser.add_argument("GITDIR", help="the folder containing .git of this repository")
	parser.add_argument("file1", help="path of the first kicad file to diff, from one git commit")
	parser.add_argument("file2", help="path of the second kicad file to diff, from other git commit")
	args = parser.parse_args()

	logging.basicConfig(filename=os.path.join(args.DIR,"app.log"),
		filemode='a',
		format='%(asctime)s %(msecs)d %(name)s %(levelname)s %(message)s',
		datefmt='%H:%M:%S',
		level=logging.DEBUG)

	logging.info("\n---")
	logging.info(f"file1 is {args.file1}")
	logging.info(f"file2 is {args.file2}")

	TEMPDIR = os.path.join(args.DIR, "tempdir")

	def clearTempDir():
		shutil.rmtree(TEMPDIR, ignore_errors=False, onerror=None)

	def saveLocalCopyOfMatchedFiles(gitk_filename):
		# as gitk gives weirdly structured `filenames`
		# perhaps this is due to my use of git submodules?
		# like this: 
		# /home/x/Documents/git_repos/general/general_electronics/.git/modules/modules/2022/M-CAM-OV5640/.gitk-tmp.ZPDRq6/3/[3b3d07fee13f4fd7141db379282c73d263ffc48e] v1.kicad_pcb
		# /dev/null
		if gitk_filename == "/dev/null":
			logging.info("filename is null")
			return None
		else:
			remainder, sha, filename = gitk_filename.replace("[", "] ").split("] ")
			logging.info(f"filename is: {filename}")
			logging.info(f"sha is: {sha}")

		
			# path_to_repo = os.getcwd()
			filePathsToView = []
			commit = Repo(args.GITDIR).commit(sha)
			logging.info(f"commit items: {commit.stats.files}")
			for key,value in commit.stats.files.items():
				if filename in key:
					key = key.split(" => ")[-1] # handle matches of renames, like: v1.kicad_pcb => main.kicad_pcb so we just get the resultant filename

					logging.info(f"The relative path of {filename} within this repo is assumed to be {key}! nice - now deal with it. note this approach may make duplicate matches")
					filePathsToView.append(key)
			
			dest_filenames = []
			for filenameMatch in filePathsToView: # should just be one... todo: work out how to ensure we always get the one true match only

				targetfile = commit.tree / filenameMatch # what the hell is this / syntax

				with io.BytesIO(targetfile.data_stream.read()) as source_f:
					dest_filename = f"{sha[:5]}_{filenameMatch}" # use first 5 sha characters...? is that enough characters? is this the right approach?
					full_dest_filename = os.path.join(TEMPDIR, dest_filename) # note that dest_filename may include subdirectories
					os.makedirs(os.path.dirname(full_dest_filename), exist_ok=True)
					
					with open(full_dest_filename, "wb") as dest_f: 
						# logging.info(source_f.read().decode('utf-8'))
						dest_f.write(source_f.read())
					
					dest_filenames.append(full_dest_filename)

			return dest_filenames
		

	clearTempDir()

	dest_filenames = []

	result = saveLocalCopyOfMatchedFiles(args.file1)
	if result:
		dest_filenames += result

	result = saveLocalCopyOfMatchedFiles(args.file2)
	if result:
		dest_filenames += result

	for filename in dest_filenames:
		logging.info(f"saved filename: {filename}")


	# temp_repo_dir = os.path.join(args.DIR, "temprepo")
	# path_to_repo = os.getcwd()
	# originalRepo = Repo(path_to_repo)

	# tree = originalRepo.head.commit.tree

	
	
	# logging.info("dir of tree:")
	# for d in dir(tree):
		# logging.info(d)
	

	# cloned_repo = originalRepo.clone(os.path.join(path_to_repo, temp_repo_dir))	


if __name__ == "__main__":
	try:
		main()	
	except Exception as e:
		logging.error(e, exc_info=True)

