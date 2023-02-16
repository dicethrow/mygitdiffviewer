#!/usr/bin/env python3

import argparse, logging, os

if __name__ == "__main__":
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

	logging.info("---")
	logging.info(f"file1 is {args.file1}")
	logging.info(f"file2 is {args.file2}")

	
