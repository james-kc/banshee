"""
Script used for splitting large data files to allow for upload to GitHub. Max file size is 100MB.
"""

import os

CHUNK_SIZE = 99 * 1024 * 1024  # 99MB


def split_csv(file_path, chunk_size=CHUNK_SIZE):
    base_name = os.path.basename(file_path)
    dir_name = os.path.dirname(file_path)
    name, ext = os.path.splitext(base_name)

    with open(file_path, "r", encoding="utf-8") as f:
        header = f.readline()
        part_num = 1
        out_file = os.path.join(dir_name, f"part_{part_num}_{base_name}")
        out = open(out_file, "w", encoding="utf-8")
        out.write(header)
        written = len(header.encode("utf-8"))

        for line in f:
            line_size = len(line.encode("utf-8"))
            if written + line_size > chunk_size:
                out.close()
                part_num += 1
                out_file = os.path.join(dir_name, f"part_{part_num}_{base_name}")
                out = open(out_file, "w", encoding="utf-8")
                out.write(header)
                written = len(header.encode("utf-8"))

            out.write(line)
            written += line_size

        out.close()

    print(f"✅ Split {file_path} into {part_num} parts")


if __name__ == "__main__":
    data_dir = "post_flight/data"
    for fname in os.listdir(data_dir):
        if fname.startswith("large_"):
            split_csv(os.path.join(data_dir, fname))
