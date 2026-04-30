import hashlib
machine_code = "用户的机器码"
secret_key = "AIJIA_ADVERTISING_2024"
activation_code = hashlib.sha256(f"{machine_code}{secret_key}".encode()).hexdigest().upper()[:24]
