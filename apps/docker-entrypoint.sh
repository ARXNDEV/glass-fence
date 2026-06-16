#!/bin/sh
set -e
# Map every GF_* variable to its GF_* equivalent
for var in $(env | grep '^GF_' | cut -d= -f1); do
    gf_var="GF_${var#GF_}"
    val=$(eval echo \$$var)
    export "$gf_var=$val"
done
exec /usr/bin/glass-fence "$@"
