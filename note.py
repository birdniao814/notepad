
import tkinter as tk
from tkinter import filedialog

save_file_flag = False
change_flag = False
current_file_path = None  # 当前文件路径，初始为None


def on_modify(event):  # 定义文本修改事件处理函数
    global change_flag
    if text_area.edit_modified():  # 检查文本区域是否被修改
        change_flag = True  # 如果被修改，设置change_flag为True
        text_area.edit_modified(False)  # 重置编辑状态


def save_file(event=None):  # 定义保存文件函数，event参数用于绑定快捷键
    global current_file_path, save_file_flag, change_flag
    if (
        not current_file_path
    ):  # 如果当前文件路径为None，说明是新文件，需要弹出保存对话框
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )  # 弹出保存文件对话框，默认扩展名为.txt
        if file_path:
            current_file_path = file_path
        else:
            save_file_flag = False  # 用户取消保存，设置保存标志为False
            return

    if current_file_path:
        with open(current_file_path, "w", encoding="utf-8") as file:
            file.write(text_area.get("1.0", "end-1c"))

        save_file_flag = True

        change_flag = False  # 保存后重置change_flag为False
        text_area.edit_modified(False)  # 重置编辑状态


def save_on_exit(event=None):  # 定义关闭窗口时的保存函数，event参数用于绑定快捷键
    if not change_flag:  # 如果没有内容修改，直接关闭窗口
        root.destroy()
        return

    result = tk.messagebox.askyesnocancel(
        "提示", "未保存内容,是否保存？"
    )  # 弹出保存文件提示框
    if result is True:
        save_file()  # 如果用户选择保存，调用保存函数
        if save_file_flag:  # 如果保存成功，关闭窗口
            root.destroy()  # 关闭窗口
            return
    elif result is False:
        root.destroy()  # 如果用户选择不保存，直接关闭窗口
    else:
        pass  # 如果用户选择取消，什么也不做


def open_file(event=None):  # 定义打开文件函数，event参数用于绑定快捷键
    global change_flag, save_file_flag

    if change_flag:
        result = tk.messagebox.askyesnocancel(
            "提示", "未保存内容,是否保存？"
        )  # 弹出保存文件提示框
        if result is True:
            save_file()
            if not save_file_flag:
                return
        elif result is False:
            pass
        else:
            return

    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

            text_area.delete("1.0", tk.END)  # 清空文本区域
            text_area.insert(tk.END, content)

            change_flag = False
            text_area.edit_modified(False)  # 重置编辑状态


def new_file(event=None):
    global change_flag, save_file_flag
    if change_flag:
        result = tk.messagebox.askyesnocancel(
            "提示", "未保存内容,是否保存？"
        )  # 弹出保存文件提示框
        if result is True:
            save_file()
            if not save_file_flag:
                return
        elif result is False:
            pass
        else:
            return

    text_area.delete("1.0", tk.END)  # 清空文本区域
    change_flag = False
    text_area.edit_modified(False)  # 重置编辑状态


# 窗口布局
root = tk.Tk()
root.title("简易记事本")  # 设置窗口标题
root.geometry("600x400")  # 设置窗口大小为600x400
root.iconbitmap("note.ico")

# 菜单栏
menu_bar = tk.Menu(root)  # 创建菜单栏

file_menu = tk.Menu(menu_bar, tearoff=0)  # 创建文件菜单
edit_menu = tk.Menu(menu_bar, tearoff=0)  # 创建编辑菜单


menu_bar.add_cascade(label="文件", menu=file_menu)  # 将文件菜单添加到菜单栏
menu_bar.add_cascade(label="编辑", menu=edit_menu)  # 添加编辑菜单


file_menu.add_command(label="保存文件      Ctrl+S", command=save_file)
file_menu.add_command(label="打开文件      Ctrl+O", command=open_file)
file_menu.add_command(label="新建文件      Ctrl+N", command=new_file)

edit_menu.add_command(
    label="撤销          Ctrl+Z", command=lambda: text_area.event_generate("<<Undo>>")
)  # 撤销操作
edit_menu.add_command(
    label="重做          Ctrl+Y", command=lambda: text_area.event_generate("<<Redo>>")
)  # 重做操作
edit_menu.add_command(
    label="剪切          Ctrl+X", command=lambda: text_area.event_generate("<<Cut>>")
)  # 剪切操作
edit_menu.add_command(
    label="复制          Ctrl+C", command=lambda: text_area.event_generate("<<Copy>>")
)  # 复制操作
edit_menu.add_command(
    label="粘贴          Ctrl+V", command=lambda: text_area.event_generate("<<Paste>>")
)  # 粘贴操作

root.config(menu=menu_bar)  # 将菜单栏添加到窗口

# 滚动条
scroll_bar = tk.Scrollbar(root)  # 创建滚动条
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)  # 将滚动条放置在右侧并填充垂直方向

# 文本输入
text_area = tk.Text(
    root, undo=True, cursor="xterm", font=("宋体", 20), yscrollcommand=scroll_bar.set
)  # 设置字体为宋体，字号为20
text_area.pack(fill=tk.BOTH, expand=True)  # 填充整个窗口

scroll_bar.config(command=text_area.yview)  # 配置滚动条与文本区域的联动

# 快捷键绑定
root.bind("<Control-s>", save_file)  # 绑定Ctrl+S快捷键保存文件
root.bind("<Control-o>", open_file)  # 绑定Ctrl+O快捷键打开文件
root.bind("<Control-n>", new_file)  # 绑定Ctrl+N快捷键新建文件
root.bind("<Control-w>", save_on_exit)  # 绑定Ctrl+W快捷键关闭窗口
text_area.bind("<<Modified>>", on_modify)  # 绑定文本修改事件


# 自动保存功能
root.protocol("WM_DELETE_WINDOW", save_on_exit)  # 绑定窗口关闭事件，调用保存函数


root.mainloop()
