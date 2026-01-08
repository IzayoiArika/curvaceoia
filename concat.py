import argparse
import os
import sys

def main():
	# parser = argparse.ArgumentParser(description='Concatenate files recursively with headers')
	# parser.add_argument('--path', default='.', help='Directory to process (default: current directory)')
	# parser.add_argument('--output', required=True, help='Output file name')
	# args = parser.parse_args()
	
	# path = args.path
	# output =  args.output

	path = r"D:\Programming\arikacus\curvaceoia"
	output = 'output.txt'
	target_dir = os.path.abspath(path)
	output_file = os.path.join(target_dir, output)

	if not os.path.isdir(target_dir):
		print(f"Error: Directory not found - {target_dir}")
		sys.exit(1)

	try:
		with open(output_file, 'w', encoding='utf-8') as outfile:
			file_count = 0
			
			for root, dirs, files in os.walk(target_dir):
				for filename in files:
					
					file_path = os.path.join(root, filename)
					relative_path = os.path.relpath(file_path, start=target_dir)
					full_path = os.path.join(os.path.abspath(root), filename)
					
					try:
						with open(file_path, 'r', encoding='utf-8') as infile:
							content = infile.read()
					except UnicodeDecodeError:
						continue
					except Exception as e:
						print(f"Error reading {full_path}: {str(e)}")
						continue
					
					outfile.write(f"## {full_path}\n")
					outfile.write(content)
					
					# Add separator if content doesn't end with newline
					if content and content[-1] != '\n':
						outfile.write('\n')
					
					outfile.write('\n')
					file_count += 1
			
			print(f"Successfully concatenated {file_count} files to {output_file}")
	
	except Exception as e:
		print(f"Error writing output: {str(e)}")

if __name__ == "__main__":
	main()