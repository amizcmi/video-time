import tkinter as tk
from tkinter import ttk
import os
from tkinter import messagebox, filedialog
import cv2

# 在文件开头添加
VERSION = "0.3"

class ModernButton(ttk.Label):
    """现代风格按钮"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        
    def on_enter(self, event):
        """鼠标悬停效果"""
        self.configure(style='Hover.Modern.TLabel')
        
    def on_leave(self, event):
        """鼠标离开效果"""
        self.configure(style='Modern.TLabel')

class VideoDurationApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"视频时长查看器 v{VERSION}")
        
        # 设置窗口大小和位置
        window_width = 600
        window_height = 500
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 设置主题和样式
        self.setup_styles()
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, style='Main.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建标题
        title_label = ttk.Label(
            self.main_frame,
            text="视频时长查看器",
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 20))
        
        # 创建按钮区域
        self.button_area = ModernButton(
            self.main_frame,
            text="点击选择视频文件或文件夹",
            padding="20",
            cursor="hand2",
            style='Modern.TLabel',
            anchor="center"
        )
        self.button_area.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # 创建结果显示区域
        self.create_result_area()
        
        # 创建统计标签
        self.stats_label = ttk.Label(
            self.main_frame,
            text="总计: 0个文件, 总时长: 00:00:00",
            style='Stats.TLabel'
        )
        self.stats_label.pack(pady=10)
        
        # 绑定点击事件
        self.button_area.bind('<Button-1>', self.on_click)

    def setup_styles(self):
        """设置自定义样式"""
        style = ttk.Style()
        
        # 主框架样式
        style.configure('Main.TFrame', background='#ffffff')
        
        # 标题样式
        style.configure('Title.TLabel',
            font=('Microsoft YaHei UI', 16, 'bold'),
            background='#ffffff',
            foreground='#1a1a1a'
        )
        
        # 现代按钮样式
        style.configure('Modern.TLabel',
            font=('Microsoft YaHei UI', 11),
            background='#E8DEF8',
            foreground='#1D192B',
            relief='flat',
            borderwidth=0,
            padding=15,
            anchor="center"
        )
        
        # 按钮悬停样式
        style.configure('Hover.Modern.TLabel',
            background='#D0BCFF',
            font=('Microsoft YaHei UI', 11),
            foreground='#1D192B',
            padding=15,
            anchor="center"
        )
        
        # 统计标签样式
        style.configure('Stats.TLabel',
            font=('Microsoft YaHei UI', 10),
            background='#ffffff',
            foreground='#666666'
        )
        
        # 文本区域样式
        style.configure('Result.TFrame',
            background='#ffffff',
            relief='flat'
        )

    def create_result_area(self):
        """创建结果显示区域"""
        result_frame = ttk.Frame(self.main_frame, style='Result.TFrame')
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # 创建文本框和滚动条
        self.result_text = tk.Text(
            result_frame,
            height=12,
            font=('Microsoft YaHei UI', 10),
            wrap=tk.WORD,
            borderwidth=1,
            relief="solid",
            background='#ffffff',
            foreground='#1a1a1a'
        )
        
        scrollbar = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=self.result_text.yview
        )
        
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        # 使用grid布局以实现更好的响应式效果
        result_frame.grid_columnconfigure(0, weight=1)
        result_frame.grid_rowconfigure(0, weight=1)
        
        self.result_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # 设置文本框标签和内边距
        self.result_text.configure(padx=10, pady=10)

    def on_click(self, event):
        """处理点击事件"""
        choice = messagebox.askyesno(
            "选择类型",
            "选择文件夹还是文件？\n\n是 - 选择文件夹\n否 - 选择文件",
            icon='question'
        )
        
        if choice:  # 选择文件夹
            folder = filedialog.askdirectory(title="选择文件夹")
            if folder:
                self.process_files([folder])
        else:  # 选择文件
            files = filedialog.askopenfilenames(
                title="选择视频文件",
                filetypes=[
                    ("视频文件", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv"),
                    ("所有文件", "*.*")
                ]
            )
            if files:
                self.process_files(files)

    def get_video_duration(self, video_path):
        """使用 OpenCV 获取视频时长"""
        try:
            video = cv2.VideoCapture(video_path)
            if not video.isOpened():
                return None
            
            total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = video.get(cv2.CAP_PROP_FPS)
            duration = total_frames / fps
            
            video.release()
            return duration
        except Exception:
            return None

    def format_duration(self, seconds):
        """将秒数转换为时:分:秒格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def process_video_file(self, file_path):
        """处理单个视频文件"""
        valid_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')
        if not file_path.lower().endswith(valid_extensions):
            return None
        
        duration = self.get_video_duration(file_path)
        return duration

    def process_path(self, path):
        """处理文件或文件夹路径"""
        if os.path.isfile(path):
            return [(path, self.process_video_file(path))]
        
        results = []
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                duration = self.process_video_file(file_path)
                if duration is not None:
                    results.append((file_path, duration))
        return results

    def process_files(self, paths):
        """处理文件列表"""
        self.result_text.delete(1.0, tk.END)
        total_duration = 0
        total_files = 0
        
        for path in paths:
            if not os.path.exists(path):
                continue
            
            results = self.process_path(path)
            for file_path, duration in results:
                if duration is not None:
                    total_duration += duration
                    total_files += 1
                    filename = os.path.basename(file_path)
                    formatted_duration = self.format_duration(duration)
                    self.result_text.insert(tk.END, 
                        f"文件: {filename}\n时长: {formatted_duration}\n\n")
        
        formatted_total = self.format_duration(total_duration)
        self.stats_label.configure(
            text=f"总计: {total_files}个文件, 总时长: {formatted_total}"
        )
        
        if total_files == 0:
            self.result_text.insert(tk.END, "未找到有效的视频文件\n")

def main():
    root = tk.Tk()
    # 设置窗口样式
    root.configure(bg='#ffffff')
    # 设置窗口图标（如果有的话）
    try:
        root.iconbitmap('vticon.ico')
    except:
        pass
    
    app = VideoDurationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 