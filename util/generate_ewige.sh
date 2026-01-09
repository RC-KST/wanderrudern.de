#!/usr/bin/sh

./util/build_yearly_list.py -f \
    -b ./wettbewerbe/ewige_liste/ewige_kilometerliste_base.csv \
    -o ./content/club/wettbewerbe/ewige_kilometerliste/ewige_kilometerliste_new.csv \
    -d ./wettbewerbe/ewige_liste
