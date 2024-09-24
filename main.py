import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests


class FormatterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("API Formatter")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f8")
        self.root.iconbitmap("main.ico")
        self.create_widgets()

    def create_widgets(self):

        tk.Label(self.root, text="Código:", bg="#f0f4f8", font=("Arial", 12)).grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        self.code_input = scrolledtext.ScrolledText(
            self.root,
            width=60,
            height=10,
            font=("Arial", 10),
            bg="#ffffff",
            bd=1,
            relief="flat",
        )
        self.code_input.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(self.root, text="Resultado:", bg="#f0f4f8", font=("Arial", 12)).grid(
            row=2, column=0, padx=10, pady=10, sticky="w"
        )
        self.result_output = scrolledtext.ScrolledText(
            self.root,
            width=60,
            height=10,
            font=("Arial", 10),
            bg="#ffffff",
            state="disabled",
            bd=1,
            relief="flat",
        )
        self.result_output.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.format_button = tk.Button(
            self.root,
            text="Formatar",
            command=self.format_code,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12),
            bd=0,
            padx=10,
            pady=5,
        )
        self.format_button.grid(row=4, column=0, padx=5, pady=5)

        self.copy_button = tk.Button(
            self.root,
            text="Copiar Resultado",
            command=self.copy_result,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12),
            bd=0,
            padx=10,
            pady=5,
        )
        self.copy_button.grid(row=4, column=1, padx=5, pady=5)

        self.reset_button = tk.Button(
            self.root,
            text="Limpar",
            command=self.reset,
            bg="#FF5722",
            fg="white",
            font=("Arial", 12),
            bd=0,
            padx=10,
            pady=5,
        )
        self.reset_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def format_code(self):
        code = self.code_input.get("1.0", tk.END).strip()
        result_type = "text"
        if not code:
            messagebox.showwarning(
                "Entrada Vazia", "Por favor, insira algum código para formatar."
            )
            return

        request_body = {
            "code": code,
            "resultType": result_type,
            "lineWidth": 100,
            "indentationLength": 2,
            "includeComments": True,
            "surroundBracesWithWs": False,
        }

        try:
            response = requests.post(
                "https://m-formatter.azurewebsites.net/api/v2", json=request_body
            )
            response_data = response.json()

            if response_data["success"]:
                self.result_output.config(state="normal")
                self.result_output.delete("1.0", tk.END)
                self.result_output.insert(tk.END, response_data["result"])
                self.result_output.config(state="disabled")
            else:
                messagebox.showerror(
                    "Erro", f"Erro ao formatar: {response_data['errors']}"
                )
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def copy_result(self):
        self.root.clipboard_clear()
        result = self.result_output.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_append(result)
            messagebox.showinfo(
                "Copiado", "Resultado copiado para a área de transferência!"
            )
        else:
            messagebox.showwarning("Sem Resultado", "Não há resultado para copiar.")

    def reset(self):
        self.code_input.delete("1.0", tk.END)
        self.result_output.config(state="normal")
        self.result_output.delete("1.0", tk.END)
        self.result_output.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = FormatterApp(root)
    root.mainloop()
