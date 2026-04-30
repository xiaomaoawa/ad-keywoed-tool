import sys
import json
import secrets
import hashlib
import time
from pathlib import Path
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

# ===================== 本地独立版配置（无需修改） =====================
CONFIG = {
    "data_file": "local_license_data.json",
    "device_id": "MY_LOCAL_PC_" + hashlib.md5(str(Path.home()).encode()).hexdigest()[:8]
}

# ===================== 本地卡密系统核心 =====================
class LocalLicenseSystem:
    def __init__(self):
        self.data_file = Path(CONFIG["data_file"])
        self.data = self.load_data()

    def load_data(self):
        if not self.data_file.exists():
            default = {
                "licenses": {},
                "devices": {},
                "generated": {}
            }
            self.save_data(default)
            return default
        try:
            return json.load(open(self.data_file, "r", encoding="utf-8"))
        except:
            return {"licenses": {}, "devices": {}, "generated": {}}

    def save_data(self, data=None):
        if data is None:
            data = self.data
        json.dump(data, open(self.data_file, "w", encoding="utf-8"), indent=2)

    # 生成卡密（时长小时、可使用次数、设备限制）
    def generate_license(self, hours=24, use_limit=1, device_limit=1):
        license_key = "LIC-" + secrets.token_hex(12).upper()
        self.data["generated"][license_key] = {
            "hours": hours,
            "use_limit": use_limit,
            "device_limit": device_limit,
            "created_at": time.time()
        }
        self.save_data()
        return license_key

    # 激活卡密
    def activate_license(self, key):
        key = key.strip().upper()
        gen = self.data["generated"]
        if key not in gen:
            return {"success": False, "error": "卡密不存在"}

        lic = gen[key]
        devices = self.data["devices"]
        used_devices = len(devices.get(key, []))

        if used_devices >= lic["use_limit"]:
            return {"success": False, "error": "使用次数已用完"}

        device = CONFIG["device_id"]
        if key not in devices:
            devices[key] = []
        if device not in devices[key]:
            if len(devices[key]) >= lic["device_limit"]:
                return {"success": False, "error": "设备数量超限"}
            devices[key].append(device)

        activate_time = time.time()
        expire_time = activate_time + lic["hours"] * 3600

        self.data["licenses"][key] = {
            "activated": True,
            "activate_time": activate_time,
            "expire_time": expire_time,
            "device": device
        }
        self.save_data()
        return {
            "success": True,
            "expire_hours": lic["hours"],
            "expire_at": time.ctime(expire_time),
            "device_limit": lic["device_limit"],
            "use_limit": lic["use_limit"]
        }

    # 验证卡密状态
    def check_license(self, key):
        key = key.strip().upper()
        if key not in self.data["licenses"]:
            if key in self.data["generated"]:
                return {"status": "unused", "msg": "未激活"}
            return {"status": "not_found", "msg": "不存在"}

        lic = self.data["licenses"][key]
        now = time.time()
        if now > lic["expire_time"]:
            return {"status": "expired", "msg": "已过期", "expire_at": time.ctime(lic["expire_time"])}
        return {
            "status": "activated",
            "msg": "已激活",
            "expire_at": time.ctime(lic["expire_time"]),
            "remaining": int((lic["expire_time"] - now) / 3600),
            "device": lic["device"]
        }

# ===================== 桌面UI界面 =====================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("独立版卡密授权系统")
        self.setFixedSize(520, 500)
        self.lic = LocalLicenseSystem()
        self.init_ui()

    def init_ui(self):
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)

        # 标题
        title = QLabel("✅ 本地独立运行 | 无第三方依赖")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 卡密输入
        layout.addWidget(QLabel("卡密："))
        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText("输入卡密，例如：LIC-XXXXXX")
        layout.addWidget(self.license_input)

        # 按钮
        self.btn_activate = QPushButton("激活卡密")
        self.btn_check = QPushButton("查询卡密状态")
        self.btn_generate = QPushButton("生成测试卡密（24小时1次1设备）")
        layout.addWidget(self.btn_activate)
        layout.addWidget(self.btn_check)
        layout.addWidget(self.btn_generate)

        # 日志框
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        layout.addWidget(self.log_box)

        # 绑定事件
        self.btn_activate.clicked.connect(self.do_activate)
        self.btn_check.clicked.connect(self.do_check)
        self.btn_generate.clicked.connect(self.do_generate)

    def log(self, msg):
        self.log_box.append(f"[{time.strftime('%H:%M:%S')}] {msg}")

    def do_generate(self):
        key = self.lic.generate_license(hours=24, use_limit=1, device_limit=1)
        self.log(f"✅ 生成卡密：{key}")

    def do_activate(self):
        key = self.license_input.text().strip()
        if not key:
            QMessageBox.warning(self, "提示", "请输入卡密")
            return
        self.log(f"🔹 正在激活：{key}")
        res = self.lic.activate_license(key)
        self.log(json.dumps(res, ensure_ascii=False, indent=2))

    def do_check(self):
        key = self.license_input.text().strip()
        if not key:
            QMessageBox.warning(self, "提示", "请输入卡密")
            return
        self.log(f"🔍 正在查询：{key}")
        res = self.lic.check_license(key)
        self.log(json.dumps(res, ensure_ascii=False, indent=2))

# ===================== 启动 =====================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())