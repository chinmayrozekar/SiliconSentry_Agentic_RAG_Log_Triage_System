import os
import random
import time
from datetime import datetime

def generate_netlist_header():
    return """
********************************************************************************
* SPICE Netlist Generated for PERC/DRC Verification
* Design: TOP_MACRO
* Date: 2026-03-08
********************************************************************************

.SUBCKT INV IN OUT VDD VSS
M1 OUT IN VDD VDD PMOS W=0.2u L=0.03u
M2 OUT IN VSS VSS NMOS W=0.1u L=0.03u
.ENDS

.SUBCKT NAND2 A B OUT VDD VSS
M1 OUT A VDD VDD PMOS W=0.2u L=0.03u
M2 OUT B VDD VDD PMOS W=0.2u L=0.03u
M3 OUT A NET1 VSS NMOS W=0.2u L=0.03u
M4 NET1 B VSS VSS NMOS W=0.2u L=0.03u
.ENDS

.SUBCKT TOP_MACRO
X1 IN_A OUT_INV VDD VSS INV
X2 OUT_INV IN_B FINAL_OUT VDD VSS NAND2
.ENDS
"""

def generate_perc_check(cell, rule_id, status):
    timestamp = datetime.now().strftime("%H:%M:%S")
    msg_types = {
        "PASS": "INFO",
        "FAIL": "ERROR",
        "WARN": "WARNING"
    }
    
    if status == "PASS":
        return f"[{timestamp}] {msg_types[status]} [PERC] Cell '{cell}': Rule {rule_id} check completed. Status: PASS.\n"
    else:
        coords = f"({random.uniform(0, 50):.3f}, {random.uniform(0, 50):.3f})"
        return f"[{timestamp}] {msg_types[status]} [PERC] Cell '{cell}': Rule {rule_id} violation found at {coords} on Net '{random.choice(['NET1', 'OUT', 'VDD'])}'. Status: FAIL.\n"

def generate_drc_verbose_trace(cell):
    timestamp = datetime.now().strftime("%H:%M:%S")
    layers = ["M1", "M2", "POLY", "DIFF", "VIA1", "VIA2"]
    layer = random.choice(layers)
    x, y = random.uniform(0, 100), random.uniform(0, 100)
    
    templates = [
        f"[{timestamp}] DEBUG [DRC] Cell '{cell}': Scanning {layer} geometry at ({x:.3f}, {y:.3f})...\n",
        f"[{timestamp}] DEBUG [DRC] Cell '{cell}': Connectivity verified for {layer} segment at ({x:.3f}, {y:.3f}).\n",
        f"[{timestamp}] DEBUG [DRC] Cell '{cell}': Checking spacing between {layer} objects at ({x:.3f}, {y:.3f}).\n",
        f"[{timestamp}] DEBUG [DRC] Cell '{cell}': Width check for {layer} polygon: current={random.uniform(0.02, 0.05):.4f}u, min=0.03u.\n"
    ]
    return random.choice(templates)

def create_hierarchical_perc_log(file_path, target_size_mb):
    target_bytes = int(target_size_mb * 1024 * 1024)
    print(f"Generating hierarchical PERC/DRC log: {file_path}. Target: {target_size_mb} MB.")
    start_time = time.time()

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    bytes_written = 0
    
    cells = ["INV", "NAND2", "TOP_MACRO"]
    rules = ["ESD_1", "PATH_RES_02", "GATE_DIRECT_FLOAT", "ANTENNA_M1", "LATCHUP_01"]

    with open(file_path, 'w') as f:
        # Tool Header
        f.write("################################################################################\n")
        f.write("# PERC/DRC High-Performance Verification Engine v2026.1\n")
        f.write(f"# Executed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# Mode: Hierarchical Debug (Full Trace)\n")
        f.write("################################################################################\n\n")
        
        # Netlist Phase
        f.write("[System] INFO [LOAD] Parsing netlist for hierarchical verification...\n")
        f.write(generate_netlist_header())
        f.write("\n[System] INFO [LOAD] Netlist parsing successful. 3 cells identified.\n\n")
        
        # Checking Phase (The bulk of the file)
        while bytes_written < target_bytes:
            chunk = []
            # Each chunk simulates a "Pass" or "Fail" sequence with high debug verbosity
            for _ in range(500):
                current_cell = random.choice(cells)
                # Verbose debug lines to fill size
                for _ in range(20):
                    chunk.append(generate_drc_verbose_trace(current_cell))
                
                # Intermittent Rule Results
                rule = random.choice(rules)
                # 95% pass rate to keep it realistic but with errors
                status = random.choices(["PASS", "FAIL"], weights=[95, 5])[0]
                chunk.append(generate_perc_check(current_cell, rule, status))
            
            chunk_str = "".join(chunk)
            f.write(chunk_str)
            bytes_written += len(chunk_str.encode('utf-8'))
            
        # Summary Phase
        f.write("\n\n################################################################################\n")
        f.write("# FINAL VERIFICATION SUMMARY\n")
        f.write("################################################################################\n")
        f.write("# Cell: INV .................. Status: PASS\n")
        f.write("# Cell: NAND2 ................ Status: FAIL (2 violations)\n")
        f.write("# Cell: TOP_MACRO ............ Status: FAIL (Inferred)\n")
        f.write("################################################################################\n")

    end_time = time.time()
    print(f"Generation complete. Took {round(end_time - start_time, 2)} seconds. File: {file_path}")

if __name__ == "__main__":
    create_hierarchical_perc_log("data/raw_logs/perc_drc_hierarchical.log", 60)
