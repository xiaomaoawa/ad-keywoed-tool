from run import generate_activation_code
machine_code = "AWAITING_ID"  # 如：A1B2C3D4E5F67890
activation_code = generate_activation_code(machine_code)
print(f"激活码: {activation_code}")
