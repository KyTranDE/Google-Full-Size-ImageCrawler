import customtkinter as ctk
from tkinter import filedialog, messagebox
import main
import threading

ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Google-Full-Size-ImageCrawler GUI")
        self.geometry("900x400")
        self.configure(bg="black") 
        self.resizable(False, False)
            
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2.5) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
    
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Web Crawler", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="Select Save Path", command=self.browse_directory)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text="Start Crawling", command=self.start_crawling)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionmenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"], command=self.change_appearance_mode)
        self.appearance_mode_optionmenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionmenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling)
        self.scaling_optionmenu.grid(row=8, column=0, padx=20, pady=(10, 20))
    
        self.entry_frame = ctk.CTkFrame(self)
        self.entry_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.entry_frame.grid_columnconfigure(1, weight=1)

        self.search_key_label = ctk.CTkLabel(self.entry_frame, text="Search Key:")
        self.search_key_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_search_key = ctk.CTkEntry(self.entry_frame)
        self.entry_search_key.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.count_page_label = ctk.CTkLabel(self.entry_frame, text="Count img:")
        self.count_page_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_count_page = ctk.CTkEntry(self.entry_frame)
        self.entry_count_page.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.path_save_label = ctk.CTkLabel(self.entry_frame, text="Save Path:")
        self.path_save_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_path_save_file = ctk.CTkEntry(self.entry_frame)
        self.entry_path_save_file.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    
        self.progressbar = ctk.CTkProgressBar(self)
        self.progressbar.grid(row=4, column=1, padx=20, pady=(0, 20), sticky="ew")

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.entry_path_save_file.delete(0, ctk.END)
            self.entry_path_save_file.insert(0, directory)

    def start_crawling(self):
        search_key = self.entry_search_key.get()
        count_page = int(self.entry_count_page.get())
        path_save_file = self.entry_path_save_file.get()

        if not search_key or not count_page or not path_save_file:
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        self.progressbar.start()

        threading.Thread(target=self.run_crawler, args=(search_key, count_page, path_save_file), daemon=True).start()

    def run_crawler(self, search_key, count_page, path_save_file):
        try:
            main.main(search_key, count_page, path_save_file)
            messagebox.showinfo("Success", f"Data has been saved to {path_save_file}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.progressbar.stop()

    def change_appearance_mode(self, new_mode):
        ctk.set_appearance_mode(new_mode)

    def change_scaling(self, new_scaling):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

if __name__ == "__main__":
    app = App()
    app.mainloop()
