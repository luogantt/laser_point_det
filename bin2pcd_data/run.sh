i=1;for x in ./*.bin; do ./build/bin2pcd --infile $x --outfile ./$i.pcd; let i=i+1; done
