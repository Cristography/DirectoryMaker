import customtkinter as ctk
import os
import re
from tkinter import filedialog, messagebox
from pathlib import Path


class DirectoryTreeCreator:
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Create main window
        self.root = ctk.CTk()
        self.root.title("Directory Maker")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)

        # Variables
        self.output_dir = ctk.StringVar()

        self.setup_ui()

    def setup_ui(self):
        # Main container with padding
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Directory Tree Creator",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 30))

        # Output Directory Selection
        dir_frame = ctk.CTkFrame(main_frame)
        dir_frame.pack(fill="x", padx=20, pady=(0, 20))

        dir_label = ctk.CTkLabel(dir_frame, text="Output Directory:", font=ctk.CTkFont(size=14, weight="bold"))
        dir_label.pack(anchor="w", padx=20, pady=(20, 5))

        dir_selection_frame = ctk.CTkFrame(dir_frame, fg_color="transparent")
        dir_selection_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.dir_entry = ctk.CTkEntry(
            dir_selection_frame,
            textvariable=self.output_dir,
            placeholder_text="Select output directory...",
            height=35
        )
        self.dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_btn = ctk.CTkButton(
            dir_selection_frame,
            text="Browse",
            command=self.browse_directory,
            width=100,
            height=35
        )
        browse_btn.pack(side="right")

        # Tree Input Section
        tree_frame = ctk.CTkFrame(main_frame)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tree_label = ctk.CTkLabel(tree_frame, text="Directory Tree Structure:",
                                  font=ctk.CTkFont(size=14, weight="bold"))
        tree_label.pack(anchor="w", padx=20, pady=(20, 5))

        # Text area with scrollbar
        text_frame = ctk.CTkFrame(tree_frame, fg_color="transparent")
        text_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tree_text = ctk.CTkTextbox(
            text_frame,
            height=300,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="none"
        )
        self.tree_text.pack(fill="both", expand=True)

        # Placeholder text
        placeholder = """project/
├── src/
│   ├── main.py
│   ├── utils.py
│   └── models/
│       └── __init__.py
├── assets/
│   ├── styles.css
│   ├── script.js
│   └── images/
│       ├── logo.png
│       └── banner.jpg
├── tests/
│   └── test_main.py
└── README.md"""

        self.tree_text.insert("1.0", placeholder)

        # Buttons Frame
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(0, 20))

        clear_btn = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_text,
            width=100,
            height=40,
            fg_color="gray"
        )
        clear_btn.pack(side="left")

        create_btn = ctk.CTkButton(
            button_frame,
            text="Create Directory Structure",
            command=self.create_structure,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        create_btn.pack(side="right")

        # Status bar
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Ready to create directory structure...",
            font=ctk.CTkFont(size=11)
        )
        self.status_label.pack(pady=(10, 20))

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir.set(directory)

    def clear_text(self):
        self.tree_text.delete("1.0", "end")

    def update_status(self, message, color="white"):
        self.status_label.configure(text=message, text_color=color)
        self.root.update()

    def parse_tree_structure(self, tree_text):
        """Parse the tree structure and return a list of file/directory paths with proper nesting"""
        lines = tree_text.strip().split('\n')
        paths = []
        path_stack = []  # Stack to maintain current path

        for line_num, line in enumerate(lines):
            if not line.strip():
                continue

            # For the first line, check if it's a root directory
            if line_num == 0 and not any(char in line for char in ['├', '└', '│']):
                root_name = line.strip().rstrip('/')
                if root_name:
                    paths.append({
                        'path': root_name,
                        'is_directory': True,
                        'depth': 0,
                        'name': root_name
                    })
                    path_stack = [root_name]
                continue

            # Determine the depth level based on tree structure
            depth = 0

            # Count the tree levels by counting '│' characters before the item
            pipe_count = 0
            idx = 0
            while idx < len(line):
                if line[idx:idx + 4] == '│   ':
                    pipe_count += 1
                    idx += 4
                elif line[idx:idx + 4] in ['├── ', '└── ']:
                    idx += 4
                    break
                else:
                    idx += 1

            depth = pipe_count + (1 if path_stack and pipe_count >= 0 else 0)

            # Extract the clean name
            clean_name = re.sub(r'^[│├└─\s]*', '', line).strip().rstrip('/')
            if not clean_name:
                continue

            # Adjust path stack to current depth
            # Keep only the directories up to current depth
            if depth < len(path_stack):
                path_stack = path_stack[:depth]

            # Build the full path
            if path_stack:
                full_path = os.path.join(*path_stack, clean_name)
            else:
                full_path = clean_name

            # Determine if it's a directory
            is_dir = self.is_directory(clean_name, line)

            # Add to paths
            paths.append({
                'path': full_path,
                'is_directory': is_dir,
                'depth': depth,
                'name': clean_name
            })

            # If it's a directory, add it to path stack for nested items
            if is_dir:
                # Ensure path_stack has the right length
                while len(path_stack) < depth:
                    path_stack.append('')  # placeholder

                if len(path_stack) == depth:
                    path_stack.append(clean_name)
                else:
                    path_stack[depth] = clean_name
                    path_stack = path_stack[:depth + 1]

        return paths

    def is_directory(self, name, original_line):
        """Determine if an item is a directory or file"""
        # If it ends with /, it's definitely a directory
        if original_line.strip().endswith('/'):
            return True

        # If it has no extension and doesn't contain common file indicators, it's likely a directory
        if '.' not in name:
            return True

        # If it has an extension, it's a file
        if '.' in name:
            return False

        return True

    def create_structure(self):
        # Validate inputs
        output_dir = self.output_dir.get().strip()
        tree_content = self.tree_text.get("1.0", "end").strip()

        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory!")
            return

        if not tree_content:
            messagebox.showerror("Error", "Please enter a directory tree structure!")
            return

        if not os.path.exists(output_dir):
            messagebox.showerror("Error", "Output directory does not exist!")
            return

        try:
            self.update_status("Parsing tree structure...", "yellow")
            parsed_items = self.parse_tree_structure(tree_content)

            if not parsed_items:
                messagebox.showerror("Error", "Could not parse any valid paths from the tree structure!")
                return

            # Debug: Show what was parsed
            debug_info = "Parsed structure:\n"
            for item in parsed_items:
                debug_info += f"  Depth {item['depth']}: {'📁' if item['is_directory'] else '📄'} {item['path']}\n"
            print(debug_info)  # This will print to console for debugging

            created_dirs = 0
            created_files = 0

            # Sort by depth to ensure parent directories are created first
            parsed_items.sort(key=lambda x: (x['depth'], x['path']))

            for item in parsed_items:
                full_path = os.path.join(output_dir, item['path'])

                if item['is_directory']:
                    # Create directory
                    if not os.path.exists(full_path):
                        os.makedirs(full_path, exist_ok=True)
                        created_dirs += 1
                        self.update_status(f"Created directory: {item['path']}", "blue")
                else:
                    # Create file - ensure parent directory exists first
                    parent_dir = os.path.dirname(full_path)
                    if parent_dir and not os.path.exists(parent_dir):
                        os.makedirs(parent_dir, exist_ok=True)

                    # Create empty file
                    if not os.path.exists(full_path):
                        try:
                            Path(full_path).touch()
                            created_files += 1
                            self.update_status(f"Created file: {item['path']}", "green")
                        except Exception as file_error:
                            self.update_status(f"Failed to create file: {item['path']} - {str(file_error)}", "red")

            # Final status
            message = f"✅ Structure created! {created_dirs} directories, {created_files} files"
            self.update_status(message, "green")

            # Show detailed summary
            summary = f"Directory structure created successfully!\n\n"
            summary += f"📁 Created {created_dirs} directories\n"
            summary += f"📄 Created {created_files} files\n"
            summary += f"📍 Location: {output_dir}\n\n"
            summary += "Structure includes proper nesting with all subdirectories and files."

            messagebox.showinfo("Success", summary)

        except Exception as e:
            error_msg = f"Error creating structure: {str(e)}"
            self.update_status(error_msg, "red")
            messagebox.showerror("Error", error_msg)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = DirectoryTreeCreator()
    app.run()
