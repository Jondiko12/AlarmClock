import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from src.utils.git_manager import GitManager
import os

class GitControlPanel(ctk.CTkFrame):
    def __init__(self, master, repo_path: str, **kwargs):
        super().__init__(master, **kwargs)
        self.repo_path = repo_path
        self.git_manager = GitManager(repo_path)
        
        # Create UI elements
        self._create_widgets()
        
    def _create_widgets(self):
        # Status section
        status_frame = ctk.CTkFrame(self)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ctk.CTkLabel(status_frame, text="Git Status:").pack(anchor=tk.W)
        self.status_text = ctk.CTkTextbox(status_frame, height=100)
        self.status_text.pack(fill=tk.X, pady=5)
        
        # Auto-push section
        auto_push_frame = ctk.CTkFrame(self)
        auto_push_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ctk.CTkLabel(auto_push_frame, text="Auto-Push Settings:").pack(anchor=tk.W)
        
        interval_frame = ctk.CTkFrame(auto_push_frame)
        interval_frame.pack(fill=tk.X, pady=5)
        
        ctk.CTkLabel(interval_frame, text="Interval (minutes):").pack(side=tk.LEFT, padx=5)
        self.interval_var = tk.StringVar(value="5")
        self.interval_entry = ctk.CTkEntry(interval_frame, textvariable=self.interval_var, width=50)
        self.interval_entry.pack(side=tk.LEFT, padx=5)
        
        self.auto_push_button = ctk.CTkButton(
            auto_push_frame,
            text="Start Auto-Push",
            command=self._toggle_auto_push
        )
        self.auto_push_button.pack(pady=5)
        
        # Manual push section
        manual_push_frame = ctk.CTkFrame(self)
        manual_push_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ctk.CTkLabel(manual_push_frame, text="Commit Message:").pack(anchor=tk.W)
        self.commit_message = ctk.CTkEntry(manual_push_frame)
        self.commit_message.pack(fill=tk.X, pady=5)
        
        self.push_button = ctk.CTkButton(
            manual_push_frame,
            text="Commit & Push",
            command=self._manual_push
        )
        self.push_button.pack(pady=5)
        
        # Update status initially
        self._update_status()
        
    def _update_status(self):
        status = self.git_manager.get_status()
        self.status_text.delete("1.0", tk.END)
        self.status_text.insert("1.0", status)
        
    def _toggle_auto_push(self):
        if self.git_manager.is_auto_push_running:
            self.git_manager.stop_auto_push()
            self.auto_push_button.configure(text="Start Auto-Push")
        else:
            try:
                interval = int(self.interval_var.get()) * 60  # Convert to seconds
                self.git_manager.start_auto_push(interval)
                self.auto_push_button.configure(text="Stop Auto-Push")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid interval")
                
    def _manual_push(self):
        message = self.commit_message.get()
        if not message:
            message = None  # Will use default message
            
        if self.git_manager.commit_and_push(message):
            messagebox.showinfo("Success", "Changes committed and pushed successfully")
            self._update_status()
        else:
            messagebox.showerror("Error", "Failed to commit and push changes")
            
    def update(self):
        """Update the status display"""
        self._update_status() 