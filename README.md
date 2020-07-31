# Tarkov Price Check

## Summary
Tarkov Price Check (TPC) is a desktop application that runs alongside [Escape From Tarkov](https://www.escapefromtarkov.com/) (EFT), using OCR to detect when a player has entered a "looting" interface, and will fetch the current prices of all the items visible on the in-game flea market (FM), in real time. This will allow a player to quickly identify valuable loot, and prevent them from taking up valuable space in their inventory with items that have little value. Since there is no public API from EFT to show current FM prices (to stop bots from buying high-value items as soon as they come up), we will use the API produced by [Tarkov Market](https://tarkov-market.com/), which uses OCR to periodically refresh it's database with relatively current prices.  

## Requirements 
- Must be hyper-performant. EFT is a resource-hungry game, and any noticeable decrease in performance due to TLF is unnacceptable
- Must not require player-intervention once a player is in-game. Once running, TLF should be able to detect what state the user is in, whether they are in the menus, queuing for a riad, in a raid, in their inventory, or looting (target state). It should also be able to easily transition between these states without the user noticing. They should be able to simply look at the UI when in the looting screen, and see the prices as the items appear. 
- Since you could potentially be looting a lot of items from a loot source, looting states should be saved as "sessions", and repeat calls to fetch a single item's price should not be made. Only when the player exits the looting session should the memory of that loot be cleared
- Since the FM prices don't fluctuate that often, a local in-memory cache can be kept for all items with a relatively long TTL, potentially the length of an entire raid (30-50 minutes). 
