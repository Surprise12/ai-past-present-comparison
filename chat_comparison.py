import threading
import tkinter as tk
from tkinter import scrolledtext

from eliza import get_eliza_response
from LLM import get_llm_response

class ChatComparisonGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Past vs Present AI - ELIZA vs LLM")
        self.root.geometry("1200x700")
        self.root.configure(bg="#0f172a")
        self.build_ui()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="AI Comparison Lab: ELIZA vs LLM",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#0f172a"
        )
        title.pack(pady=(15, 5))

        subtitle = tk.Label(
            self.root,
            text="Compare rule-based AI and modern generative AI side by side",
            font=("Arial", 11),
            fg="#cbd5e1",
            bg="#0f172a"
        )
        subtitle.pack(pady=(0, 15))

        top_frame = tk.Frame(self.root, bg="#0f172a")
        top_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.eliza_frame = tk.LabelFrame(
            top_frame, 
            text=" ELIZA - Past AI (Rule-Based) ",
            font=("Arial", 12, "bold"),
            bg="#1e293b",
            fg="white"
        )
        self.eliza_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.eliza_chat = scrolledtext.ScrolledText(
            self.eliza_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="black",
            fg="lightgreen",
            height=25
        )
        self.eliza_chat.pack(fill="both", expand=True, padx=10, pady=10)
        self.eliza_chat.insert(tk.END, "="*50 + "\n")
        self.eliza_chat.insert(tk.END, "ELIZA READY\n")
        self.eliza_chat.insert(tk.END, "="*50 + "\n\n")
        self.eliza_chat.config(state="disabled")

        self.llm_frame = tk.LabelFrame(
            top_frame,
            text=" LLM - Present AI (Neural Network) ",
            font=("Arial", 12, "bold"),
            bg="#1e293b",
            fg="white"
        )
        self.llm_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.llm_chat = scrolledtext.ScrolledText(
            self.llm_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="black",
            fg="lightblue",
            height=25
        )
        self.llm_chat.pack(fill="both", expand=True, padx=10, pady=10)
        self.llm_chat.insert(tk.END, "="*50 + "\n")
        self.llm_chat.insert(tk.END, "LLM READY\n")
        self.llm_chat.insert(tk.END, "="*50 + "\n\n")
        self.llm_chat.config(state="disabled")

        bottom_frame = tk.Frame(self.root, bg="#0f172a")
        bottom_frame.pack(fill="x", padx=20, pady=(0, 20))

        input_label = tk.Label(
            bottom_frame,
            text="Enter your message:",
            font=("Arial", 10),
            fg="white",
            bg="#0f172a"
        )
        input_label.pack(anchor="w", pady=(0, 5))

        self.input_box = tk.Entry(
            bottom_frame,
            font=("Arial", 12),
            bg="white",
            fg="black"
        )
        self.input_box.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.input_box.bind("<Return>", self.send_message)
        self.input_box.focus()

        send_btn = tk.Button(
            bottom_frame,
            text="SEND",
            font=("Arial", 11, "bold"),
            bg="blue",
            fg="white",
            padx=20,
            pady=5,
            command=self.send_message
        )
        send_btn.pack(side="left", padx=(0, 10))

        clear_btn = tk.Button(
            bottom_frame,
            text="CLEAR",
            font=("Arial", 11, "bold"),
            bg="gray",
            fg="white",
            padx=20,
            pady=5,
            command=self.clear_chats
        )
        clear_btn.pack(side="left")

    def append_text(self, widget, text, color=None):
        widget.config(state="normal")
        widget.insert(tk.END, text + "\n")
        if color:
            widget.tag_add(color, "end-2c", "end-1c")
            widget.tag_config(color, foreground=color)
        widget.see(tk.END)
        widget.config(state="disabled")

    def send_message(self, event=None):
        user_text = self.input_box.get().strip()
        if not user_text:
            return

        self.input_box.delete(0, tk.END)

        self.append_text(self.eliza_chat, f"\n[You] {user_text}", "yellow")
        self.append_text(self.llm_chat, f"\n[You] {user_text}", "yellow")

        try:
            eliza_reply = get_eliza_response(user_text)
            self.append_text(self.eliza_chat, f"[ELIZA] {eliza_reply}", "lightgreen")
        except Exception as e:
            self.append_text(self.eliza_chat, f"[ELIZA] Error: {e}", "red")

        self.append_text(self.llm_chat, "[LLM] Thinking...", "orange")

        threading.Thread(
            target=self.get_llm_in_background,
            args=(user_text,),
            daemon=True
        ).start()

    def get_llm_in_background(self, user_text):
        try:
            llm_reply = get_llm_response(user_text)
        except Exception as e:
            llm_reply = f"Error: {e}"

        self.root.after(0, self.replace_last_llm_message, llm_reply)

    def replace_last_llm_message(self, new_text):
        self.llm_chat.config(state="normal")
        content = self.llm_chat.get("1.0", tk.END)
        lines = content.split('\n')
        
        for i in range(len(lines)-1, -1, -1):
            if "[LLM] Thinking..." in lines[i]:
                lines[i] = f"[LLM] {new_text}"
                break
        
        self.llm_chat.delete("1.0", tk.END)
        self.llm_chat.insert(tk.END, '\n'.join(lines))
        self.llm_chat.see(tk.END)
        self.llm_chat.config(state="disabled")

    def clear_chats(self):
        for widget in [self.eliza_chat, self.llm_chat]:
            widget.config(state="normal")
            widget.delete("1.0", tk.END)
            widget.insert(tk.END, "="*50 + "\n")
            if widget == self.eliza_chat:
                widget.insert(tk.END, "ELIZA READY\n")
            else:
                widget.insert(tk.END, "LLM READY\n")
            widget.insert(tk.END, "="*50 + "\n\n")
            widget.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatComparisonGUI(root)
    root.mainloop()