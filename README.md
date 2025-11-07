<h2 align="center"><b>melonDS-RPC</b></h2>

<b>melonDS-RPC</b> is a simple Python script that adds Rich Presence in Discord for the <a href="https://github.com/melonDS-emu/melonDS">melonDS emulator</a>, specifically, a special version of melonDS.
<br>This script requires a modified version of the melonDS emulator, <a href="https://github.com/kid-a-mnesiac/melonDS-ROMname">melonDS-ROMname</a>.

## Why is melonDS-ROMname needed? 

melonDS-RPC fetches the window title, de-obfuscates it through a special script and displays the clean, de-obfuscated game title in your Discord RPC.
<br>Since the original version of melonDS does not showcase the current ROM emulated in its window title, it was almost impossible for the RPC script to accurately demonstrate the current game the user is playing.
<br>The .toml/.ini files that could have been possibly used for game detection are extremely unreliable – that's why I decided to modify the source code of the original melonDS to display the ROM name in the window title – it's the most reliable way of fetching the game title, as well as the fastest. 
<br>This small change allows melonDS-RPC to almost instantly change the RPC in accordance to the window title fetched.

## Requirements

- Windows 10 or newer
  
- Discord (desktop app)
  
- <a href="https://github.com/kid-a-mnesiac/melonDS-ROMname">melonDS-ROMname</a>

## Installation

The installation is as simple as downloading the latest release and running the melonDS-RPC.exe file. After that, run melonDS-ROMname. melonDS-RPC will automatically fetch the game name and display it in your Discord RPC. You don't have to have melonDS registered/detected for this to work.

## Features
### System tray

<img src="https://i.imgur.com/CABiwUS.png">

<img src="https://i.imgur.com/IVPNGoi.png">
 
 After running melonDS-RPC.exe, the program minimizes to the system tray and runs in the background – it has no GUI.
 It automatically starts with your Windows. You can turn it off, as well as just exit the application.

### RPC in Discord

Having melonDS-RPC open will automatically activate melonDS RPC in Discord <b>(this is something I'm planning on fixing)</b>, even if you don't have melonDS registered/detected as a game in Discord. Please note that <i>you do <b>not</b> have to have melonDS registered/detected in Discord for this to work</i>.
<br>While a ROM is not loaded, melonDS-RPC will show the message '<i>Waiting for melonDS</i>'.
<br>Note: <i>melonDS-RPC does not fetch data from the original melonDS – only from the modified melonDS-ROMname</i>.

<img src="https://i.imgur.com/E4Fgntg.png">

<img src="https://i.imgur.com/7zUGxxp.png">

After loading the game in the modified melonDS emulator, melonDS-RPC forwards the game name to Discord.
<br>Ejecting the ROM will change the message to '<i>Idle</i>'.

<img src="https://i.imgur.com/ByIzUtj.png">

The script tries to fetch, de-obfuscate and forward the data to Discord as fast as possible, but to be sure that the game you're playing will be visible in the RPC, please wait for about 5-10 seconds before switching between ROMs – if you do it too fast the RPC might break and won't display the game properly. 

### De-obfuscator

melonDS-RPC has a primitive de-obfuscator that cuts off unwanted parts of the filename, such as locations (<i>Europe, Japan, Au, Es, etc.</i>), certain signs, and, sadly, hyphens <b>(this is also something I want to rework)</b>.
<br>Below you can see how the example file names got de-obfuscated.

<img src="https://i.imgur.com/cgvMT88.png">

<img src="https://i.imgur.com/oBfCAeS.png">

<img src="https://i.imgur.com/r3fBazR.png">

<img src="https://i.imgur.com/Aeh7sKh.png">

<img src="https://i.imgur.com/b3BbYkZ.png">

<img src="https://i.imgur.com/FBvF9oP.png">

As you can see, it has its flaws. The de-obfuscator will definitely be reworked, the same can't yet be said about the game titles being cut off.
<br>Since the game name is fetched from the ROM file name displayed in the window title, some of them are cut off, for example, <b>Mario & Sonic at the Olympic Winter Games</b>.

<img src="https://i.imgur.com/r3fBazR.png">

<img src="https://i.imgur.com/zRuTj5V.png">

<i>This is why the game title in the RPC is cut off.</i>
<br>I will be fixing all of this. This is how things are for now.

## To-Do List

- fix melonDS-RPC turning on RPC in Discord despite no ROM being emulated
- rework de-obfuscator - remove hyphens from the list, add more keywords
- fix game titles being cut off
- MAYBE add icons

## Credits

Please support the creators of <a href="https://github.com/melonDS-emu/melonDS">melonDS emulator</a>.

<h2>⠀</h2>

<p align="center">Happy gaming to everyone!</p>

<p align="center"><img src="https://i.imgur.com/XswSLOc.gif"></p>


