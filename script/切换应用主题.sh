query=$1
appId=$(osascript -e "id of app \"$query\"")
current=$(defaults read $appId NSRequiresAquaSystemAppearance)

if [ "$current" = 1 ] ; then
  mode='No'
  ret="Switch $query to Dark Mode"
else
  ret="Switch $query to Light Mode"
  mode='Yes'
fi

defaults write $appId NSRequiresAquaSystemAppearance -bool $mode
echo $ret
