import os

def menu():
    os.system("cls;clear")
    print("""
    +======================================+
    USB Debugging (Security Settings) Bypass

    [1] Bypass
    [0] Exit
    """)

    try:
        global ch
        ch = int(input("[Choice 1,0] >> "))
    except KeyboardInterrupt:
        print("[!] CTRL^C Detected")
        cleanup()
    except:
        print("[!] Invalid Choice...")
        menu()
def rootcheck():
    os.system("cls;clear")
    global flag
    if flag == 0:
        print("[>] Please connect your phone and give ADB authorizaton/superuser privileges")
        tmpstr = input("\n[>] Press any key to continue...")
    print("[#] Checking for root")
    os.system("""adb shell "su -c 'echo wereroot_1928 > /sdcard/root_check'" 1>std.tmp 2>&1""")
    with open("std.tmp", "r", encoding="utf-8") as f:
        fr = f.read()
        if "no devices" in fr:
            flag = 1
            print("[!] ADB => No device connected!")
            print("[!] Please connect your device and press any key to continue")
            tmpstr = input("\n...")
            rootcheck()
        elif "device offline" in fr:
            flag = 1
            print("[!] ADB => Device offline!")
            print("[!] Please make sure root/USB debugging is set up properly, reboot and re-connect your phone")
            tmpstr = input("\nPress any key to continue...")
            rootcheck()
        elif "Permission denied" in fr:
            flag = 1
            print("[!] WARNING => Root permissions were denied")
            print("[!] Please make sure '[SharedUID] Shell' has root privileges")
            tmpstr = input("\nPress any key to continue...")
            rootcheck()
        else:
            flag = 1
            print("[#] Pulling root_check file")
            os.system("adb pull /sdcard/root_check 1>nul2>nul")
            with open("root_check") as x:
                xr = x.read()
                if "wereroot_1928" in xr:
                    print("[#] Root check passed, cleaning up...")
            x.close()
            os.remove("root_check")
            return 1
            

def cleanup():
    os.system("cls;clear")
    print("[>] Cleaning up")
    try:
        os.remove("std.tmp")
        os.remove("remote_provider_preferences.xml")
        os.remove("root_check")
    except:
        pass
    print("[>] Exitting")
    exit()  
            

global flag
flag = 0
menu()
if ch == int(1):
    if rootcheck() == 1:
        os.system("cls;clear")
        print("[@] Bypassing...")
        print("[@] SetProp => ADBInstall 1")
        os.system("""adb shell "su -c 'setprop persist.security.adbinstall 1'" 1>std.tmp 2>&1""")
        print("[@] SetProp => ADBInput 1")
        os.system("""adb shell "su -c 'setprop persist.security.adbinput 1'" 1>std.tmp 2>&1""")
        print("[@] Cloning Remote_Provider_Preferences.xml")
        os.system("""adb shell "su -c 'cp /data/data/com.miui.securitycenter/shared_prefs/remote_provider_preferences.xml /sdcard/'" 1>std.tmp 2>&1""")
        print("[@] Pulling Remote_Provider_Preferences.xml")
        os.system("adb pull /sdcard/remote_provider_preferences.xml 1>std.tmp 2>&1")
        print("[@] Modifying file...")
        with open("remote_provider_preferences.xml", "r", encoding="latin-1") as buf_in:
            buf = buf_in.readlines()
            buf_in.close()
        with open("remote_provider_preferences.xml", "w", encoding="utf-8") as buf_out:
            for line in buf:
                if line == "</map>\n":
                    line = line + """<boolean name="security_adb_install_enable" value="true" />\n<boolean name="security_adb_input_enable" value="true" />\n"""
                buf_out.write(line)
            buf_out.close()
        print("[@] Removing file on smartphone (precaution)...")
        os.system("adb shell 'rm /sdcard/remote_provider_preferences.xml' 1>std.tmp 2>&1")
        print("[@] Pushing file onto device")
        os.system("adb push remote_provider_preferences.xml /sdcard/ 1>std.tmp 2>&1")
        print("[@] Moving file on device to shared_prefs")
        os.system("""adb shell "su -c 'rm /data/data/com.miui.securitycenter/shared_prefs/remote_provider_preferences.xml && mv /sdcard/remote_provider_preferences.xml /data/data/com.miui.securitycenter/shared_prefs/'" 1>std.tmp 2>&1""")
        print("[@] Rebooting device")
        os.system("adb reboot")
        print("[@] Bypass complete, press any key to clean up and exit.")
        stdtmp = input("...")
        cleanup()
    else:
        os.system("cls;clear")
        print("[!] Root check failure, device appears to be detected, is not offline and has proper permissions\n[!] However the check has failed.\n[!] Please run the commands manually.")
            
            
elif ch == int(0):
    cleanup()
else:
    print("[!] Invalid Choice...")
    menu()
