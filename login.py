from time import sleep
import requests

# Type your id and password here
username = ""
password = ""


class Login:
    """A class for sign in the ipgw."""
    ipgwLoginURL = "http://ipgw.neu.edu.cn/srun_portal_pc.php?ac_id=1&"
    ipgwInfoURL = "http://ipgw.neu.edu.cn/include/auth_action.php?k=23092"
    ipgwLogOutURL = "http://ipgw.neu.edu.cn/include/auth_action.php"

    def __init__(self, stuid, passwd):
        self.__stuId = stuid
        self.__password = passwd
        self.__login_data = {
            "action": "login",
            "ac_id": "1",
            "user_ip": "",
            "nas_ip": "",
            "user_mac": "",
            "url": "",
            "username": self.__stuId,
            "password": self.__password,
            "save_me": "0",
        }
        self.__info_data = {
            "action": "get_online_info",
            "key": "23092",
        }

        self.__logout_data = {
            "action": "logout",
            "username": self.__stuId,
            "password": self.__password,
            "ajax": "1",
        }

    def __str__(self):
        info_str = "A class serve to log-in"
        return info_str

    @property
    def getStuId(self):
        """Return the object's id."""
        return self.__stuId

    @property
    def getpassword(self):
        """Return the object's password."""
        return self.__password

    def getinfo(self):
        """Login,return empty dictionary when failed, return information dictionary when succeed"""
        self.logout()
        try:
            login_page = requests.post(self.ipgwLoginURL, self.__login_data)
        except:
            return {}
        else:
            if "已欠费" in login_page.text:
                return {}
        get_info = requests.post(self.ipgwInfoURL, self.__info_data)
        if "not_online" in get_info.text:
            return {}
        info_list = get_info.text.split(",")
        byte = int(info_list[0])
        time_s = int(info_list[1])
        balance = float(info_list[2])
        ip = info_list[5]
        gb = byte / (1024 * 1024 * 1024)
        hour = int(time_s / 3600)
        minute = int((time_s - hour * 3600) / 60)
        second = int(time_s - hour * 3600 - minute * 60)
        time = {
            "hour": hour,
            "minute": minute,
            "second": second,
        }
        return {
            "traffic": gb,
            "time": time,
            "balance": balance,
            "ip": ip,
        }

    def logout(self):
        """Log out from ipgw."""
        requests.post(self.ipgwLogOutURL, self.__logout_data)


if __name__ == '__main__':
    print("Logging in...")
    mine = Login(username, password)
    if mine.getinfo():
        ipgwInfo = mine.getinfo()
        print("Traffic:{0:.2f} Gb".format(ipgwInfo["traffic"]))
        print("Time: {hour}:{minute}:{second}".format(
            hour=ipgwInfo["time"]["hour"],
            minute=ipgwInfo["time"]["minute"],
            second=ipgwInfo["time"]["second"]))
        print("Balance:", ipgwInfo["balance"])
        print("IP:", ipgwInfo["ip"])
    else:
        print("Failed")
    sleep(3)
