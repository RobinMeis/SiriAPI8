SiriAPI8
========
SiriAPI8 opens Siri for your own purposes. You can use it to redirect any Siri command to any computer (Windows, Linux and Mac OS) without a Jailbreak. This is the only API that works with iOS8. In opposite to previous implementations you don't even need to be in your homes network! When your server is running, you can use SiriAPI8.
I use SiriAPI8 for my home automation system to control the lights. Since I also developed the original SiriAPI (https://github.com/HcDevel/Siri-API) which was compatible with iOS 7, I have a lot of experience in this matter and the basic algorithms were already tested by a big community. The use and installation of SiriAPI8 became much easier. You are not forced to use a Linux computer as a server anymore since Squid proxy is no longer required. Any operating system which is able to run the Python 3 interpreter will support this tool.

How does it work?
=================
Basically you just create notes with a defineable keyword. By default you say "Create a note iPhone ...". In this case iPhone is the keyword. SiriAPI8 which runs on your own computer and doesn't send any information to other servers than Apple's your data keeps safe, scans your iCloud notes for this keyword. When the keyword is found, anything what you said after the keyword can be checked for predefined sentences and trigger your own Python scripts. The easy to use API helps you to concentrate on your plans and not the software. Also wildcards are supported.
When you haven't blocked Siri access from the lock screen you can also use "Hey Siri" without unlocking your phone! In the original SiriAPI you always had to unlock your phone.
You can watch a demo video on YouTube (TODO: Add link). I tested and developed SiriAPI8 on an iPhone 5s with iOS8 but it should be compatible with any other iPhone which supports Siri. Users of iOS <=7 will have the choice between SiriAPI8 and the original implementation.

Installation
============
The installation instructions can be found in the wiki. In comparision to the original SiriAPI they decreased to a few commands. If you have any problem or found bugs, please report them in the Issue tracker.
