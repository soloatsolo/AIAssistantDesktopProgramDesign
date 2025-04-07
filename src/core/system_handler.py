import psutil
import platform
import subprocess
import os
from typing import Dict, List, Optional

class SystemHandler:
    @staticmethod
    def get_system_info() -> Dict[str, str]:
        """Get basic system information"""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "cpu": platform.processor(),
            "memory_total": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            "memory_available": f"{psutil.virtual_memory().available / (1024**3):.2f} GB",
            "disk_usage": f"{psutil.disk_usage('/').percent}%"
        }
    
    @staticmethod
    def get_resource_usage() -> Dict[str, float]:
        """Get current resource usage"""
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        }
    
    @staticmethod
    def search_files(query: str, path: str = ".") -> List[str]:
        """Search for files matching the query"""
        results = []
        try:
            for root, _, files in os.walk(path):
                for file in files:
                    if query.lower() in file.lower():
                        results.append(os.path.join(root, file))
        except Exception as e:
            print(f"Error searching files: {e}")
        return results
    
    @staticmethod
    def execute_command(command: str) -> Optional[str]:
        """Execute a system command safely"""
        try:
            # List of allowed commands/programs
            allowed_commands = ['ls', 'dir', 'pwd', 'echo', 'date', 'time']
            
            # Basic command validation
            cmd_parts = command.split()
            if not cmd_parts or cmd_parts[0] not in allowed_commands:
                return "Command not allowed for security reasons"
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5  # 5 second timeout
            )
            return result.stdout if result.returncode == 0 else result.stderr
        except subprocess.TimeoutExpired:
            return "Command timed out"
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    @staticmethod
    def check_drivers() -> Dict[str, List[str]]:
        """Get basic driver information"""
        drivers = {"loaded": [], "errors": []}
        
        if platform.system() == "Windows":
            try:
                result = subprocess.run(
                    ["driverquery", "/FO", "CSV"],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    # Parse the CSV output and add to drivers["loaded"]
                    lines = result.stdout.split("\n")[1:]  # Skip header
                    for line in lines:
                        if line.strip():
                            drivers["loaded"].append(line.split(",")[0].strip('"'))
            except Exception as e:
                drivers["errors"].append(str(e))
        else:
            try:
                result = subprocess.run(
                    ["lsmod"],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    lines = result.stdout.split("\n")[1:]  # Skip header
                    for line in lines:
                        if line.strip():
                            drivers["loaded"].append(line.split()[0])
            except Exception as e:
                drivers["errors"].append(str(e))
        
        return drivers