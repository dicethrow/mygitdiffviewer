#!/usr/bin/env python3

import argparse, logging, os, shutil, io
from git import Repo
 
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("DIR", help="parent folder of this script")
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

	def parse_gitk_filename(gitk_filename):
		# as gitk gives weirdly structured `filenames`
		# perhaps this is due to my use of git submodules?
		# like this: 
		# /home/x/Documents/git_repos/general/general_electronics/.git/modules/modules/2022/M-CAM-OV5640/.gitk-tmp.ZPDRq6/3/[3b3d07fee13f4fd7141db379282c73d263ffc48e] v1.kicad_pcb
		# /dev/null
		if gitk_filename == "/dev/null":
			logging.info("filename is null")
			return None
		else:
			path_to_repo, remainder = gitk_filename.split("/.gitk-tmp")
			remainder, git_sha, filename = remainder.replace("[", "] ").split("] ")

			# test = path_to_repo + "/.gitk-tmp" + j# + filename
			# shutil.copytree(test, os.path.join(args.DIR,"testdir2"))
			# with open(test, "r") as f:
				# logging.info(f.readlines())

			remainder, filename = gitk_filename.split(" ")
			logging.info(f"filename is: {filename}")
			path_to_repo, path_within_repo, remainder = remainder.split("/.git")
			path_within_repo = path_within_repo[1:] # remove leading slash
			path_within_repo = os.path.join(path_within_repo, filename)

			logging.info(f"path_to_repo is: {path_to_repo}")
			logging.info(f"path_within_repo is: {path_within_repo}")
			
			_, sha, _ = remainder.replace("]","[").split("[")
			logging.info(f"sha is: {sha}")




			path_to_repo = os.getcwd()
			originalRepo = Repo(path_to_repo)
			commit = originalRepo.commit(sha)
			# for d in dir(commit):
				# logging.info(d)
			for k,v in commit.stats.files.items():
				if filename in k:
					logging.info(f"The full path of {filename} is assumed to be {k}! nice - now deal with it")
					filename = k

			targetfile = commit.tree / filename#'filea'

			# Retrieve contents of targetfile

			with io.BytesIO(targetfile.data_stream.read()) as f:
				logging.info(f.read().decode('utf-8'))

			return path_to_repo, path_within_repo, sha
		

	path_to_repo, path_within_repo_1, sha_1 = parse_gitk_filename(args.file1)
	path_to_repo, path_within_repo_1, sha_2 = parse_gitk_filename(args.file2)

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

