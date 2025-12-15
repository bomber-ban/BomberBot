#!/bin/bash
rm -rf AppDir

mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/{256x256,512x512}/apps

cp nuitka/BomberBot AppDir/usr/bin/BomberBot
chmod +x AppDir/usr/bin/BomberBot


for size in 256 512; do
        convert bomberbot_icon.png \
            -resize ${size}x${size} \
            -background transparent \
            -gravity center \
            -extent ${size}x${size} \
            -unsharp 0.5x0.5+0.5+0.008 \
            -quality 99 \
            "AppDir/usr/share/icons/hicolor/${size}x${size}/apps/bomberbot.png"
    done

cp AppDir/usr/share/icons/hicolor/256x256/apps/bomberbot.png AppDir/.DirIcon
cp AppDir/usr/share/icons/hicolor/512x512/apps/bomberbot.png AppDir/bomberbot.png

APP_NAME="bomberbot"
DESKTOP_FILE_NAME="${APP_NAME}.desktop"

cat > "AppDir/${DESKTOP_FILE_NAME}" << DESKTOP_LOCAL
[Desktop Entry]
Name=BomberBot
Comment=Stress testing telecommunications systems
TryExec=AppRun
Exec=AppRun
Icon=${APP_NAME}
Terminal=false
StartupWMClass=BomberBot
Type=Application
Categories=Network
Keywords=Bot;Bomber;bot;bomber;
SingleMainWindow=true
X-GNOME-UsesNotifications=true
X-GNOME-SingleWindow=true
DESKTOP_LOCAL


cat > AppDir/AppRun << 'EOF'
#!/bin/bash

set -e

case "${1:-}" in
    "--uninstall")
        rm -f ~/.local/bin/BomberBot 2>/dev/null
        rm -f "$HOME/.local/share/applications/bomberbot.desktop" 2>/dev/null
        find ~/.local/share/icons -name "*bomberbot*" -delete 2>/dev/null
        rm -f "$HOME/Desktop/bomberbot.desktop" 2>/dev/null
        rm -f "$HOME/Рабочий стол/bomberbot.desktop" 2>/dev/null
        rm -f "$HOME/.local/share/icons/hicolor/"*"/apps/bomberbot.*" 2>/dev/null

        echo "BomberBot successfully uninstall from your computer."
        command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database ~/.local/share/applications >/dev/null 2>&1
        command -v gtk-update-icon-cache >/dev/null 2>&1 && gtk-update-icon-cache ~/.local/share/icons/hicolor >/dev/null 2>&1
        exit 0
        ;;
    "--help")
        echo "Usage:"
        echo "  Double-click AppImage                # Run and auto-install"
        echo "  ./BomberBot.AppImage --uninstall     # Remove installation"
        exit 0
        ;;
esac

SELF="$(readlink -f "$0")"
HERE="${SELF%/*}"
APP_NAME="bomberbot"
DESKTOP_FILE_NAME="${APP_NAME}.desktop"
APPIMAGE="${APPIMAGE:-$SELF}"

export APPIMAGE="$SELF"
export APPDIR="$HERE"
export PATH="$HERE/usr/bin:$PATH"
export LD_LIBRARY_PATH="$HERE/usr/lib:$LD_LIBRARY_PATH"

export RESOURCE_NAME="BomberBot"

mkdir -p "$HOME/.local/bin/"
mkdir -p "$HOME/.local/share/"
mkdir -p "$HOME/.local/share/icons"
mkdir -p "$HOME/.local/share/icons/hicolor/256x256"
mkdir -p "$HOME/.local/share/icons/hicolor/512x512"
mkdir -p "$HOME/.local/share/icons/hicolor/256x256/apps"
mkdir -p "$HOME/.local/share/icons/hicolor/512x512/apps"

create_desktop_integration() {
    mkdir -p "$HOME/.local/share/applications"
    cp -f $APPDIR/usr/bin/BomberBot $HOME/.local/bin/BomberBot

    for size_dir in "$HERE/usr/share/icons/hicolor/"*; do
        if [ -d "$size_dir/apps" ] && [ -f "$size_dir/apps/bomberbot.png" ]; then
            size=$(basename "$size_dir")
            mkdir -p "$HOME/.local/share/icons/hicolor/$size/apps"
            cp "$size_dir/apps/bomberbot.png" "$HOME/.local/share/icons/hicolor/$size/apps/${APP_NAME}.png"
        fi
    done
    
    cat > "$HOME/.local/share/applications/${DESKTOP_FILE_NAME}" << DESKTOP
[Desktop Entry]
Name=BomberBot
Comment=Stress testing telecommunications systems
TryExec=$HOME/.local/bin/BomberBot
Exec=$HOME/.local/bin/BomberBot -- %U
Icon=${APP_NAME}
Terminal=false
StartupWMClass=BomberBot
Type=Application
Categories=Network
Keywords=Bot;Bomber;bot;bomber;
SingleMainWindow=true
X-GNOME-UsesNotifications=true
X-GNOME-SingleWindow=true
DESKTOP
    
    update_icon_cache
    update_desktop_database
    
}

update_icon_cache() {
    if command -v gtk-update-icon-cache &> /dev/null; then
        gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
    fi
}

update_desktop_database() {
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
    fi
}


if [ ! -f "$HOME/.local/share/applications/${DESKTOP_FILE_NAME}" ]; then
    create_desktop_integration
fi

cd "$HERE"
exec "./usr/bin/BomberBot" "$@"
EOF


chmod +x AppDir/AppRun

if ! command -v appimagetool &> /dev/null; then
    wget -c "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    chmod +x appimagetool-x86_64.AppImage
    APPIMAGETOOL="./appimagetool-x86_64.AppImage"
else
    APPIMAGETOOL="appimagetool"
fi
 #APPIMAGETOOL="appimagetool"

$APPIMAGETOOL AppDir dist/BomberBot.AppImage

chmod +x dist/BomberBot.AppImage

rm -rf AppDir
