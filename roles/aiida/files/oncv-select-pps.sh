# Selec v1.1 PPs, where they exist
# naming scheme: Br_ONCV_PBE-1.0.upf

re="(\w+)_ONCV_PBE-(...).upf"
for fname in *-1.0.upf; do
    [[ $fname =~ $re ]] && element=${BASH_REMATCH[1]}
    fname_new="${element}_ONCV_PBE-1.1.upf"
    if [ -e $fname_new ]; then
        rm $fname
    fi
done
