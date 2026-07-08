#!/usr/bin/env python3
"""Generate 1201v0227.mib tree (wrapper)."""
from gen_mib_tree import MIB_CONFIGS, generate_tree

if __name__ == "__main__":
    generate_tree(MIB_CONFIGS["1201v0227.mib"])
