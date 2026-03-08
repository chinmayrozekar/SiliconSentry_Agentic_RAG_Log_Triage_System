import os
import logging
import multiprocessing
from functools import partial
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig

# Configure basic logging for Drain3
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class LogParser:
    def __init__(self, config_file="drain3.ini"):
        config = TemplateMinerConfig()
        if config_file and os.path.exists(config_file):
            config.load(config_file)
        elif os.path.exists("drain3.ini"):
            config.load("drain3.ini")
        
        config.profiling_enabled = False
        self.template_miner = TemplateMiner(config=config)

    def process_chunk(self, file_path, start_byte, end_byte):
        """
        Worker function to process a specific byte range of a file.
        """
        local_miner = TemplateMiner(config=self.template_miner.config)
        results = {}

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            if start_byte != 0:
                f.seek(start_byte)
                # Skip the first partial line
                f.readline()
            
            while f.tell() < end_byte:
                line = f.readline()
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                result = local_miner.add_log_message(line)
                template = result.get("template_mined")
                results[template] = results.get(template, 0) + 1

        return results

    def parse_file_parallel(self, file_path):
        """
        Parallel parser that divides the file into chunks based on CPU count.
        Works across Windows, Linux, and macOS.
        """
        file_size = os.path.getsize(file_path)
        cpu_count = multiprocessing.cpu_count()
        chunk_size = file_size // cpu_count

        chunks = []
        for i in range(cpu_count):
            start = i * chunk_size
            end = file_size if i == cpu_count - 1 else (i + 1) * chunk_size
            chunks.append((start, end))

        # Use a Process Pool for true parallelism (bypassing the GIL)
        with multiprocessing.Pool(processes=cpu_count) as pool:
            worker_func = partial(self.process_chunk, file_path)
            chunk_results = pool.starmap(worker_func, chunks)

        # Merge results from all workers
        global_summary = {}
        for res in chunk_results:
            for template, count in res.items():
                global_summary[template] = global_summary.get(template, 0) + count
        
        return global_summary

    def get_summary(self):
        """Returns a summary of discovered templates from the current miner state."""
        summary = []
        for cluster in self.template_miner.drain.clusters:
            summary.append({
                "id": cluster.cluster_id,
                "template": cluster.get_template(),
                "count": cluster.size
            })
        return summary

if __name__ == "__main__":
    log_file = "data/raw_logs/system_test.log"
    if os.path.exists(log_file):
        parser = LogParser()
        print(f"--- Processing {log_file} with Parallelism ({multiprocessing.cpu_count()} cores) ---")
        summary = parser.parse_file_parallel(log_file)
        
        print(f"\nDiscovered {len(summary)} Unique Log Templates:\n")
        for i, (template, count) in enumerate(summary.items(), 1):
            print(f"ID {i} (Count: {count}): {template}")
