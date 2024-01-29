#!/bin/bash
# Update the index for all release tags

printf "# GROK Toolkit Releases\n\n" > README.md
rm -rf releases

# 3.0.0a1 has no versions file.
for tag in "master" $(git tag -l "4*" -l "3*" | sort -r | grep -v "3.0.0a1"); do
    echo $tag
    mkdir -p releases/$tag
    git show $tag:grok-versions.cfg > releases/$tag/grok-versions.cfg
    printf "## $tag\n\n- [grok-versions.cfg](releases/$tag/grok-versions.cfg)\n\n" >> README.md;
done

# Add a footer
printf "\n_____\n\n" >> README.md
printf "[How to maintain this page](HOWTO.md)\n" >> README.md
