# copy_newer_files
It uses the Linux "cp" command to copy only the missing or newer files from the source directory to the destination directory.

When I was testing the performance of "rsync", while copying about 100GB of files from the internal SSD of my MacBook Pro to the external Thunderbolt 3 SSD,
I realised that using "cp" instead was about 3 to 5 times faster.
So I made this little python script, to scan for missing files from the destination directory,
or files in the source directory with their modification date being newer than those in the destination directory and copy only those.

The python script will also display the performance while copying the files, and an overall performance at the end.
