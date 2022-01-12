#!/usr/bin/env python3

"""CloakPass copyright 1994 MtxDev.

# version P_2.01rc Dec 2021 by MtxDev
# The previous versions were written in Visual Basic.
# cntl alt p turns on the listener.
# Key's are captured upon tab or enter
# the hashed string is output.
# Two command line arguments are input a salt and a key
# This makes each usage unique.
# cntl alt e ends the program
"""
import argparse

parser = argparse.ArgumentParser(description='CloakPass Password Hasher')
parser.add_argument('--key', type=str, default="mycloakkey",
                    help='enter an easy to remember cloaking key or phrase')
parser.add_argument('--salt', type=str,
                    default='_489e7(*79#$^3vJIUYHJHJKKJHcloaking' +
                    'salt24127491871324789871234',
                    help='enter a long unchanging system' +
                    'cloaking starting point')
parser.add_argument('--passlen', type=int, default=12,
                    help="the max password length")
parser.add_argument('--spcchars', type=bool, default=True,
                    help="include special chars (True or False)")
parser.add_argument('--caps', type=bool, default=True,
                    help="include capital letters (True or False)")
parser.add_argument('--numbers', type=bool, default=True,
                    help="include numbers (True or False)")
parser.add_argument('--showpass', type=bool, default=False,
                    help="Show plain text password as you type it")
parser.add_argument('--showstars', type=bool, default=False,
                    help="Shows plain text * as you type")

myargs = parser.parse_args()


class CloakPass():
    """MtxDev's password hasher.

    Listen for cntl alt p then collect characters
    upon an enter or tab then hash them.
    Following an enter or tab replace
    them with the hashed string and reset to
    listen for the next Crtl alt p.
    if you press shift alt c it will launch a small gui
    to change the hash or exit the program
    """

    # needed for MD5 Hash functions
    import hashlib
    from collections import OrderedDict
    import base64
    mybase64 = base64
    myOrderedDict = OrderedDict
    # used for main message loop
    import time
    mysleep = time.sleep
    mytime = time
    # used for keyboard control of application
    # from pynput import keyboard
    # used for readability convience everything is in keyboard
    from pynput.keyboard import Key, Listener, Controller, GlobalHotKeys
    #  myKey = ""  # Key
    lisKeys = ""  # Listener
    myController = ""  # Controller
    # myGlobalHotKeys = "" # GlobalHotKeys
    lisHotKey = ""  # Place holder will be assigned in a method
    lstHotKeys = ""  # Place holder will be assigned in a method

    # Password Settings
    # Three items make up the hash.  A Salt, a Key and Password
    # The Salt is something you own
    # The Key is something you are
    # The Password is something you know
    sSalt = "salt1"
    sKey = "key1"
    iPassLen = 12
    bSpcChars = True
    bCaps = True
    bNums = True
    PassWord = ""  # Holds the password prior to hashing
    HashedPassWord = ""  # Holds the result of the hash temporaraly

    # System Settings
    fDefaultLoopDelay = 2  # This is default sleep delay for the message looper
    fLoopDelay = 2  # This is the sleep delay for the message loop looper
    iDebugLevel = 0  # debug level 1-5 for which messages you want to see
    bShowPass = False  # Do we type the password for the user or hide it
    bShowStars = False  # Do we type stars for the user or hide letter count
    sHotKeyP = '<ctrl>+<alt>+p'  # Hotkey for starting the password session
    sHotKeyI = '<ctrl>+<alt>+e'  # Hotkey for shutting down CloakPass

    # Flags
    bHotKeyP = False  # flag to control the start of the listener
    bHotKeyI = False  # flag to control shutdown of the app
    bInPass = False  # used to start capturing keys for password
    bStopLooper = False  # sets flag to stop the message loop
    bPauseListener = False  # prevents looping in listener callbacks
    bListening = False  # Keeps track of whether keylistener is running
    bSendOutput = False  # flag for looper to send final output

    # keywords
    _Suppress_ = True  # Used to flag the suppression of all keyboard events
    _NoSuppress_ = False  # Used to flag no suppression of all keyboard events
    _Start_ = True  # Used for the Listeners bStartStop
    _Stop_ = False  # Used for the Listeners bStartStop

    def __init__(self, sSalt: str = "salt",
                 sKey: str = "key",
                 iPassLen: int = 12,
                 bSpcChars: bool = True,
                 bCaps: bool = True,
                 bNums: bool = True,
                 bShowPass: bool = False,
                 bShowStars: bool = False,
                 ) -> None:
        self.sSalt = sSalt
        self.sKey = sKey
        self.iPassLen = iPassLen
        self.bSpcChars = bSpcChars
        self.bCaps = bCaps
        self.bNums = bNums
        self.bShowPass = bShowPass
        self.bShowStars = bShowStars
        if bShowStars is True:
            self.bShowPass = False

        self.myController = self.Controller()

    def main(self) -> None:
        """Initialize and start Listener."""
        self.debug(1, "starting", "Main")
        self.HotKeyListener(self._Start_)
        self.looper(self.fDefaultLoopDelay)

#        print("stopping now")

    def SendOutput(self):
        """Send the password and backspaces if flag is set.

        This is necessary becasue the keyboard thread does not shut down
        immediately.  So you have to loop till it does.  Once shut down
        then you can echo keystrokes.
        """
        if self.bSendOutput is True:
            if self.bListening is False:  # don't send if listener is running
                if ((self.bShowPass is True) or
                        (self.bShowStars is True)):
                    # send bkspces when pwd is shown
                    self.debug(2, "sending backspaces", "SendingOutput")
                    self.Send_backspaces(len(self.PassWord)+1)
                    self.PassWord = ""
                self.Send_HashedPassword(self.HashedPassWord)
                self.debug(2, "Sending output:"
                           + self.HashedPassWord, "SendingOutput")
                self.bSendOutput = False
                # change the loop delay here instead of at the keylistener exit
                # because otherwise there will be a delay upon sending
                # backspaces
                self.fLoopDelay = self.fDefaultLoopDelay
            else:
                self.KeyListener(self._Stop_)

    def CheckFlags(self, bPress: bool, key) -> None:
        """Set Crtl alt p flags etc.

        this is run on every key down and key release
        bPress is true for press event
        bPress is false for release event
        """
        if bPress is True:
            if self.bInPass is True and (
                    key == self.Key.enter or key == self.Key.tab
                    ):
                self.bInPass = False
                self.debug(2, "passwd:" + self.PassWord, "CheckFlags")
                self.debug(2, "sSalt:" + self.sSalt, "CheckFlags")
                self.debug(2, "sKey:" + self.sKey, "CheckFlags")
                sHP = self.HashPass(self.PassWord,
                                    self.sSalt,
                                    self.sKey)
                self.HashedPassWord = sHP
                self.fLoopDelay = .05
                self.bSendOutput = True
                return True
            elif self.bInPass is True:
                self.PassWord = self.PassWord + str(self.get_char(key))
                self.Send_Key(key)
                return True
        else:
            if key == self.Key.esc:
                self.debug(1, "esc pressed", "CheckFlags")
                self.shutdown()
                # Redundant, but Listener thread will stop if we return false
                return False
            elif self.bHotKeyP is True:
                self.bHotKeyP = False
                self.bInPass = True
                self.PassWord = ""
                return True

    def HashPass(self, sInput: str, sSalt: str, sKey: str) -> str:
        """Hash a password using 3 items irreversibly."""
        sHashPass = sSalt + sInput + sKey
        self.debug(2, "sHashPass=" + sHashPass, "HashPass")
        hashthing = self.hashlib.sha512()
        hashthing.update(bytes(sHashPass, 'utf-8'))
        hxSha512 = hashthing.hexdigest()
        self.debug(2, "hxSha512=" + str(hxSha512), "HashPass")
        hx64 = hxSha512.encode('ascii')
        base64_bytes = self.base64.b64encode(hx64)
        base64_message = base64_bytes.decode('ascii')
        sNoDupes = "".join(self.OrderedDict.fromkeys(base64_message))
        if self.iPassLen >= len(sNoDupes):
            self.iPassLen = len(sNoDupes)
        sHP = sNoDupes[0:self.iPassLen]
        # Replace some numbers with some special characters
        if self.bSpcChars is True:  # refine this later
            mydict = {51:  33, 52:  35, 53:  36, 54:  37, 61:  36}
            sAddSpcChar = sHP.translate(mydict)
            sHP = sAddSpcChar
        self.debug(2, "sHP=" + sHP, "HashPass")
        return sHP

    def Send_Key(self, key):
        """Send one key to the controller."""
        self.bPauseListener = True
        if self.bShowPass is True:
            self.myController.type(self.get_char(key))
        elif self.bShowStars is True:
            self.myController.type("*")
        self.debug(3, self.get_char(key), "Send_Key")
        self.bPauseListener = False

    def Send_HashedPassword(self, sHashedPass: str = 'NONE') -> None:
        """After backspaces send hashed string to keyboard controller."""
        self.bPauseListener = True
        self.myController.type(sHashedPass)
        self.bPauseListener = False

    def Send_backspaces(self, iCount: int) -> None:
        """Send iCount backspaces to keyboard controller."""
        self.bPauseListener = True
        for x in range(0, iCount):
            self.myController.tap(self.Key.backspace)
        self.bPauseListener = False

    def get_char(self, key):
        """Translate key to character or string."""
        try:
            # you can end up with a key.char that is NoneType
            # so plan for that and replace the displayed character
            # with an underscore
            if (key.char is None):
                return "?"
            else:
                return key.char
        except AttributeError:
            return "~"

    def on_press(self, key) -> None:
        """Process keyboard key down callback."""
        if self.bPauseListener is True:
            return True
        else:
            return self.CheckFlags(True, key)

    def on_release(self, key) -> bool:
        """Process keyboard key up callback."""
        if self.bPauseListener is True:
            return True
        else:
            return self.CheckFlags(False, key)

    def KeyListener(self, bStartStop: bool = True,
                    bSuppress: bool = False) -> None:
        """Key Listener setup and startup controls callback for keyboard.

        call: sCmd="start" or sCmd="stop" bSuppress is True of Fallse
        """
        if (bStartStop is True):
            self.lisKeys = self.Listener(
                suppress=bSuppress,
                on_release=self.on_release,
                on_press=self.on_press
                )
            self.lisKeys.daemon = True
            if self.bListening is False:  # Only start if it's not running
                self.lisKeys.start()
                self.bListening = True
                self.fLoopDelay = .05
                self.debug(3, "Listener Started", "KeyListener")
        else:
            if self.bListening is True:  # only stop if it's running
                self.lisKeys.stop()
                self.bListening = False
                self.debug(3, "Listener Stopping", "KeyListener")
                # self.fLoopDelay = self.fDefaultLoopDelay
                # I know this seems to make sense but it will delay
                # sending of keystrokes after completion.
                # it is moved to the sendoutput function instead.

    def on_activate_p(self) -> None:
        """Hot key p has been pressed set flags."""
        self.bHotKeyP = True
        self.KeyListener(self._Start_, self._Suppress_)

    def on_activate_i(self) -> None:
        """Hot key i has been pressed set flags."""
        self.shutdown()

    def HotKeyListener(self, bStartStop: bool = True) -> None:
        """Hotkey Listner setup and startup controls callback for keyboard.

        call: bStartStop is true for starting false for stopping
        """
        if (bStartStop is True):
            self.lstHotKeys = {self.sHotKeyP: self.on_activate_p,
                               self.sHotKeyI: self.on_activate_i}
            self.lisHotKey = self.GlobalHotKeys(self.lstHotKeys)
            self.lisHotKey.daemon = True
            self.lisHotKey.start()
            self.debug(1, "Listener Started", "HotKeyListener")
        else:
            self.lisHotKey.stop()
            self.debug(3, "Listener Stopped", "HotKeyListener")
            return False

    def looper(self, i: int) -> None:
        """Message loop to run as a daemon."""
        self.fLoopDelay = i
        while True:
            i = self.fLoopDelay  # allows other processes to alter the sleep
            self.mysleep(i)
            ts = str(self.mytime.time())
            self.debug(4, ts, "looper")
            if self.bStopLooper is True:
                break
                return False
            elif (self.bSendOutput is True):
                self.SendOutput()

    def shutdown(self) -> None:
        """Shutdown cleanly."""
        self.debug(1, "Shutting Down", "shutdown")
        self.KeyListener(self._Stop_)
        self.HotKeyListener(self._Stop_)
        self.debug(3, "Setting Looper Shutdown flag", "shutdown")
        self.bStopLooper = True

    def debug(self, iLevel: int = 0,
              sDebug: str = "Nothing to Say",
              sLocation: str = "Unknown"):
        """Print a string and location of the call for debugging.

        Takes debug level, the string and the name of the calling function
        """
        if iLevel <= self.iDebugLevel:
            print("\nCP: Loc=" + sLocation + " Str=" + sDebug)


if __name__ == '__main__':
    """Main portion to execute class."""
    cloak = CloakPass(myargs.key, myargs.salt,
                      myargs.passlen,
                      myargs.spcchars,
                      myargs.caps,
                      myargs.numbers,
                      myargs.showpass,
                      myargs.showstars
                      )
    cloak.main()
