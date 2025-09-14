"""
Script used for joining large data files that were split to allow for upload to GitHub. Max file
size is 100MB.
"""

import os
import re


def join_csv(parts, output_file):
    with open(output_file, "w", encoding="utf-8") as out:
        first = True
        for part in parts:
            with open(part, "r", encoding="utf-8") as f:
                if first:
                    out.write(f.read())
                    first = False
                else:
                    f.readline()  # skip header
                    out.write(f.read())
    print(f"✅ Rejoined into {output_file}")


if __name__ == "__main__":
    data_dir = "post_flight/data"
    part_files = [f for f in os.listdir(data_dir) if f.startswith("part_")]
    if not part_files:
        print("⚠️ No part_ files found in data/")
        exit(1)

    # Group by the original large_ filename
    groups = {}
    for f in part_files:
        # Extract original filename after part_N_
        match = re.match(r"part_\d+_(large_.*)", f)
        if match:
            orig = match.group(1)
            groups.setdefault(orig, []).append(f)

    # Rebuild each large_ file
    for orig, parts in groups.items():
        parts.sort(key=lambda x: int(x.split("_")[1]))  # sort by part number
        output_file = os.path.join(data_dir, orig)
        part_paths = [os.path.join(data_dir, p) for p in parts]
        join_csv(part_paths, output_file)
