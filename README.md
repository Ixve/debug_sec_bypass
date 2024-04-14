# debug_sec_bypass

This script is **root only**, users who have not rooted their phones **cannot** use this script. The script has been so far only tested on a Xiaomi Redmi 12C, please open an issue if you're facing any problems regarding device compatibility or any other errors.

The script works in a very simple manner, it'll check for root and then force `persist.security.adbinstall` and `persist.security.adbinput` to `1` using `setprop`.<br><br><br> After that it'll pull `remote_provider_preferences.xml` from the phone (found in `/data/data/com.miui.securitycenter/shared_prefs/`) and modify it to add 2 flags:<br><br> `<boolean name="security_adb_install_enable" value="true" />`<br>AND<br> `<boolean name="security_adb_input_enable" value="true" />`<br><br>And will then put it back onto the phone and reboot it.

# issues
If root_check fails and gives you an error message, download and run the text file from the repository and follow it step by step.
