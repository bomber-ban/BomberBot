#!/bin/bash

rm -f ~/.local/bin/BomberBot
rm -f ~/.local/share/applications/bomberbot.desktop
rm -f ~/Desktop/bomberbot.desktop 2>/dev/null
rm -f ~/Рабочий\ стол/bomberbot.desktop 2>/dev/null
find ~/.local/share/icons -name "*bomberbot*" -delete 2>/dev/null
rm -f BomberBot.AppImage 2>/dev/null


command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database ~/.local/share/applications >/dev/null 2>&1
command -v gtk-update-icon-cache >/dev/null 2>&1 && gtk-update-icon-cache ~/.local/share/icons/hicolor >/dev/null 2>&1

echo "BomberBot is Uninstalled."