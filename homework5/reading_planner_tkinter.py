import tkinter as tk
from tkinter import messagebox, ttk


class ReadingPlanner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Читай по плану")
        self.minsize(380, 160)

        container = ttk.Frame(self, padding=12)
        container.pack(fill="both", expand=True)
        container.columnconfigure(1, weight=1)

        ttk.Label(container, text="Рассчитайте дневную норму чтения").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )

        ttk.Label(container, text="Осталось страниц").grid(
            row=1, column=0, sticky="w", padx=(0, 8)
        )
        self.pages_input = ttk.Entry(container)
        self.pages_input.grid(row=1, column=1, sticky="ew")

        ttk.Label(container, text="Срок чтения (в днях)").grid(
            row=2, column=0, sticky="w", padx=(0, 8), pady=6
        )
        self.deadline = ttk.Spinbox(container, from_=1, to=365, increment=1)
        self.deadline.set("7")
        self.deadline.grid(row=2, column=1, sticky="ew", pady=6)

        ttk.Button(container, text="Рассчитать", command=self.calculate).grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=(4, 8)
        )

        self.result = ttk.Label(container, wraplength=350)
        self.result.grid(row=4, column=0, columnspan=2, sticky="w")

        self.pages_input.bind("<Return>", self.calculate)
        self.deadline.bind("<Return>", self.calculate)
        self.pages_input.focus_set()

    def calculate(self, event=None):
        pages = self.read_positive_int(self.pages_input, "Осталось страниц")
        if pages is None:
            return

        days = self.read_positive_int(self.deadline, "Срок чтения (в днях)")
        if days is None:
            return

        pages_per_day = (pages + days - 1) // days
        self.result.configure(text=f"Дневная норма: {pages_per_day} стр. в день.")

    def read_positive_int(self, field, label):
        try:
            number = int(field.get().strip())
            if number <= 0:
                raise ValueError
        except ValueError:
            self.result.configure(text="")
            messagebox.showwarning(
                "Ошибка ввода",
                f"В поле «{label}» введите целое число больше нуля.",
                parent=self,
            )
            field.focus_set()
            field.selection_range(0, tk.END)
            return None

        return number


if __name__ == "__main__":
    ReadingPlanner().mainloop()
