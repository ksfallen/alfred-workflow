-- chrome书签同步到 safari
-- close google chrome to perform importing 
-- do shell script "killall \"Google Chrome\" || echo \"Google Chrome is not running.\""

tell application "Safari" to activate

tell application "System Events" to set visible of application process "Safari" to false

log "Syncing"

tell application "System Events"
	tell application process "Safari"
    	tell menu "导入自" of menu item "导入自" of menu "文件" of menu bar item "文件" of menu bar 1
			click menu item "Google Chrome.app…"
		end tell
		tell sheet 1 of window "起始页"
			click button "导入"
		end tell
		delay 2
		tell sheet 1 of window "起始页"
			click button "好"
		end tell
    end tell
end tell

log "All done"

-- restore chrome closed tabs and minimize window in background
delay 0.5
log "Opening chrome in background"