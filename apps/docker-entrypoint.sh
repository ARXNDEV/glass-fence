#!/bin/sh
set -e
# Map every GF_* variable to its NEKO_* equivalent
# The Go binary internally expects NEKO_* env vars.
# Operators only ever set GF_* variables.
for var in $(env | grep '^GF_' | cut -d= -f1); do
    neko_var="NEKO_${var#GF_}"
    val=$(eval echo \$$var)
    export "$neko_var=$val"
done
exec /usr/bin/glass-fence "$@"
