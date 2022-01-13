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

It has not been tested on windows or Mac yet.  It was developed on linux mint 20.3 una in Anaconda.

Detailed usage:
There is a salt.  You should set the salt either on the command line or by editing the default on line 20 of the code.
This is the foundation of making your installation unique.  That way someone needs YOUR personalized copy 
of cloakpass in order to generate similar passwords.  This is the thing you "own"

There is a Key.  This is something you know.  It should be memorable and simple. You enter this every time on the command line
when starting cloakpass.

Finally there is a unique identifier for each password you need.  IE  mybank, myFacebook (just kidding) or just ebay. 

These things make up your password which is hashed with Sha512, then patterned with whatever special chars, numbers or caps
your password needs.

The principle is that passwords that are memorable are easy to crack and passwords that are hard to crack are difficult to remember.
Cloak pass solves this problem by putting together 2 things you know that are easy to remember and hashing them into 
a password that is hard to crack.  No passwords are stored anywhere not even encrypted.  The two things (key and password) are only 
in your head so there is nothing to steal, nothing to crack and nothing to find.  Without your copy of cloakpass no reasonable
hacker is going to be able to crack your passwords and since large portions of data were removed it is not possible to reverse
the hash to your original two salt, key, and password.  

I hope you enjoy this updated version of CloakPass!  
