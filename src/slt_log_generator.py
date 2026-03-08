import os
import random
import time
from datetime import datetime

def generate_slt_line():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    cores = [f"CORE_{i}" for i in range(16)] + [f"GPU_CORE_{i}" for i in range(8)]
    peripherals = ["USB_3.1", "PCIE_GEN4", "PCIE_GEN5", "NVME_CTRL", "DDR5_CH_A", "DDR5_CH_B", "THM_SENS_0", "GPIO_EXP"]
    
    category = random.choices(["COMPUTE", "PERIPHERAL", "THERMAL", "SYSTEM"], weights=[50, 30, 10, 10])[0]
    severity = random.choices(["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"], weights=[60, 25, 10, 4, 1])[0]
    
    if category == "COMPUTE":
        core = random.choice(cores)
        load = random.randint(80, 100)
        ops = random.randint(1000000, 9000000)
        templates = [
            f"[{timestamp}] {severity} [{core}] Stress test active: {ops} ops/s, Load: {load}%",
            f"[{timestamp}] {severity} [{core}] Floating point benchmark iteration {random.randint(1, 1000)} completed",
            f"[{timestamp}] {severity} [{core}] Cache coherency check: Status {random.choice(['SYNC', 'LOCKED', 'DIRTY'])}",
            f"[{timestamp}] {severity} [{core}] Unexpected IRQ signal detected on vector 0x{random.randint(0, 0xFF):02X}"
        ]
    elif category == "PERIPHERAL":
        peri = random.choice(peripherals)
        templates = [
            f"[{timestamp}] {severity} [{peri}] Link negotiation started: Target Speed {random.choice(['5GT/s', '16GT/s', '32GT/s'])}",
            f"[{timestamp}] {severity} [{peri}] Enumeration successful: ID {random.randint(1000, 9999)}:0x{random.randint(0, 0xFFFF):04X}",
            f"[{timestamp}] {severity} [{peri}] Data integrity failure: CRC mismatch at block 0x{random.randint(0, 0xFFFFFFFF):08X}",
            f"[{timestamp}] {severity} [{peri}] Throughput verified: {random.uniform(1.0, 20.0):.2f} GB/s",
            f"[{timestamp}] {severity} [{peri}] Device disconnected: Unresponsive after {random.randint(10, 100)}ms"
        ]
    elif category == "THERMAL":
        sens = random.choice([p for p in peripherals if "THM" in p] or ["THM_SENS_DEFAULT"])
        temp = random.randint(40, 105)
        templates = [
            f"[{timestamp}] {severity} [{sens}] Current junction temperature: {temp}C",
            f"[{timestamp}] {severity} [{sens}] Thermal throttling engaged: Limit set to {random.randint(50, 70)}%",
            f"[{timestamp}] {severity} [{sens}] Critical temperature threshold exceeded: Shutting down non-essential rails"
        ]
    else: # SYSTEM
        templates = [
            f"[{timestamp}] {severity} [SYS] Power rail {random.choice(['VDD_CORE', 'VDD_SOC', 'VDD_MEM'])} stable at {random.uniform(0.7, 1.2):.3f}V",
            f"[{timestamp}] {severity} [SYS] Heartbeat signal received from BMC",
            f"[{timestamp}] {severity} [SYS] Boot sequence state changed to: {random.choice(['KERNEL_INIT', 'BENCH_START', 'POST_DONE'])}",
            f"[{timestamp}] {severity} [SYS] Memory scrub detected single-bit ECC error at 0x{random.randint(0, 0xFFFFFFFF):08X}"
        ]
        
    return random.choice(templates) + "\n"

def create_slt_logs(file_path, target_size_mb):
    target_bytes = int(target_size_mb * 1024 * 1024)
    print(f"Generating high-fidelity SLT benchmark log: {file_path}. Target: {target_size_mb} MB.")
    start_time = time.time()

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    bytes_written = 0
    
    with open(file_path, 'w') as f:
        # SLT Header
        f.write("================================================================================\n")
        f.write("SYSTEM LEVEL TEST (SLT) BENCHMARK SUITE v4.2\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"DUT ID: DUT_{random.randint(10000, 99999)}\n")
        f.write("Configuration: 16-Core CPU, 8-Core GPU, 64GB DDR5, PCIe Gen5 Enabled\n")
        f.write("================================================================================\n\n")
        
        while bytes_written < target_bytes:
            chunk = [generate_slt_line() for _ in range(5000)]
            chunk_str = "".join(chunk)
            f.write(chunk_str)
            bytes_written += len(chunk_str.encode('utf-8'))
            
        f.write("\n================================================================================\n")
        f.write("SLT TEST SEQUENCE COMPLETED\n")
        f.write(f"Total Errors: {random.randint(5, 50)}\n")
        f.write(f"Total Warnings: {random.randint(50, 200)}\n")
        f.write("Final Result: FAIL (Check logs for peripheral CRC mismatches)\n")
        f.write("================================================================================\n")

    end_time = time.time()
    print(f"Generation complete. Took {round(end_time - start_time, 2)} seconds. File: {file_path}")

if __name__ == "__main__":
    create_slt_logs("data/raw_logs/slt_benchmark_100mb.log", 100)
