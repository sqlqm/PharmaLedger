import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import subprocess
import os
import time
import json
from pathlib import Path
import webbrowser
from datetime import datetime

class PharmaLedgerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PharmaLedger - A Blockchain-Based Medicine Tracking Dashboard")
        self.root.geometry("1400x900")
        
        # Modern color scheme
        self.colors = {
            'primary': '#2563eb',      # Blue
            'secondary': '#7c3aed',    # Purple
            'success': '#10b981',      # Green
            'danger': '#ef4444',       # Red
            'warning': '#f59e0b',      # Orange
            'info': '#06b6d4',         # Cyan
            'bg_dark': '#1f2937',      # Dark gray
            'bg_light': '#f3f4f6',     # Light gray
            'text_dark': '#111827',    # Almost black
            'text_light': '#6b7280',   # Gray
        }
        
        # Animation state
        self.is_loading = False
        self.loading_angle = 0
        self.progress_value = 0
        
        # Operation lock to prevent multiple simultaneous operations
        self.operation_running = False
        
        self.setup_styles()
        self.create_widgets()
        self.check_files()
        
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Primary.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=10)
        style.map('Primary.TButton',
                 background=[('active', '#1d4ed8')])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white',
                       borderwidth=0,
                       padding=10)
        
        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground='white',
                       borderwidth=0,
                       padding=10)
        
        # Progress bar style
        style.configure('Custom.Horizontal.TProgressbar',
                       background=self.colors['primary'],
                       troughcolor=self.colors['bg_light'],
                       borderwidth=0,
                       thickness=20)
        
    def create_widgets(self):
        """Create the main GUI layout"""
        # Configure root background
        self.root.configure(bg=self.colors['bg_light'])
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['primary'], height=100)
        header.pack(fill='x')
        
        title_label = tk.Label(header,
                              text="💊 PharmaLedger",
                              font=('Segoe UI', 28, 'bold'),
                              bg=self.colors['primary'],
                              fg='white')
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(header,
                                 text="Blockchain-Powered Pharmaceutical Supply Chain Management",
                                 font=('Segoe UI', 12),
                                 bg=self.colors['primary'],
                                 fg='#e0e7ff')
        subtitle_label.pack()
        
        # Main container
        container = tk.Frame(self.root, bg=self.colors['bg_light'])
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Top row - Stats cards
        stats_row = tk.Frame(container, bg=self.colors['bg_light'])
        stats_row.pack(fill='x', pady=(0, 15))
        
        self.create_stats_cards(stats_row)
        
        # Middle row - Main content
        middle_row = tk.Frame(container, bg=self.colors['bg_light'])
        middle_row.pack(fill='both', expand=True)
        
        # Left panel - Actions
        left_panel = tk.Frame(middle_row, bg=self.colors['bg_light'])
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.create_blockchain_card(left_panel)
        self.create_analysis_card(left_panel)
        
        # Middle panel - Visualization
        middle_panel = tk.Frame(middle_row, bg=self.colors['bg_light'])
        middle_panel.pack(side='left', fill='both', expand=True, padx=5)
        
        self.create_visualization_card(middle_panel)
        
        # Right panel - Status and Output
        right_panel = tk.Frame(middle_row, bg=self.colors['bg_light'])
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        self.create_status_card(right_panel)
        self.create_output_card(right_panel)
        
        # Footer
        footer = tk.Frame(self.root, bg='white', height=50)
        footer.pack(fill='x', side='bottom')
        
        footer_label = tk.Label(footer,
                               text=f"© 2024 PharmaLedger Team | CSE 532 Project | {datetime.now().strftime('%I:%M %p')}",
                               font=('Segoe UI', 9),
                               bg='white',
                               fg=self.colors['text_light'])
        footer_label.pack(pady=15)
        
    def create_stats_cards(self, parent):
        """Create statistics cards at the top"""
        self.stats_frames = []
        
        stats = [
            ('📊 Total Transactions', '142,268', self.colors['primary']),
            ('📦 Unique Products', '24,501', self.colors['success']),
            ('🏢 Participants', '45', self.colors['warning']),
            ('⛓️ Blockchain Blocks', '0', self.colors['secondary']),
        ]
        
        for title, value, color in stats:
            card = tk.Frame(parent, bg='white', relief='flat', width=200)
            card.pack(side='left', fill='both', expand=True, padx=5)
            
            # Shadow effect
            shadow = tk.Frame(parent, bg='#d1d5db', relief='flat')
            shadow.place(in_=card, x=2, y=2, relwidth=1, relheight=1)
            card.lift()
            
            # Content
            tk.Label(card,
                    text=title,
                    font=('Segoe UI', 10),
                    bg='white',
                    fg=self.colors['text_light']).pack(pady=(15, 5))
            
            value_label = tk.Label(card,
                                  text=value,
                                  font=('Segoe UI', 24, 'bold'),
                                  bg='white',
                                  fg=color)
            value_label.pack(pady=(0, 15))
            
            self.stats_frames.append(value_label)
            
    def create_visualization_card(self, parent):
        """Create central visualization card with loading animation"""
        content = self.create_card(parent, "📈 Live Visualization")
        
        # Canvas for visualization
        self.viz_canvas = tk.Canvas(content,
                                    bg='#f9fafb',
                                    highlightthickness=0,
                                    height=400)
        self.viz_canvas.pack(fill='both', expand=True, pady=10)
        
        # Progress bar
        self.progress_label = tk.Label(content,
                                      text="",
                                      font=('Segoe UI', 10),
                                      bg='white',
                                      fg=self.colors['text_light'])
        self.progress_label.pack(pady=(10, 5))
        
        self.progress_bar = ttk.Progressbar(content,
                                           style='Custom.Horizontal.TProgressbar',
                                           mode='determinate',
                                           length=400)
        self.progress_bar.pack(pady=(0, 10))
        
        # Status message
        self.viz_status = tk.Label(content,
                                  text="Ready to analyze data",
                                  font=('Segoe UI', 11),
                                  bg='white',
                                  fg=self.colors['text_dark'])
        self.viz_status.pack(pady=10)
        
        # Draw initial idle state after canvas is ready
        self.root.after(100, self.draw_idle_visualization)
        
    def draw_idle_visualization(self):
        """Draw idle state visualization"""
        self.viz_canvas.delete('all')
        
        # Force canvas to update its dimensions
        self.viz_canvas.update_idletasks()
        w = self.viz_canvas.winfo_width()
        h = self.viz_canvas.winfo_height()
        
        # Use minimum dimensions if canvas isn't ready
        if w < 50:
            w = 500
        if h < 50:
            h = 400
        
        # Draw blockchain icon - centered properly
        cx, cy = w // 2, h // 2
        
        # Smaller blocks for better fit
        block_size = 70
        spacing = 20
        
        # Draw 3 blocks horizontally centered
        start_x = cx - (block_size * 1.5 + spacing)
        
        # Draw blocks
        for i in range(3):
            x = start_x + i * (block_size + spacing)
            y = cy - block_size // 2
            
            # Block shadow
            self.viz_canvas.create_rectangle(x + 3, y + 3, x + block_size + 3, y + block_size + 3,
                                           fill='#d1d5db',
                                           outline='')
            # Block
            self.viz_canvas.create_rectangle(x, y, x + block_size, y + block_size,
                                           fill='white',
                                           outline=self.colors['primary'],
                                           width=2)
            
            # Block icon (cube emoji or simple shape)
            self.viz_canvas.create_text(x + block_size // 2, y + block_size // 2,
                                       text='📦',
                                       font=('Segoe UI', 28))
            
            # Connecting arrow
            if i < 2:
                self.viz_canvas.create_line(x + block_size, cy,
                                          x + block_size + spacing, cy,
                                          fill=self.colors['primary'],
                                          width=3,
                                          arrow=tk.LAST)
        
        # Status text - centered below
        self.viz_canvas.create_text(cx, cy + block_size,
                                   text='Blockchain System Ready',
                                   font=('Segoe UI', 14, 'bold'),
                                   fill=self.colors['text_dark'])
        
    def draw_loading_animation(self):
        """Draw animated loading visualization"""
        if not self.is_loading:
            return
            
        self.viz_canvas.delete('all')
        self.viz_canvas.update_idletasks()
        w = self.viz_canvas.winfo_width()
        h = self.viz_canvas.winfo_height()
        
        if w < 50:
            w = 500
        if h < 50:
            h = 400
            
        cx, cy = w // 2, h // 2
        
        # Animated spinner
        import math
        radius = 50
        for i in range(8):
            angle = math.radians((self.loading_angle + i * 45) % 360)
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            
            # Create fading circles
            size = 10 - i
            self.viz_canvas.create_oval(x - size, y - size, x + size, y + size,
                                       fill=self.colors['primary'],
                                       outline='')
        
        # Center text
        self.viz_canvas.create_text(cx, cy + 80,
                                   text='Processing...',
                                   font=('Segoe UI', 14, 'bold'),
                                   fill=self.colors['primary'])
        
        # Continue animation
        self.loading_angle = (self.loading_angle + 10) % 360
        self.root.after(50, self.draw_loading_animation)
        
    def draw_blockchain_building(self, blocks_created):
        """Draw simple blockchain building visualization"""
        self.viz_canvas.delete('all')
        self.viz_canvas.update_idletasks()
        w = self.viz_canvas.winfo_width()
        h = self.viz_canvas.winfo_height()
        
        if w < 50:
            w = 500
        if h < 50:
            h = 400
        
        # Simple center position
        cx = w // 2
        cy = h // 2 - 20
        
        # Block size
        size = 60
        gap = 15
        
        # 4 positions in a square
        positions = [
            (cx - size - gap//2, cy - size - gap//2),  # 1: top-left
            (cx + gap//2, cy - size - gap//2),          # 2: top-right
            (cx + gap//2, cy + gap//2),                 # 3: bottom-right
            (cx - size - gap//2, cy + gap//2),          # 4: bottom-left
        ]
        
        # Which block is currently active (cycles 0-3)
        active = (blocks_created // 7000) % 4
        
        # Draw all 4 blocks
        for i in range(4):
            x, y = positions[i]
            
            # Active block is green, others blue
            color = self.colors['success'] if i == active else self.colors['primary']
            
            # Shadow
            self.viz_canvas.create_rectangle(
                x + 3, y + 3, x + size + 3, y + size + 3,
                fill='#d1d5db', outline=''
            )
            
            # Block
            self.viz_canvas.create_rectangle(
                x, y, x + size, y + size,
                fill=color, outline='white', width=3
            )
        
        # Draw arrows
        # 1 → 2
        self.viz_canvas.create_line(
            positions[0][0] + size, positions[0][1] + size//2,
            positions[1][0], positions[1][1] + size//2,
            fill=self.colors['success'] if active == 1 else self.colors['primary'],
            width=3, arrow=tk.LAST
        )
        
        # 2 → 3
        self.viz_canvas.create_line(
            positions[1][0] + size//2, positions[1][1] + size,
            positions[2][0] + size//2, positions[2][1],
            fill=self.colors['success'] if active == 2 else self.colors['primary'],
            width=3, arrow=tk.LAST
        )
        
        # 3 → 4
        self.viz_canvas.create_line(
            positions[2][0], positions[2][1] + size//2,
            positions[3][0] + size, positions[3][1] + size//2,
            fill=self.colors['success'] if active == 3 else self.colors['primary'],
            width=3, arrow=tk.LAST
        )
        
        # 4 → 1
        self.viz_canvas.create_line(
            positions[3][0] + size//2, positions[3][1],
            positions[0][0] + size//2, positions[0][1] + size,
            fill=self.colors['success'] if active == 0 else self.colors['warning'],
            width=3, arrow=tk.LAST,
            dash=(5, 3) if active != 0 else ()
        )
        
        # Single status line at bottom
        progress = (blocks_created / 142269) * 100
        self.viz_canvas.create_text(
            cx, h - 40,
            text=f'Blocks Created: {blocks_created:,} ({progress:.1f}%)',
            font=('Segoe UI', 13, 'bold'),
            fill=self.colors['text_dark']
        )
    
    def generate_spiral_positions(self, max_blocks, block_size, spacing, center_x, center_y):
        """Removed - no longer needed"""
        return []
        
    def draw_success_state(self, message):
        """Draw success state"""
        self.viz_canvas.delete('all')
        self.viz_canvas.update_idletasks()
        w = self.viz_canvas.winfo_width()
        h = self.viz_canvas.winfo_height()
        
        if w < 50:
            w = 500
        if h < 50:
            h = 400
            
        cx, cy = w // 2, h // 2
        
        # Success checkmark circle
        self.viz_canvas.create_oval(cx - 60, cy - 60, cx + 60, cy + 60,
                                   fill=self.colors['success'],
                                   outline='')
        
        # Checkmark
        self.viz_canvas.create_text(cx, cy,
                                   text='✓',
                                   font=('Segoe UI', 50, 'bold'),
                                   fill='white')
        
        # Message
        self.viz_canvas.create_text(cx, cy + 90,
                                   text=message,
                                   font=('Segoe UI', 14, 'bold'),
                                   fill=self.colors['success'])
        
    def create_card(self, parent, title):
        """Create a styled card container"""
        card = tk.Frame(parent, bg='white', relief='flat', borderwidth=1)
        card.pack(fill='both', expand=True, pady=(0, 15))
        
        # Add shadow effect
        shadow = tk.Frame(parent, bg='#d1d5db', relief='flat')
        shadow.place(in_=card, x=3, y=3, relwidth=1, relheight=1)
        card.lift()
        
        # Card header
        header = tk.Frame(card, bg='white')
        header.pack(fill='x', padx=20, pady=(15, 10))
        
        title_label = tk.Label(header,
                              text=title,
                              font=('Segoe UI', 14, 'bold'),
                              bg='white',
                              fg=self.colors['text_dark'])
        title_label.pack(anchor='w')
        
        # Card content
        content = tk.Frame(card, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        return content
        
    def create_blockchain_card(self, parent):
        """Create blockchain operations card"""
        content = self.create_card(parent, "⛓️ Blockchain Operations")
        
        # View Dataset button
        btn_view = tk.Button(content,
                            text="📊 View Dataset Info",
                            command=self.view_dataset,
                            bg=self.colors['primary'],
                            fg='white',
                            font=('Segoe UI', 10),
                            relief='flat',
                            cursor='hand2',
                            padx=15,
                            pady=10)
        btn_view.pack(fill='x', pady=(0, 8))
        
        # Build Blockchain button
        btn_build = tk.Button(content,
                             text="🔨 Build Blockchain",
                             command=self.build_blockchain,
                             bg=self.colors['success'],
                             fg='white',
                             font=('Segoe UI', 10),
                             relief='flat',
                             cursor='hand2',
                             padx=15,
                             pady=10)
        btn_build.pack(fill='x', pady=(0, 8))
        
        # Export to JSON button
        btn_export = tk.Button(content,
                              text="💾 Export Blockchain JSON",
                              command=self.export_json,
                              bg=self.colors['secondary'],
                              fg='white',
                              font=('Segoe UI', 10),
                              relief='flat',
                              cursor='hand2',
                              padx=15,
                              pady=10)
        btn_export.pack(fill='x')
        
    def create_analysis_card(self, parent):
        """Create analysis operations card"""
        content = self.create_card(parent, "📈 Data Analysis")
        
        # Transit Time Analysis
        btn_transit = tk.Button(content,
                               text="🚚 Transit Time Analysis",
                               command=self.run_transit_analysis,
                               bg=self.colors['primary'],
                               fg='white',
                               font=('Segoe UI', 10),
                               relief='flat',
                               cursor='hand2',
                               padx=15,
                               pady=10)
        btn_transit.pack(fill='x', pady=(0, 8))
        
        # Tampering Detection
        btn_tamper = tk.Button(content,
                              text="🔒 Tampering Detection Test",
                              command=self.run_tamper_test,
                              bg=self.colors['danger'],
                              fg='white',
                              font=('Segoe UI', 10),
                              relief='flat',
                              cursor='hand2',
                              padx=15,
                              pady=10)
        btn_tamper.pack(fill='x', pady=(0, 8))
        
        # ML Predictions
        btn_predict = tk.Button(content,
                               text="🤖 ML Transit Predictions",
                               command=self.run_predictions,
                               bg=self.colors['warning'],
                               fg='white',
                               font=('Segoe UI', 10),
                               relief='flat',
                               cursor='hand2',
                               padx=15,
                               pady=10)
        btn_predict.pack(fill='x')
        
    def create_status_card(self, parent):
        """Create system status card"""
        content = self.create_card(parent, "✅ System Status")
        
        # File status indicators
        self.status_labels = {}
        
        files_to_check = [
            ('CSV Dataset', 'dscsa_transactions_2024_2025.csv'),
            ('Blockchain Code', 'chain.py'),
            ('Project Script', 'project.py'),
            ('Transit Analysis', 'transit_time.py'),
            ('Tamper Test', 'tamper_measure.py'),
            ('Predictions', 'predict_transit_time.py'),
        ]
        
        for name, filename in files_to_check:
            frame = tk.Frame(content, bg='white')
            frame.pack(fill='x', pady=4)
            
            label = tk.Label(frame,
                           text=name,
                           font=('Segoe UI', 9),
                           bg='white',
                           fg=self.colors['text_dark'],
                           width=18,
                           anchor='w')
            label.pack(side='left')
            
            status = tk.Label(frame,
                            text="⏳",
                            font=('Segoe UI', 9),
                            bg='white',
                            fg=self.colors['text_light'])
            status.pack(side='right')
            
            self.status_labels[filename] = status
            
    def create_output_card(self, parent):
        """Create output/log card"""
        content = self.create_card(parent, "📝 Output Log")
        
        # Output text area with scrollbar
        scroll_frame = tk.Frame(content, bg='white')
        scroll_frame.pack(fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(scroll_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Terminal-style text widget
        self.output_text = tk.Text(scroll_frame,
                                   wrap='word',
                                   yscrollcommand=scrollbar.set,
                                   font=('Consolas', 9),
                                   bg='#1e1e1e',  # Dark background
                                   fg='#d4d4d4',  # Light gray text
                                   insertbackground='#00ff00',  # Green cursor
                                   selectbackground='#264f78',
                                   relief='flat',
                                   padx=12,
                                   pady=12,
                                   height=15)
        self.output_text.pack(fill='both', expand=True)
        scrollbar.config(command=self.output_text.yview)
        
        # Configure text tags for colored terminal output
        self.output_text.tag_config('timestamp', foreground='#858585')  # Gray
        self.output_text.tag_config('success', foreground='#4ec9b0')    # Cyan
        self.output_text.tag_config('error', foreground='#f48771')      # Red
        self.output_text.tag_config('warning', foreground='#dcdcaa')    # Yellow
        self.output_text.tag_config('info', foreground='#569cd6')       # Blue
        self.output_text.tag_config('lock', foreground='#c586c0')       # Purple
        self.output_text.tag_config('separator', foreground='#608b4e')  # Green
        self.output_text.tag_config('normal', foreground='#d4d4d4')     # Light gray
        
        # Welcome message
        self.output_text.insert('end', '╔═══════════════════════════════════════════════════════╗\n', 'separator')
        self.output_text.insert('end', '║   ', 'separator')
        self.output_text.insert('end', 'PharmaLedger Blockchain System', 'success')
        self.output_text.insert('end', '                    ║\n', 'separator')
        self.output_text.insert('end', '╚═══════════════════════════════════════════════════════╝\n', 'separator')
        self.output_text.insert('end', f'\n$ System initialized at ', 'normal')
        self.output_text.insert('end', f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n', 'timestamp')
        self.output_text.insert('end', '$ Ready to process operations...\n\n', 'info')
        
        # Button frame
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(pady=(10, 0))
        
        # Clear button
        btn_clear = tk.Button(btn_frame,
                             text="🗑️ Clear",
                             command=self.clear_output,
                             bg=self.colors['bg_light'],
                             fg=self.colors['text_dark'],
                             font=('Segoe UI', 8),
                             relief='flat',
                             cursor='hand2',
                             padx=12,
                             pady=6)
        btn_clear.pack(side='left', padx=3)
        
        # View Results button
        btn_results = tk.Button(btn_frame,
                               text="📂 View Files",
                               command=self.view_results,
                               bg=self.colors['primary'],
                               fg='white',
                               font=('Segoe UI', 8),
                               relief='flat',
                               cursor='hand2',
                               padx=12,
                               pady=6)
        btn_results.pack(side='left', padx=3)
        
    def check_files(self):
        """Check if required files exist"""
        for filename, status_label in self.status_labels.items():
            if os.path.exists(filename):
                status_label.config(text="✅", fg=self.colors['success'])
            else:
                status_label.config(text="❌", fg=self.colors['danger'])
    
    
    def log_output(self, message, tag='info'):
        """Add message to output log with terminal-style colors"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        # Add timestamp in gray
        self.output_text.insert('end', f'[{timestamp}] ', 'timestamp')
        
        # Detect message type and apply appropriate color
        if '✅' in message or 'success' in message.lower() or 'complete' in message.lower():
            self.output_text.insert('end', message + '\n', 'success')
        elif '❌' in message or 'error' in message.lower() or 'failed' in message.lower():
            self.output_text.insert('end', message + '\n', 'error')
        elif '⚠️' in message or 'warning' in message.lower():
            self.output_text.insert('end', message + '\n', 'warning')
        elif '🔒' in message or 'locked' in message.lower():
            self.output_text.insert('end', message + '\n', 'lock')
        elif '🔓' in message or 'unlocked' in message.lower():
            self.output_text.insert('end', message + '\n', 'success')
        elif '🚀' in message:
            self.output_text.insert('end', message + '\n', 'info')
        elif '=' * 10 in message:
            self.output_text.insert('end', message + '\n', 'separator')
        else:
            self.output_text.insert('end', message + '\n', 'normal')
        
        self.output_text.see('end')
        self.root.update()
        
    def clear_output(self):
        """Clear the output log"""
        self.output_text.delete(1.0, 'end')
        
    def start_loading(self, message="Processing..."):
        """Start loading animation"""
        self.is_loading = True
        self.viz_status.config(text=message, fg=self.colors['primary'])
        self.progress_label.config(text=message)
        self.progress_bar['value'] = 0
        self.draw_loading_animation()
        
    def stop_loading(self, success=True, message="Complete"):
        """Stop loading animation"""
        self.is_loading = False
        self.progress_bar['value'] = 100
        if success:
            self.viz_status.config(text=message, fg=self.colors['success'])
            self.draw_success_state(message)
        else:
            self.viz_status.config(text=message, fg=self.colors['danger'])
        
    def update_progress(self, value, message=""):
        """Update progress bar"""
        self.progress_bar['value'] = value
        if message:
            self.progress_label.config(text=message)
            
    def run_command(self, command, description, visualize=True):
        """Run a command in a separate thread"""
        self.log_output(f"\n{'='*50}")
        self.log_output(f"🚀 {description}")
        self.log_output(f"🔒 Operation locked")
        self.log_output(f"{'='*50}\n")
        
        if visualize:
            self.start_loading(description)
        
        def run():
            # Start a progress simulation thread
            stop_progress = threading.Event()
            
            def simulate_progress():
                """Simulate progress while operation runs"""
                progress = 0
                while not stop_progress.is_set() and progress < 95:
                    progress = min(95, progress + 1)
                    self.root.after(0, lambda p=progress: self.update_progress(p, f"{description}..."))
                    time.sleep(0.3)  # Update every 0.3 seconds
            
            # Start progress simulation
            if visualize:
                progress_thread = threading.Thread(target=simulate_progress, daemon=True)
                progress_thread.start()
            
            try:
                # Set environment variable to prevent matplotlib from showing plots
                env = os.environ.copy()
                env['MPLBACKEND'] = 'Agg'
                # Set Python to use UTF-8 encoding
                env['PYTHONIOENCODING'] = 'utf-8'
                
                # If it's a matplotlib-using script, wrap it with suppression code
                if 'tamper_measure.py' in command:
                    wrapper = self.create_matplotlib_wrapper('tamper_measure.py')
                    cmd = f'python {wrapper}'
                else:
                    cmd = command
                    wrapper = None
                
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    env=env,
                    encoding='utf-8',
                    errors='replace'  # Replace encoding errors with ?
                )
                
                # Stop progress simulation
                stop_progress.set()
                
                # Clean up temp file
                if wrapper:
                    try:
                        os.remove(wrapper)
                    except:
                        pass
                
                if result.stdout:
                    self.log_output(result.stdout)
                    
                    # Update blockchain stat if building
                    if '--build-chain' in command and 'Chain built:' in result.stdout:
                        try:
                            blocks = int(result.stdout.split('Chain built:')[1].split('blocks')[0].strip())
                            self.stats_frames[3].config(text=f'{blocks:,}')
                        except:
                            pass
                
                if result.stderr and result.returncode != 0:
                    # Clean up error messages for better readability
                    error_msg = result.stderr
                    # Remove long stack traces if present
                    if 'Traceback' in error_msg:
                        lines = error_msg.split('\n')
                        # Get just the error type and message
                        error_lines = [l for l in lines if 'Error:' in l or 'Exception:' in l]
                        if error_lines:
                            error_msg = '\n'.join(error_lines[-3:])  # Last 3 error lines
                    self.log_output(f"⚠️ Error: {error_msg}")
                    
                if visualize:
                    self.update_progress(100, f"{description} - Complete!")
                    time.sleep(0.5)
                    
                if result.returncode == 0:
                    self.log_output(f"\n✅ {description} completed successfully!\n")
                    if visualize:
                        self.stop_loading(True, f"{description} - Success!")
                    
                    # Offer to view tampering detection chart
                    if 'tamper_measure.py' in command and os.path.exists("detection_rate_chart.png"):
                        view_result = messagebox.askyesno(
                            "Chart Ready",
                            "Tampering detection chart generated!\n\nView now?"
                        )
                        if view_result:
                            webbrowser.open("detection_rate_chart.png")
                else:
                    self.log_output(f"\n❌ {description} failed.\n")
                    if visualize:
                        self.stop_loading(False, f"{description} - Failed")
                    
            except Exception as e:
                stop_progress.set()
                self.log_output(f"\n❌ Error: {str(e)}\n")
                if visualize:
                    self.stop_loading(False, "Error occurred")
            finally:
                # Unlock operations on main thread
                def unlock():
                    self.operation_running = False
                    self.log_output("🔓 Operation unlocked - ready for next task\n")
                self.root.after(0, unlock)
                
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
        
    def view_dataset(self):
        """View dataset information"""
        if self.operation_running:
            messagebox.showwarning("Operation in Progress", "Please wait for the current operation to complete.")
            return
        self.run_command("python project.py", "Loading Dataset", visualize=True)
        
    def build_blockchain(self):
        """Build the blockchain"""
        if self.operation_running:
            messagebox.showwarning("Operation in Progress", "Please wait for the current operation to complete.")
            return
            
        result = messagebox.askyesno(
            "Build Blockchain",
            "This will build a blockchain.\n"
            "Estimated time: 30-60 seconds.\n\n"
            "Continue?"
        )
        if result:
            # Double-check lock wasn't set during dialog
            if self.operation_running:
                messagebox.showwarning("Operation in Progress", "Please wait for the current operation to complete.")
                return
            self.operation_running = True  # Lock operations
            self.is_loading = False  # Stop any loading animation
            self.viz_status.config(text="Building Blockchain...", fg=self.colors['primary'])
            self.progress_label.config(text="Initializing...")
            self.progress_bar['value'] = 0
            
            def build_with_progress():
                try:
                    # Start the actual blockchain build process
                    process = subprocess.Popen(
                        "python project.py --build-chain",
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    # Estimated time: 45 seconds (adjust based on your system)
                    estimated_time = 45  # seconds
                    update_interval = 0.5  # update every 0.5 seconds
                    total_updates = int(estimated_time / update_interval)
                    
                    # Progress simulation while building (stops at 99%)
                    for i in range(total_updates):
                        if process.poll() is not None:
                            # Process finished early
                            break
                        
                        # Calculate progress (max 99% until actually complete)
                        progress = min(99, int((i / total_updates) * 100))
                        blocks_simulated = int((progress / 100) * 142269)
                        
                        # Update UI on main thread
                        self.root.after(0, lambda p=progress, b=blocks_simulated: (
                            self.progress_bar.config(value=p),
                            self.progress_label.config(text=f"Building blocks..."),
                            self.viz_status.config(text=f"Building Blockchain"),
                            self.draw_blockchain_building(b)
                        ))
                        
                        time.sleep(update_interval)
                    
                    # Wait for process to complete
                    stdout, stderr = process.communicate()
                    
                    # Log output on main thread
                    self.root.after(0, lambda: self.log_output(stdout))
                    if stderr and process.returncode != 0:
                        self.root.after(0, lambda: self.log_output(f"⚠️ Error: {stderr}"))
                    
                    # Final update to 100%
                    if process.returncode == 0:
                        self.root.after(0, lambda: (
                            self.progress_bar.config(value=100),
                            self.progress_label.config(text="Complete!"),
                            self.viz_status.config(text="Blockchain Built Successfully!", fg=self.colors['success']),
                            self.draw_blockchain_building(142269)
                        ))
                        self.root.after(0, lambda: self.stats_frames[3].config(text='142,269'))
                        self.root.after(0, lambda: self.log_output("\n✅ Blockchain built successfully!\n"))
                        time.sleep(1)
                        self.root.after(0, lambda: self.draw_success_state("Blockchain Built Successfully!"))
                    else:
                        self.root.after(0, lambda: self.log_output("\n❌ Blockchain build failed.\n"))
                        self.root.after(0, lambda: (
                            self.viz_status.config(text="Build Failed", fg=self.colors['danger']),
                            self.progress_bar.config(value=0)
                        ))
                finally:
                    # Unlock operations on main thread
                    self.root.after(0, lambda: setattr(self, 'operation_running', False))
                
            thread = threading.Thread(target=build_with_progress)
            thread.daemon = True
            thread.start()
            
    def export_json(self):
        """Export blockchain to JSON"""
        if self.operation_running:
            messagebox.showwarning("Operation in Progress", "Please wait for the current operation to complete.")
            return
            
        result = messagebox.askyesno(
            "Export Blockchain",
            "This will create a ~300 MB JSON file.\n"
            "Estimated time: 60-90 seconds.\n\n"
            "Continue?"
        )
        if result:
            # Double-check lock wasn't set during dialog
            if self.operation_running:
                messagebox.showwarning("Operation in Progress", "Please wait for the current operation to complete.")
                return
            self.operation_running = True
            self.run_command(
                "python project.py --build-chain --chain-output json1.json",
                "Exporting to JSON",
                visualize=True
            )
            
    def create_matplotlib_wrapper(self, script_name):
        """Create a temporary wrapper script to suppress matplotlib"""
        wrapper_content = f"""import sys
import os
os.environ['MPLBACKEND'] = 'Agg'
import matplotlib
matplotlib.use('Agg', force=True)
import matplotlib.pyplot as plt
original_show = plt.show
plt.show = lambda *args, **kwargs: None
exec(open('{script_name}').read())
"""
        # Write to temp file
        with open('_temp_wrapper.py', 'w') as f:
            f.write(wrapper_content)
        return '_temp_wrapper.py'
    
    def run_transit_analysis(self):
        """Run transit time analysis"""
        if self.operation_running:
            messagebox.showwarning("Operation in Progress", "Please wait for the current operation to complete.")
            return
            
        self.operation_running = True
        self.start_loading("Analyzing Transit Times...")
        
        def analyze():
            # Progress simulation
            stop_progress = threading.Event()
            
            def simulate_progress():
                progress = 0
                while not stop_progress.is_set() and progress < 95:
                    progress = min(95, progress + 1)
                    self.root.after(0, lambda p=progress: self.update_progress(p, "Analyzing transit times..."))
                    time.sleep(0.3)
            
            progress_thread = threading.Thread(target=simulate_progress, daemon=True)
            progress_thread.start()
            
            try:
                # Create wrapper to suppress matplotlib
                wrapper = self.create_matplotlib_wrapper('transit_time.py')
                
                # Set environment variable
                env = os.environ.copy()
                env['MPLBACKEND'] = 'Agg'
                env['PYTHONIOENCODING'] = 'utf-8'
                
                # Run with wrapper
                result = subprocess.run(
                    f'python {wrapper}',
                    shell=True,
                    capture_output=True,
                    text=True,
                    env=env,
                    encoding='utf-8',
                    errors='replace'
                )
                
                # Stop progress simulation
                stop_progress.set()
                
                # Clean up temp file
                try:
                    os.remove(wrapper)
                except:
                    pass
                
                self.log_output(result.stdout)
                self.update_progress(100, "Analysis complete!")
                time.sleep(1)
                self.stop_loading(True, "Transit Analysis Complete!")
                
                # Offer to view chart
                if os.path.exists("top10_transit_time_avg_variability.png"):
                    view_result = messagebox.askyesno(
                        "Chart Ready",
                        "Transit time chart generated!\n\nView now?"
                    )
                    if view_result:
                        webbrowser.open("top10_transit_time_avg_variability.png")
            except Exception as e:
                stop_progress.set()
                self.log_output(f"\n❌ Error: {str(e)}\n")
                self.stop_loading(False, "Analysis Failed")
            finally:
                def unlock():
                    self.operation_running = False
                    self.log_output("🔓 Operation unlocked - ready for next task\n")
                self.root.after(0, unlock)
        
        thread = threading.Thread(target=analyze)
        thread.daemon = True
        thread.start()
        
    def run_tamper_test(self):
        """Run tampering detection test"""
        if self.operation_running:
            messagebox.showwarning("Operation in Progress", "Please wait for the current operation to complete.")
            return
            
        if not os.path.exists("json1.json"):
            messagebox.showwarning(
                "JSON Required",
                "Please export blockchain JSON first."
            )
            return
            
        result = messagebox.askyesno(
            "Tampering Detection",
            "Run 10 tampering experiments?\n"
            "Estimated time: 60-120 seconds.\n\n"
            "Continue?"
        )
        if result:
            # Double-check lock wasn't set during dialog
            if self.operation_running:
                messagebox.showwarning("Operation in Progress", "Please wait for the current operation to complete.")
                return
            self.operation_running = True
            self.run_command("python tamper_measure.py", "Testing Tampering Detection", visualize=True)
            
    def run_predictions(self):
        """Run ML predictions"""
        if self.operation_running:
            messagebox.showwarning("Operation in Progress", "Please wait for the current operation to complete.")
            return
        
        self.operation_running = True
        self.run_command("python predict_transit_time.py", "Running ML Predictions", visualize=True)
        
    def view_results(self):
        """Open folder containing generated files"""
        folder = os.getcwd()
        if os.name == 'nt':  # Windows
            os.startfile(folder)
        elif os.name == 'posix':  # macOS/Linux
            subprocess.run(['open' if os.uname().sysname == 'Darwin' else 'xdg-open', folder])

def main():
    root = tk.Tk()
    
    # Set window icon (if available)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    app = PharmaLedgerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()