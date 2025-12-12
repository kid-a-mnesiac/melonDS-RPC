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

Having melonDS-RPC running and stored in tray will automatically activate melonDS RPC in Discord whenever your <a href="https://github.com/kid-a-mnesiac/melonDS-ROMname">modified version of melonDS</a> is running. Please note that <i>you do <b>not</b> have to have melonDS registered/detected in Discord for this to work</i>.
<br>While a ROM is not loaded, melonDS-RPC in the tray will show the message '<i>Waiting for melonDS</i>'.
<br>Note: <i>melonDS-RPC does not fetch data from the original melonDS – only from the modified melonDS-ROMname</i>.

<img src="https://i.imgur.com/C1W30RW.png">

After loading the game in the modified melonDS emulator, melonDS-RPC forwards the game name to Discord.
<br>Ejecting the ROM will change the message to '<i>No ROM loaded</i>'.

<img src="https://i.imgur.com/DyZ9g7M.png">

<img src="https://i.imgur.com/GaUeq2L.png">
<i>Ejected ROM.</i>

<br>Closing melonDS emulator will make the Discord RPC disappear.

### De-obfuscator

<br>melonDS-RPC's de-obfuscator has been reworked. It cuts off unwanted parts of the filename, such as locations (<i>Europe, Japan, Au, Es, etc.</i>), certain signs, etc., more efficiently now.
<br>Below you can see how the example file names got de-obfuscated. I've chosen more conmplex ones to showcase the abilities of the de-obfuscator.

<img src="https://i.imgur.com/YMHoNli.png">

<img src="https://i.imgur.com/TkRTHyL.png">

<img src="https://i.imgur.com/7X8kKEs.png">

<img src="https://i.imgur.com/QvlZ3ij.png">

<img src="https://i.imgur.com/6wzSR8i.png">

<img src="https://i.imgur.com/ioEvxxZ.png">

<img src="https://i.imgur.com/Wsfwz9S.png">

<img src="https://i.imgur.com/YDUb841.png">

## To-Do List & Changelog
### To-Do List
- <s>fix melonDS-RPC turning on RPC in Discord despite no ROM being emulated</s> [FIXED]
- <s>rework de-obfuscator - remove hyphens from the list, add more keywords</s> [FIXED]
- <s>fix game titles being cut off</s> [FIXED]
- MAYBE add icons

### Changelog
12.12.2025
- melonDS-ROMname 1.1 support
- No longer shows RPC in Discord when no melonDS-ROMname is launched.
- The de-obfuscator can handle most of the file names now.
- <a href="https://github.com/kid-a-mnesiac/melonDS-ROMname">melonDS-ROMname</a> doesn't cut off game titles anymore.
- Clicking on GUI buttons doesn't throw off the RPC.

## Credits

Please support the creators of <a href="https://github.com/melonDS-emu/melonDS">melonDS emulator</a>.

<h2>⠀</h2>

<p align="center">Happy gaming to everyone!</p>

<p align="center"><img src="https://i.imgur.com/XswSLOc.gif"></p>


