# CloakPass
Password Hasher

CloakPass was written in python 3.9.7 and pynput 1.7.6

Set the path to your python executable in the first line of cloakpass.py and change permissions to executable.
Run CloakPass from the command line with cloakpass.py&.  
CloakPass will sit quietly in the background and wait for cntl-alt-p.
When it receives that key combination it will start actively listning to keystrokes and lock the keyboard for it's exclusive use.
At this point start typing your password.  
After you are ready to see your password press either enter or tab and your hashed password will be displayed.
You can then go about your work waiting till the next time you need a password.
It works throughout the xwindows environment including browsers and inside seperate terminals.
When you want to stop cloakpass press cntl-alt-e and it will exit.
There is a salt, a key, and your password which make up the string which will be hashed.
you can specify these on the command line.  Type cloakpass.py --help for more information.
Some keywords are not implemented yet like including/removing numbers and capitals.  They are included by default.
It has not been tested on windows or Mac yet.  It was developed on linux mint 20.3 una in Anaconda.
