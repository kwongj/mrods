#!/usr/bin/env python
# Script by JK

from __future__ import print_function

# Modules
import argparse
from argparse import RawTextHelpFormatter
import os
import re
import subprocess
from subprocess import Popen
import tempfile
from Bio.Blast.Applications import NcbiblastnCommandline

# Use BLAST to check if query sequence is present in genome
def blast_check(query, ref):
	with tempfile.TemporaryDirectory() as dirpath:		# Note python3 syntax
		blastdbpath = os.path.join(dirpath, 'ref')
		# Create BLAST DB
#		print('makeblastdb -in {} -out {} -dbtype nucl'.format(ref, blastdbpath))
		proc = subprocess.Popen(['makeblastdb', '-in', ref, '-out', blastdbpath, '-dbtype', 'nucl'], stdout=subprocess.PIPE)
		procOUT = proc.communicate()[0]
		# Run NCBI blastn
		fBLAST = NcbiblastnCommandline(query=query, db=blastdbpath, outfmt='6', perc_identity='90', qcov_hsp_perc='70')
		stdout, stderr = fBLAST()
		return stdout

# Check if file is in FASTA format
def check_fasta(f):
	if not os.path.isfile(f) or os.path.getsize(f) < 1:
		return False
	with open(f, 'r') as fasta:
		if fasta.readline()[0] != '>':
			return False
		for line in fasta:
			line = line.strip()
			if not line or line[0] == '>':
				continue
			if bool(re.search('[^ACTGactg]', line)):
				return False
	return True

def main():
	# Usage
	parser = argparse.ArgumentParser(
		formatter_class=RawTextHelpFormatter,
		description='BLAST check to see if sequence is present',
		usage='\n  %(prog)s --query <query> <fasta>')
	parser.add_argument('fasta', metavar='FILE', nargs='+', help='reference sequence file in FASTA format (required)')
	parser.add_argument('--query', metavar='FILE', nargs=1, required=True, help='query sequence in FASTA format (required)')
	parser.add_argument('--version', action='version', version=
		'%(prog)s v0.1\n')
	args = parser.parse_args()

	for f in args.fasta:
		# Check input file is FASTA format
		if check_fasta(f) != True:
			print('{}\tERROR: Check file exists and is in FASTA nucleotide format.'.format(f))
			continue
		output = blast_check(args.query[0], f)
		print(output)

if __name__ == "__main__":
	main()