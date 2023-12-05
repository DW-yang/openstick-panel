from flask import Flask,render_template
import os

app = Flask(__name__)
state_cmd = "mmcli -m 0|grep -w '  state'|awk '{print $3}'"
signal_cmd = "mmcli -m 0|grep signal|awk '{print $4}'"
os_name_cmd = "uname -o"
host_name_cmd = "uname -n"
kernel_cmd = "uname -r"
arch_cmd = "uname -m"
ap_status_cmd = "nmcli|grep wlan0:"
usb_status_cmd = "nmcli|grep usb0:"


def cmd(command):
    fr = os.popen(command)
    result = fr.read()
    fr.close()
    return result


@app.route('/')
def root():
    status_result = cmd(state_cmd)
    if status_result.find("connected") >= 0:
        state = "已连接"
    else:
        state = "未连接"
    signal = cmd(signal_cmd).split()[0]
    os_name = cmd(os_name_cmd).split()[0]
    host_name = cmd(host_name_cmd).split()[0]
    kernel = cmd(kernel_cmd).split()[0]
    arch = cmd(arch_cmd).split()[0]
    wifi_result = cmd(ap_status_cmd)
    if wifi_result.find("已连接") >= 0:
        wifi = "已启用"
    else:
        wifi = "已禁用"
    usb_result = cmd(usb_status_cmd)
    if usb_result.find("已连接") >= 0:
        usb = "已启用"
    else:
        usb = "已禁用"
    args = {"signal": signal,
            "state": state,
            "os_name": os_name,
            "host_name": host_name,
            "kernel": kernel,
            "arch": arch,
            "wifi": wifi,
            "usb": usb}
    return render_template("index.html", args)


def wifi_switch():
    state_result = cmd(ap_status_cmd)
    if state_result.find("已连接") >= 0:
        state = 1
    else:
        state = 0
    if state == 1:
        os.system("nmcli d disconnect wlan0")
    else:
        os.system("nmcli d connect wlan0")


def usb_switch(request):
    state_result = cmd(usb_status_cmd)
    if state_result.find("已连接") >= 0:
        state = 1
    else:
        state = 0
    if state == 1:
        os.system("nmcli d disconnect usb0")
    else:
        os.system("nmcli d connect usb0")


def reboot():
    os.system("reboot")


if __name__ == '__main__':
    app.run()
