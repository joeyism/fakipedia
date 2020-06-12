from tqdm import tqdm
import re
import sys

EOT = "<|endoftext|>\n"

if len(sys.argv) == 1:
  print("Please provide filename")
  sys.exit(1)

in_filename = sys.argv[1]
print(f"Running for {in_filename}")
data = []
with open(in_filename, "r") as f:
  for line in tqdm(f.readlines(), desc="Reading"):
    if re.search("^ = ([a-zA-Z]+)", line):
      data.append(EOT)
      data.append("\n")
    data.append(line)

in_filename_split = in_filename.split(".")
out_filename = ".".join(in_filename_split[:1] + ["eot"] + in_filename_split[1:])

with open(out_filename, "w+") as g:
  print(f"Writing to {out_filename}")
  g.writelines(data[2:])

print("Done")
