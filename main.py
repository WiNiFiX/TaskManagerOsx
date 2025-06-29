import tkinter as tk
from tkinter import ttk
import psutil
import threading
import time

class MainWindow:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Python Process Monitor")
        
        # Set window size to 800x600
        self.root.geometry("800x600")
        
        # Center the window on screen
        self.center_window()
        
        # Configure the main window
        self.setup_ui()
        
        # Load processes when form loads
        self.load_processes()
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_ui(self):
        """Setup the user interface"""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title label
        title_label = ttk.Label(
            main_frame, 
            text="System Process Monitor", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Create Treeview for processes
        self.create_process_treeview(main_frame)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=10, sticky=(tk.W, tk.E))
        
        # Refresh button
        refresh_button = ttk.Button(
            button_frame,
            text="Refresh Processes",
            command=self.refresh_processes
        )
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        # Auto-refresh checkbox
        self.auto_refresh_var = tk.BooleanVar()
        auto_refresh_check = ttk.Checkbutton(
            button_frame,
            text="Auto-refresh (5s)",
            variable=self.auto_refresh_var,
            command=self.toggle_auto_refresh
        )
        auto_refresh_check.pack(side=tk.LEFT, padx=20)
        
        # Exit button
        exit_button = ttk.Button(
            button_frame,
            text="Exit",
            command=self.root.quit
        )
        exit_button.pack(side=tk.RIGHT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Loading processes...",
            font=("Arial", 10)
        )
        self.status_label.grid(row=3, column=0, pady=5)
        
        # Initialize auto-refresh thread
        self.auto_refresh_thread = None
        self.stop_auto_refresh = False
        
    def create_process_treeview(self, parent):
        """Create the Treeview widget for displaying processes"""
        # Create frame for treeview and scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Create Treeview
        columns = ('PID', 'Name', 'CPU %', 'Memory %', 'Status', 'User')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Define column headings
        self.tree.heading('PID', text='PID')
        self.tree.heading('Name', text='Process Name')
        self.tree.heading('CPU %', text='CPU %')
        self.tree.heading('Memory %', text='Memory %')
        self.tree.heading('Status', text='Status')
        self.tree.heading('User', text='User')
        
        # Define column widths
        self.tree.column('PID', width=80, minwidth=80)
        self.tree.column('Name', width=200, minwidth=150)
        self.tree.column('CPU %', width=80, minwidth=80)
        self.tree.column('Memory %', width=100, minwidth=100)
        self.tree.column('Status', width=100, minwidth=100)
        self.tree.column('User', width=120, minwidth=100)
        
        # Create scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
    def get_processes(self):
        """Get list of running processes"""
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status', 'username']):
                try:
                    proc_info = proc.info
                    processes.append({
                        'pid': proc_info['pid'],
                        'name': proc_info['name'] or 'Unknown',
                        'cpu_percent': proc_info['cpu_percent'] or 0.0,
                        'memory_percent': proc_info['memory_percent'] or 0.0,
                        'status': proc_info['status'] or 'Unknown',
                        'username': proc_info['username'] or 'Unknown'
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception as e:
            print(f"Error getting processes: {e}")
            
        return processes
        
    def load_processes(self):
        """Load and display processes in the treeview"""
        def load_in_thread():
            try:
                # Get processes
                processes = self.get_processes()
                
                # Sort by CPU usage (descending)
                processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
                
                # Get existing items
                existing_items = {}
                for item in self.tree.get_children():
                    values = self.tree.item(item, 'values')
                    if values:
                        pid = values[0]
                        existing_items[pid] = item
                
                # Update or add processes to treeview
                new_pids = set()
                for i, proc in enumerate(processes):
                    pid = str(proc['pid'])
                    new_pids.add(pid)
                    
                    values = (
                        proc['pid'],
                        proc['name'][:30],  # Truncate long names
                        f"{proc['cpu_percent']:.1f}",
                        f"{proc['memory_percent']:.1f}",
                        proc['status'],
                        proc['username']
                    )
                    
                    if pid in existing_items:
                        # Update existing item
                        self.tree.item(existing_items[pid], values=values)
                        # Move to correct position if needed
                        current_index = self.tree.index(existing_items[pid])
                        if current_index != i:
                            self.tree.move(existing_items[pid], '', i)
                    else:
                        # Insert new item at correct position
                        self.tree.insert('', i, values=values)
                
                # Remove items that no longer exist
                for pid, item in existing_items.items():
                    if pid not in new_pids:
                        self.tree.delete(item)
                
                # Update status
                self.root.after(0, lambda: self.status_label.config(
                    text=f"Loaded {len(processes)} processes - Last updated: {time.strftime('%H:%M:%S')}"
                ))
                
            except Exception as e:
                self.root.after(0, lambda: self.status_label.config(
                    text=f"Error loading processes: {str(e)}"
                ))
        
        # Run in separate thread to avoid blocking UI
        threading.Thread(target=load_in_thread, daemon=True).start()
        
    def refresh_processes(self):
        """Refresh the process list"""
        self.load_processes()
        
    def toggle_auto_refresh(self):
        """Toggle auto-refresh functionality"""
        if self.auto_refresh_var.get():
            self.start_auto_refresh()
        else:
            self.stop_auto_refresh = True
            
    def start_auto_refresh(self):
        """Start auto-refresh thread"""
        def auto_refresh_loop():
            while not self.stop_auto_refresh:
                time.sleep(5)  # Wait 5 seconds
                if not self.stop_auto_refresh:
                    self.root.after(0, self.refresh_processes)
        
        self.stop_auto_refresh = False
        self.auto_refresh_thread = threading.Thread(target=auto_refresh_loop, daemon=True)
        self.auto_refresh_thread.start()
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main function to start the application"""
    app = MainWindow()
    app.run()

if __name__ == "__main__":
    main() 