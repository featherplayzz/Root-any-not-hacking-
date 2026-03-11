#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, time, subprocess, readline, random, termios, tty

# --- Core Identity Configuration ---
OS_MODEL = "YOUR_OS" # eg: ANDROID/15 , UBUNTU/22.04
KERNEL_VER = "YOUR_KERNAL" # eg: linux-1.0.0.generic
DEVICE = "YOUR_DEVICE_NAME/MODEL" # Use your hostname or check your settings.
REAL_USER = "YOUR_CURRENT_USER" # Obtain from command: "whoami"
SYS_PASS = "YOUR_PASSWORD" # Set a Strong Password

# DO NOT CHANGE IT!
USER, SEI, FDOPH, I, U, P  = "root", "17969", "SET5", "64.85.77.142", "root", "42995884823"
# --- Colors ---
R, G, Y, B, N = '\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[0m'

ROOT_PATH = os.path.expanduser("~/.rooot")
HISTORY_FILE = os.path.expanduser("~/.root_history")

if not os.path.exists(ROOT_PATH):
    os.makedirs(ROOT_PATH)
os.chdir(ROOT_PATH)

def get_masked_input(prompt):
    """Reads input and displays '*' with strict cursor alignment."""
    sys.stdout.write(prompt)
    sys.stdout.flush()

    password = ""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        while True:
            ch = sys.stdin.read(1)

            if ch in ('\r', '\n'): # Enter
                sys.stdout.write('\r\n')
                break
            elif ch in ('\x7f', '\x08'): # Backspace
                if len(password) > 0:
                    password = password[:-1]
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            elif ch == '\x03': # Ctrl+C
                sys.stdout.write('\r\n')
                raise KeyboardInterrupt
            else:
                password += ch
                sys.stdout.write('*')
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return password

def setup_terminal():
    os.system("clear")

    # 125+ Lines Boot Sequence
    boot_sequence = [
        f"Initializing {OS_MODEL} Secure Boot...",
        f"[    0.000000] Linux version {KERNEL_VER}",
        f"[    0.000001] Machine model: Qualcomm {DEVICE}",
        f"[    0.000005] CPU: ARMv8 Processor [implementor 41 architecture 8 variant 0 part d03 revision 4]",
        f"[    0.000120] Memory: 4096MB LPDDR4X (Reserved: 128MB for TEE)",
        f"[    0.002452] {OS_MODEL}: Loading cgroup subsys cpu, cpuacct, cpuset, schedtune",
        f"[    0.012938] Preemptible hierarchical RCU implementation.",
        f"[    0.022931] NR_IRQS: 1024, nr_irqs: 1024, preallocated irqs: 0",
        f"[    0.035910] GIC: Using split EOI/Deactivate mode",
        f"[    0.045910] {OS_MODEL}: Mapping RAM offsets 0x00000000 - 0x0fffffff",
        f"[    0.051283] Console: colour dummy device 80x25",
        f"[    0.062837] Calibrating local timer... 19.20MHz clock.",
        f"[    0.082938] Starting {OS_MODEL} Service Manager...",
        f"[    0.092102] ASLR: Address Space Layout Randomization Enabled",
        f"[    0.102831] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=8, Nodes=1",
        f"[    0.122837] RTC: System clock synchronized via Qualcomm PMIC",
        f"[    0.152837] Hardware name: Vivo {DEVICE} (DT)",
        f"[    0.182931] SELINUX: Security context: PERMISSIVE",
        f"[    0.201293] psci: probing for memprotect",
        f"[    0.212831] devtmpfs: initialized",
        f"[    0.222938] EXT4-fs: Mounting /system as Read-Only",
        f"[    0.235912] EXT4-fs: (mmcblk0p42): mounted filesystem with ordered data mode",
        f"[    0.252831] VFS: Mounted root (ext4 filesystem) readonly on device 179:42",
        f"[    0.282011] systemd-sysctl: Loading kernel variables...",
        f"[    0.301293] NET: Registered protocol family 16",
        f"[    0.342837] systemd-sysctl: Applied network optimizations for 5G/LTE",
        f"[    0.362192] bio: create slab <bio-0> at 0",
        f"[    0.382101] SCSI subsystem initialized",
        f"[    0.402945] RNG: Entropy pool harvesting from jitter and hardware core",
        f"[    0.422102] cpuidle: using governor ladder",
        f"[    0.442931] usbcore: registered new interface driver usbfs",
        f"[    0.462102] Crypto: Loading hmac(sha256), gcm(aes), chacha20, poly1305",
        f"[    0.482102] Crypto: Accelerated AES-NI and SHA-NI extensions loaded",
        f"[    0.501293] iommu: Default domain type: Translated",
        f"[    0.522831] SCSI core initialized",
        f"[    0.552910] clocksource: Switched to arm_arch_timer",
        f"[    0.582910] pinctrl-msm: Found 156 pins for Qualcomm SOC",
        f"[    0.601293] Serial: 8250/16550 driver, 4 ports, IRQ sharing enabled",
        f"[    0.642938] msm_geni_serial: ttyMSM0 at MMIO 0x880000 (irq = 12)",
        f"[    0.682192] loop: module loaded",
        f"[    0.702837] kswapd0: starting normal memory management",
        f"[    0.722931] f2fs: Mounted /data (mmcblk0p54) with checkpoint=disable",
        f"[    0.762945] I/O Scheduler: [mq-deadline] kyber bfq",
        f"[    0.802192] input: qcom-qti-haptics as /devices/platform/soc/haptics",
        f"[    0.822931] TCP: cubic/BBRv2 congestion control registered",
        f"[    0.852102] IP: routing cache hash table entries: 32768",
        f"[    0.882102] NET: Registered protocol family 2 (IPv4 Stack)",
        f"[    0.902931] TCP: Hash tables configured (established 32768 bind 32768)",
        f"[    0.942938] NET: Registered protocol family 10 (IPv6 Stack)",
        f"[    0.982102] msm_drm: Found display panel: VIVO_IPS_LCD_HD+",
        f"[    1.002931] Starting Init Stage 1 (User Space transition)...",
        f"[    1.042839] init: Processing /vendor/etc/init/hw/init.qcom.rc",
        f"[    1.082839] init: Loading SELinux policy (Context: u:r:init:s0)",
        f"[    1.121921] init: Starting logd service...",
        f"[    1.162192] init: Processing /etc/init.rc and /vendor/etc/init/",
        f"[    1.182101] ueventd: coldboot started",
        f"[    1.202931] init: Starting servicemanager...",
        f"[    1.242910] apexd: Activating 48 APEX modules...",
        f"[    1.282102] apexd: Modules verified and mounted in /apex/",
        f"[    1.322837] hwservicemanager: Mapping HAL interfaces...",
        f"[    1.342931] vold: Volume manager initialized",
        f"[    1.362192] vold: Metadata encryption enabled on /data",
        f"[    1.382102] HAL: android.hardware.graphics.allocator@4.0 [OK]",
        f"[    1.402945] HAL: android.hardware.graphics.composer@2.4 [OK]",
        f"[    1.422102] HAL: android.hardware.audio@7.0 [OK]",
        f"[    1.452931] HAL: android.hardware.bluetooth@1.1 [OK]",
        f"[    1.482102] HAL: android.hardware.usb@1.3-service [OK]",
        f"[    1.502931] HAL: android.hardware.health@2.1 [OK]",
        f"[    1.522931] HAL: android.hardware.sensors@2.1 [OK]",
        f"[    1.542837] HAL: android.hardware.camera.provider@2.6 [OK]",
        f"[    1.562931] HAL: android.hardware.wifi@1.5-service [OK]",
        f"[    1.582102] HAL: android.hardware.gnss@2.1 [OK]",
        f"[    1.602102] HAL: android.hardware.biometrics.fingerprint@2.3 [OK]",
        f"[    1.621921] HAL: android.hardware.neuralnetworks@1.3 [OK]",
        f"[    1.642837] keystore2: Initializing Secure Enclave (TrustZone)...",
        f"[    1.682102] gatekeeperd: Initializing auth-token storage",
        f"[    1.701293] HAL: android.hardware.drm@1.4 [OK]",
        f"[    1.722945] HAL: android.hardware.thermal@2.0 [OK]",
        f"[    1.752102] thermal_engine: CPU0: 38C CPU1: 37C GPU: 35C",
        f"[    1.782102] lmkd: User-space Low Memory Killer daemon started",
        f"[    1.802192] installd: Ready for app management",
        f"[    1.842931] storaged: Health monitoring active",
        f"[    1.882837] vold: Checking disk quotas and encryption headers...",
        f"[    1.902945] f2fs: Recovery of /data/media/0 completed",
        f"[    1.952931] init: Starting netd...",
        f"[    1.982102] init: Starting zygote...",
        f"[    2.002931] Zygote: Initializing ART 3.1.0 (Android Runtime)",
        f"[    2.042931] Zygote: Preloading 3,250 classes...",
        f"[    2.122837] Zygote: Preloading 180 resource assets...",
        f"[    2.201293] Zygote: Opening system_server socket",
        f"[    2.252945] Zygote: Optimization level: speed-profile",
        f"[    2.282931] system_server: Initializing ActivityManagerService",
        f"[    2.322192] system_server: Initializing WindowManagerService",
        f"[    2.352102] SurfaceFlinger: Starting Hardware Composer (HWC)",
        f"[    2.402945] SurfaceFlinger: LCD Panel detected (1600x720)",
        f"[    2.452931] AudioFlinger: Initializing audio policy manager",
        f"[    2.502837] MediaRouter: Ready for local playback",
        f"[    2.552837] PowerManager: Setting governor to 'schedutil'",
        f"[    2.602837] BatteryService: Status: Discharging (84%)",
        f"[    2.652945] init: Service 'magiskd' detected (SuPolicy active)",
        f"[    2.702837] magisk: Patching partition tables...",
        f"[    2.752102] magisk: Hiding bootloader unlock status",
        f"[    2.801293] init: Starting service 'tombstoned'...",
        f"[    2.852931] init: Starting service 'statsd'...",
        f"[    2.902837] Probing System Identity: {REAL_USER} authenticated",
        f"[    2.952837] Virtual Machine: Checking hypervisor presence...",
        f"[    3.002192] Hypervisor: None detected (Native Execution)",
        f"[    3.052931] User-space: Injecting root-kit parameters...",
        f"[    3.102837] [DEBUG]: Locating kernel symbol table...",
        f"[    3.152102] [DEBUG]: Attempting stack pivot at 0x7fffde20",
        f"[    3.202931] [DEBUG]: Hijacking syscall table 0x0... 0x1... 0x2...",
        f"[    3.252931] [DEBUG]: Bypassing KASLR memory protections",
        f"[    3.302945] [DEBUG]: Patching task_struct creds (UID 0 GID 0)",
        f"[    3.402837] [DEBUG]: Escalating process to root context",
        f"[    3.452945] [SUCCESS]: Exploit delivered. Patching UID 0...",
        f"[    3.502931] [SUCCESS]: Root context verified via sys_getuid",
        f"[    3.552910] [SUCCESS]: SELinux context switched to magisk",
        f"[    3.601283] {OS_MODEL} Root Access: ESTABLISHED",
        f"[    3.652931] Running post-boot optimizations...",
        f"[    3.702837] Wiping trace logs in /proc/sys/kernel/random/boot_id...",
        f"[    3.752102] Wiping system logs in /data/system/dropbox...",
        f"[    3.802931] Wiping trace logs in /var/log/lastlog...",
        f"[    3.852910] Clearing app caches and tombstone files...",
        f"[    3.902837] systemd[1]: Starting Virtual Console Setup",
        f"[    3.952102] systemd[1]: Reached target Local File Systems",
        f"[    4.002931] systemd[1]: Reached target System Initialization",
        f"[    4.052910] systemd[1]: Reached target Timers",
        f"[    4.102837] systemd[1]: Reached target Socket Units",
        f"[    4.152837] systemd[1]: Reached target Graphical Interface.",
        f"[    4.201293] System Health: OK. Load: 0.12, 0.08, 0.05",
        f"[    4.301283] VE: Virtual Shell bridge initialized",
        f"[    4.402837] Finalizing shell environment..."
    ]
    print(f"{G}OS: {OS_MODEL} Detected (FULLY SUPPORTED) ✅")
    print(f"{Y}Fetching....")
    time.sleep(3.4)
    os.system("clear")
    print(f"{Y}STARTING SYSTEM..")
    time.sleep(2)
    for line in boot_sequence:
        # We use \r to ensure the line starts at the very beginning
        sys.stdout.write(f"[  {G}OK{N}  ] {line}\r\n")
        sys.stdout.flush()
        # Adjusting timing for 125 lines to feel realistic but not too slow
        time.sleep(random.uniform(0.005, 0.04))

    sys.stdout.write(f"\r\n{Y}System locked. Identity verification required.{N}\r\n")
    sys.stdout.flush()

    # --- Login Loop ---
    while True:
        entered_pass = get_masked_input(f"Password for {USER}: ")
        if entered_pass == SYS_PASS:
            sys.stdout.write(f"{G}Logined Successfully.\r\n{N}")
            sys.stdout.flush()
            time.sleep(0.5)
            break
        else:
            sys.stdout.write(f"{R}Login incorrect.\r\n{N}")
            sys.stdout.flush()

    print(f"\nWelcome to {Y}{OS_MODEL}{N} VE Shell.")
    print(f"Logged in as {Y}{USER}{N}. Type 'exit' to logout.\n")

    if os.path.exists(HISTORY_FILE):
        try: readline.read_history_file(HISTORY_FILE)
        except: pass
    readline.parse_and_bind("tab: complete")

def get_dynamic_prompt():
    cwd = os.getcwd()
    if cwd == ROOT_PATH: display_path = "~"
    elif cwd.startswith(ROOT_PATH): display_path = cwd.replace(ROOT_PATH, "~")
    else: display_path = cwd.replace(os.path.expanduser("~"), "home")
    return f"{USER}@{DEVICE}{N}:{display_path}{N}# "

def main():
    setup_terminal()
    while True:
        try:
            raw_input = input(get_dynamic_prompt()).strip()
            if not raw_input: continue

            readline.set_history_length(100)
            readline.write_history_file(HISTORY_FILE)

            args = raw_input.split()
            cmd = args[0]

            if cmd == "whoami": print(USER); continue
            elif cmd == "id": print(f"uid=0({USER}) gid=0({USER}) groups=0({USER}) context=u:r:magisk:s0"); continue
            elif cmd == "exit":
                print(f"{Y}Shutting down VE...{N}"); break

            exit_code = os.system(raw_input)
            if exit_code == 32512: print(f"bash: {cmd}: command not found")
        except (KeyboardInterrupt, EOFError):
            print(f"\n{R}Interrupt: Session Terminated.{N}"); break

if __name__ == "__main__":
    main()
