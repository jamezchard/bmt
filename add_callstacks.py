from pathlib import Path
from bmt_v2bm import v2bm

import sys
import re


def main() -> None:
    # will try to support more kinds of callstacks
    regex_gpuview = r"(\S*\.dll!.*) \[(.*) \@ (\S*)\]"
    with open(sys.argv[1], mode="r", encoding="utf-8") as txt:
        for textline in txt:
            matches = re.findall(regex_gpuview, textline.strip(), re.MULTILINE)
            assert len(matches) == 1 and len(matches[0]) == 3
            label, pos, line = matches[0]
            v2bm(Path(pos), int(line), str(label))


if __name__ == "__main__":
    main()
