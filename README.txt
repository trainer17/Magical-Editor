		**Magical-Editor**
Save-state editor for the NDS game Magical Starsign.

Currently supports the following features:

-Choose the gender of the main character

-Enable having both protagonists (Male & Female)in your party (!)

-Unlock all Egg Characters (from Amigo mode)

-Unlock all Amigo content (Equipment sets, recovery items, figurines, key items)

-Change character starsigns to any element

-Set character 6th spell to any spell (including debugging spells)

-Change character names

-Change character level & stats

-Unlock all Bestiary, Diary & Enciclopedia entries (including Amigo Dungeon ones)

-Unlock all characters from the beginning of the story

---------------------------------------------------------------

Some cool things you can do with this:

-Begin a new adventure with both protagonists

-Have an All-Earth or All-Wood team to go against Macadameus

-Rebalance stats (eg: incresing Mokka defense stats, and decreasing his MP). Super fast Chai, Super Physically-strong Pico & Mokka, Super-Slow eggs are some ideas.

-Unlock Fondue/Kir (Fire egg) early on so as to see all his special dialogs as you progress through the story

----------------------------------------------------------------

How to use:

You will need to have Python 3 installed on your computer in order to run the program. If you do not have Python, install it from the main page, and when prompted, check the "install pip" option.

1- Open cmd on current folder (e.g. "Powershell" on Windows) and run  "python ./saveEditor.py"
   If an error shows up, try installing the following dependencies through the cmd
   pip install image
   pip install tkinter
   pip install enum	

2- Click on "Open save file" and choose your ".sav" file. 
   If you are using a flashcart, this will be in the "SAVE/" folder on the root of your microSD. 
   If you are using an emulator, such as DeSmuME, you can go to "File->Export Backup Memory".
3- Modify any stats you want
4- Click on "Export Save" 
5- Backup old save and replace with new one. If you are using an emulator such as MelonDS or DeSmuMe, you will need to select the "Import savefile" / "Import Backup Memory" from the menu.
6- Enjoy!

---------------------------------------------------------------
On choosing protagonist's names:

-When choosing to play both with Male and Female protagonists in your team, you will need to run another tool included here in order to set the "new" protagonist's name 
	 Simply run "python ./romEditor.py" in cmd, open the ROM (.nds) file you are using, choose the other character's name and click on "Patch ROM". 
	 This Should support both USA and EUR ROMs, but let me know if this isn't the case.


----------------------------------------------------------------

On functionality:

-When adding the second protagonist to your team, you will need to warp to a new location first to settle things into place (any Pizza Warp point will do).
Same rule applies when unlocking all characters.
After that, character slots 1 & 2 will have both Male and Female protagonists, and Lassi will be waiting at Neumann. You can have Lassi go back into your team if you talk to her, but you won't be able to remove either of the main protagonists unless you use this tool again.

-Starsign changes will affect a character's element and field spell, so he will be affected by planet alignment and enemies' spells, but it won't change the 5 basic spells. Spells have their own element, so you can have, say, Pico as a water starsign while still retaining all his fire spells.

-Stats affect only base stats - these will be modified further by equipment.

- Available spells are determined by the level of your character. Refer to the new wiki (https://kovopedia.com/wiki/Main_Page) to see at what level each spell unlocks. Levels don't influence stats in any way afaik.

-When unlocking egg characters, they will appear first at Neumann

-When unlocking both main characters and male/female, you will need to *first* unlock main characters, and *then* select "both" genders.

-Changing character portraits introduces bugs when swapping characters and egg characters. Use with caution.

Be careful when unlocking main characters or when changing their starsigns. If not, dependig on where on the story you are, you may lock yourself out of progression.

---------------------------------------------------------------

Concerning Spells:

-Spells #1-40 are the normal spells you encounter in the game

-Spell #41 is a backfiring spell (which sometimes happens when using Egg characters)

-Spells #42-44 are the "Planet Alignment" spells (what happens when you align all five planets)
  #42 attacks enemies (you align them)
  #43 attacks your team (enemies align them)
  #44 attacks everyone (they align by themselves)

-Spells #45 onward are enemy spells - therefore, they will attack your own team when used, as if an enemy had casted them.
 Note however that some spells, like #49, do inflict damage on enemies instead of your team. I haven't tried them all yet so there could be other rare effects with some spells

-Spell #87: Cures enemies
-Spell #90: Damages enemies + gives stats raise

-------------------
Concerning Regions:

I haven't tested this with japanese save-states, but i assume they won't work. 
I have mainly tested with EUR copies of the game. 
Should work with USA copies.

-------------------
Useful AR Codes (for EUR Version):

-No random encounters: 

-Planets always in "aura boost" zone: 

-------------------

Contact & feedback:

For anything that doesn't go as expected, or any cool feature you would like to see, write me an e-mail to romanimanga@gmail.com and I'll try to address the issue as soon as I can.

-------------------

Comunnity links:


Wiki: https://kovopedia.com/wiki/Main_Page 
      https://magicalvacation.fandom.com/wiki/Magical_Vacation_Wiki  
      https://magicalstarsign.fandom.com/wiki/Magical_Starsign_Wiki

Reddit: https://www.reddit.com/r/magicalstarsign/
Gamefaqs: https://gamefaqs.gamespot.com/ds/925593-magical-starsign
Discord: ...