import os
import random
import time

def create_dummy_logs(file_name, target_size_gb):
    target_bytes = int(target_size_gb * 1024 * 1024 * 1024)
    print(f"Starting generation of {file_name}. Target size: {target_size_gb} GB.")
    start_time = time.time()

    bytes_written = 0
    
    with open(file_name, 'w') as f:
        while bytes_written < target_bytes:
            chunk = []
            # Generate 10,000 lines at a time to keep it fast
            for _ in range(10000):
                line = f"[{random.randint(1000, 9999)}] INFO: Dummy log entry simulated...\n"
                chunk.append(line)
            
            # Join the chunk and write to disk
            chunk_str = "".join(chunk)
            f.write(chunk_str)
            
            # Track bytes written in memory, not via disk checks
            bytes_written += len(chunk_str.encode('utf-8'))
            
    end_time = time.time()
    print(f"Generation complete. Took {round(end_time - start_time, 2)} seconds.")

# This is the execution block that was missing
if __name__ == "__main__":
    # Test with 0.1 GB (100MB) first to prove it works before locking up your disk
    create_dummy_logs("test_dump.log", 10)