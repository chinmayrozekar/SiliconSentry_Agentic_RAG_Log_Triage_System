import os
import logging
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig

# Configure basic logging for Drain3
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class LogParser:
    def __init__(self, config_file="drain3.ini"):
        """
        Initializes the Drain3 TemplateMiner.
        :param config_file: Path to a drain3.ini file (optional).
        """
        config = TemplateMinerConfig()
        if config_file and os.path.exists(config_file):
            config.load(config_file)
        elif os.path.exists("drain3.ini"):
            config.load("drain3.ini")
        
        # Default configuration settings to isolate variables better
        config.profiling_enabled = False
        
        self.template_miner = TemplateMiner(config=config)

    def parse_file(self, file_path):
        """
        Parses a log file line by line and extracts templates.
        :param file_path: Path to the raw log file.
        :return: A list of dictionaries containing template and isolated variables.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Log file not found: {file_path}")

        results = []
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Drain3 extracts the template and the cluster it belongs to
                result = self.template_miner.add_log_message(line)
                
                # We extract the cluster details (template and parameters)
                results.append({
                    "raw": line,
                    "template": result.get("template_mined"),
                    "cluster_id": result.get("cluster_id"),
                    "change_type": result.get("change_type")
                })
        
        return results

    def get_summary(self):
        """
        Returns a summary of all discovered log templates.
        """
        summary = []
        # In newer versions of drain3, TemplateMiner wraps Drain
        # Correct way to access clusters is through the drain attribute
        for cluster in self.template_miner.drain.clusters:
            summary.append({
                "id": cluster.cluster_id,
                "template": cluster.get_template(),
                "count": cluster.size
            })
        return summary

if __name__ == "__main__":
    # Test the parser with our generated dummy log
    log_file = "data/raw_logs/system_test.log"
    
    if os.path.exists(log_file):
        print(f"--- Parsing {log_file} ---")
        parser = LogParser()
        parser.parse_file(log_file)
        
        summary = parser.get_summary()
        print(f"\nDiscovered {len(summary)} Unique Log Templates:\n")
        for s in summary:
            print(f"ID {s['id']} (Count: {s['count']}): {s['template']}")
    else:
        print(f"Log file {log_file} not found. Please run dummy_log_generator_file.py first.")
