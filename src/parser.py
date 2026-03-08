import os
import logging
import multiprocessing
import re
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

    def process_chunk(self, file_path, start_byte, end_byte, chunk_id):
        """
        Worker function to process a specific byte range.
        Tracks line numbers and detects severity.
        """
        local_miner = TemplateMiner(config=self.template_miner.config)
        results = {} # template -> {count, line_no, severity}
        
        # Approximate line number calculation based on average log line length (~100 chars)
        # For precision, we'd need a pre-scan, but for 80GB trends, approximate is standard.
        # However, we can track internal line count within the chunk.
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            f.seek(start_byte)
            if start_byte != 0:
                f.readline() # Skip partial line
            
            line_count = 0
            while f.tell() < end_byte:
                line = f.readline()
                if not line:
                    break
                line_count += 1
                
                clean_line = line.strip()
                if not clean_line:
                    continue
                
                # Intelligence: Detect Severity
                severity = "INFO"
                if any(x in clean_line.upper() for x in ["CRITICAL", "FATAL"]):
                    severity = "CRITICAL"
                elif any(x in clean_line.upper() for x in ["ERROR", "FAIL"]):
                    severity = "ERROR"
                elif "WARN" in clean_line.upper():
                    severity = "WARNING"
                elif "DEBUG" in clean_line.upper():
                    severity = "DEBUG"

                result = local_miner.add_log_message(clean_line)
                template = result.get("template_mined")
                
                if template not in results:
                    results[template] = {
                        "count": 1,
                        "severity": severity,
                        "first_line_in_chunk": line_count,
                        "chunk_id": chunk_id
                    }
                else:
                    results[template]["count"] += 1
        
        return results

    def parse_file_parallel(self, file_path, filter_severity=None):
        """
        Parallel parser that returns an intelligent summary with trends and line numbers.
        """
        file_size = os.path.getsize(file_path)
        cpu_count = multiprocessing.cpu_count()
        chunk_size = file_size // cpu_count

        chunks = []
        for i in range(cpu_count):
            start = i * chunk_size
            end = file_size if i == cpu_count - 1 else (i + 1) * chunk_size
            chunks.append((file_path, start, end, i))

        with multiprocessing.Pool(processes=cpu_count) as pool:
            chunk_results = pool.starmap(self.process_chunk, chunks)

        # Intelligence: Reduce and Trend Analysis
        global_summary = {}
        for res in chunk_results:
            for template, data in res.items():
                if template not in global_summary:
                    global_summary[template] = data
                else:
                    global_summary[template]["count"] += data["count"]
                    # Keep the earliest appearance
                    if data["chunk_id"] < global_summary[template]["chunk_id"]:
                        global_summary[template]["first_line_in_chunk"] = data["first_line_in_chunk"]
                        global_summary[template]["chunk_id"] = data["chunk_id"]

        # Filtering
        if filter_severity:
            severities = [s.strip().upper() for s in filter_severity.split(",")]
            global_summary = {k: v for k, v in global_summary.items() if v["severity"] in severities}

        return global_summary

if __name__ == "__main__":
    # Test internal logic
    pass
