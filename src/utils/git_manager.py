import os
import subprocess
import threading
import time
from datetime import datetime
from typing import List, Optional

class GitManager:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.auto_push_interval = 300  # 5 minutes default
        self.auto_push_thread: Optional[threading.Thread] = None
        self.is_auto_push_running = False

    def commit_and_push(self, message: str = None) -> bool:
        try:
            if not message:
                message = f"Auto commit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Add all changes
            subprocess.run(['git', 'add', '.'], cwd=self.repo_path, check=True)
            
            # Commit changes
            subprocess.run(['git', 'commit', '-m', message], cwd=self.repo_path, check=True)
            
            # Push changes
            subprocess.run(['git', 'push'], cwd=self.repo_path, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Git operation failed: {e}")
            return False

    def get_status(self) -> str:
        try:
            result = subprocess.run(['git', 'status'], cwd=self.repo_path, 
                                  capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError:
            return "Error getting git status"

    def get_remotes(self) -> List[str]:
        try:
            result = subprocess.run(['git', 'remote', '-v'], cwd=self.repo_path,
                                  capture_output=True, text=True, check=True)
            return result.stdout.splitlines()
        except subprocess.CalledProcessError:
            return []

    def start_auto_push(self, interval: int = None):
        if interval:
            self.auto_push_interval = interval
        
        if not self.is_auto_push_running:
            self.is_auto_push_running = True
            self.auto_push_thread = threading.Thread(target=self._auto_push_loop)
            self.auto_push_thread.daemon = True
            self.auto_push_thread.start()

    def stop_auto_push(self):
        self.is_auto_push_running = False
        if self.auto_push_thread:
            self.auto_push_thread.join()

    def _auto_push_loop(self):
        while self.is_auto_push_running:
            self.commit_and_push()
            time.sleep(self.auto_push_interval) 