sudo ./p4 set P4PORT=perforce:166
./p4 set P4USER=bagarwal
./p4 -u bagarwal login
./p4 set P4CLIENT=cdi-devops
./p4 sync //Florence/buildOps/Applications/InfaEnvJsonGenerator/data/Properties/test/pod-cdi-services.properties
python ami.py
export cl=`./p4 change -o | grep '^\(Change\|Client\|User\|Description\)' | ./p4 change -i | cut -d ' ' -f 2`
./p4 edit -c $cl /Users/bagarwal/Perforce/cdi-devops/Florence/buildOps/Applications/InfaEnvJsonGenerator/data/Properties/test/pod-cdi-services.properties
./p4 submit -c $cl%