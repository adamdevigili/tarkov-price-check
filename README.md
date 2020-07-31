# tarkov-live-flea

## Summary
Tarkov Live Flea (TLF) is a desktop application that runs alongside [Escape From Tarkov](https://www.escapefromtarkov.com/) (EFT), detects when a player has entered a "looting" interface, and will fetch the current prices of all the items visible on the in-game flea market, in real time. This will allow a player to quickly identify valuable loot, and prevent them from taking up valuable space in their inventory with items that have little value. 

## Requirements 
- Must be hyper-performant. EFT is a resource-hungry game, and any noticeable decrease in performance due to TLF is unnacceptable
- Must not require player-intervention once a player is in-game. Once running, TLF should be able to detect what state the user is in, whether they are in the menus, queuing for a riad, in a raid, in their inventory, or looting (target state). It should also be able to easily transition between these states without the user noticing. They should be able to simply look at the UI when in the looting screen, and see the prices as the items appear. 
