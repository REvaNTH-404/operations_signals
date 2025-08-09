from tkinter import Tk, Label, Button, StringVar, OptionMenu, Frame, DoubleVar, Scale, HORIZONTAL
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.style.use('dark_background')  # Set matplotlib to dark mode

OPERATION_FORMULAS = {
    "Time Scaling": "x(at)",
    "Amplitude Scaling": "A·x(t)",
    "Time Shifting": "x(t - t₀)",
    "Time Reversal": "x(-t)",
    "Signal Addition": "x₁(t) + x₂(t)",
    "Signal Multiplication": "x₁(t) · x₂(t)"
}

DARK_BG = "#222831"
DARK_FG = "#eeeeee"
ACCENT = "#00adb5"
BTN_BG = "#393e46"
BTN_FG = "#eeeeee"

class SignalGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Signals and Systems App")
        self.master.configure(bg=DARK_BG)

        tk.Label(master, text="Signals and Systems", font=("Arial", 22, "bold"), bg=DARK_BG, fg=ACCENT).pack(padx=20, pady=10)
        tk.Label(master, text="Select a signal and operation, adjust parameters, then click 'Process Signal'.",
                 font=("Arial", 12), bg=DARK_BG, fg=DARK_FG).pack(pady=(0, 10))

        # Section: Signal Selection
        section1 = Frame(master, bg=DARK_BG)
        section1.pack(pady=5)
        tk.Label(section1, text="Signal Type:", font=("Arial", 14), bg=DARK_BG, fg=DARK_FG).grid(row=0, column=0, padx=5)
        self.signal_type = StringVar(master)
        self.signal_type.set("Sine")
        self.signal_options = ["Sine", "Square", "Sawtooth", "Step", "Impulse", "Ramp"]
        self.signal_menu = OptionMenu(section1, self.signal_type, *self.signal_options)
        self.signal_menu.config(font=("Arial", 13), bg=BTN_BG, fg=BTN_FG, width=10, highlightthickness=0)
        self.signal_menu.grid(row=0, column=1, padx=5)

        # Second signal selector (for addition/multiplication)
        tk.Label(section1, text="Signal 2 Type:", font=("Arial", 14), bg=DARK_BG, fg=DARK_FG).grid(row=0, column=4, padx=5)
        self.signal2_type = StringVar(master)
        self.signal2_type.set("Sine")
        self.signal2_menu = OptionMenu(section1, self.signal2_type, *self.signal_options)
        self.signal2_menu.config(font=("Arial", 13), bg=BTN_BG, fg=BTN_FG, width=10, highlightthickness=0)
        self.signal2_menu.grid(row=0, column=5, padx=5)
        # Hide second signal selector initially
        self.signal2_menu.grid_remove()
        section1.grid_columnconfigure(6, weight=1)

        # Section: Operation Selection
        tk.Label(section1, text="Operation:", font=("Arial", 14), bg=DARK_BG, fg=DARK_FG).grid(row=0, column=2, padx=5)
        self.operation_type = StringVar(master)
        self.operation_type.set("Time Scaling")
        self.operation_options = [
            "Time Scaling", "Amplitude Scaling", "Time Shifting",
            "Time Reversal", "Signal Addition", "Signal Multiplication"
        ]
        self.operation_menu = OptionMenu(section1, self.operation_type, *self.operation_options, command=self.update_parameter_controls)
        self.operation_menu.config(font=("Arial", 13), bg=BTN_BG, fg=BTN_FG, width=16, highlightthickness=0)
        self.operation_menu.grid(row=0, column=3, padx=5)

        # Time range controls
        time_frame = Frame(master, bg=DARK_BG)
        time_frame.pack(pady=2)
        Label(time_frame, text="Time Start:", font=("Arial", 12), bg=DARK_BG, fg=ACCENT).pack(side="left")
        self.time_start_var = DoubleVar(master, value=0.0)
        tk.Entry(time_frame, textvariable=self.time_start_var, width=6, font=("Arial", 12)).pack(side="left")
        Label(time_frame, text="End:", font=("Arial", 12), bg=DARK_BG, fg=ACCENT).pack(side="left")
        self.time_end_var = DoubleVar(master, value=1.0)
        tk.Entry(time_frame, textvariable=self.time_end_var, width=6, font=("Arial", 12)).pack(side="left")
        Label(time_frame, text="Step:", font=("Arial", 12), bg=DARK_BG, fg=ACCENT).pack(side="left")
        self.time_step_var = DoubleVar(master, value=0.01)
        tk.Entry(time_frame, textvariable=self.time_step_var, width=6, font=("Arial", 12)).pack(side="left")

        # Parameters for Signal 1
        self.param1_frame = Frame(master, bg=DARK_BG)
        self.param1_frame.pack(pady=2)
        Label(self.param1_frame, text="Signal 1 Amplitude:", font=("Arial", 12), bg=DARK_BG, fg=ACCENT).pack(side="left")
        self.amp1_var = DoubleVar(master, value=1.0)
        Scale(self.param1_frame, from_=0.1, to=5.0, resolution=0.1, orient=HORIZONTAL, variable=self.amp1_var, length=120, bg=DARK_BG, fg=ACCENT, troughcolor=BTN_BG, highlightthickness=0).pack(side="left")
        Label(self.param1_frame, text="Frequency:", font=("Arial", 12), bg=DARK_BG, fg=ACCENT).pack(side="left")
        self.freq1_var = DoubleVar(master, value=5.0)
        Scale(self.param1_frame, from_=1.0, to=20.0, resolution=1.0, orient=HORIZONTAL, variable=self.freq1_var, length=120, bg=DARK_BG, fg=ACCENT, troughcolor=BTN_BG, highlightthickness=0).pack(side="left")
        Label(self.param1_frame, text="Phase:", font=("Arial", 12), bg=DARK_BG, fg=ACCENT).pack(side="left")
        self.phase1_var = DoubleVar(master, value=0.0)
        Scale(self.param1_frame, from_=-np.pi, to=np.pi, resolution=0.1, orient=HORIZONTAL, variable=self.phase1_var, length=120, bg=DARK_BG, fg=ACCENT, troughcolor=BTN_BG, highlightthickness=0).pack(side="left")

        # Parameters for Signal 2
        self.param2_frame = Frame(master, bg=DARK_BG)
        self.param2_frame.pack(pady=2)
        Label(self.param2_frame, text="Signal 2 Amplitude:", font=("Arial", 12), bg=DARK_BG, fg=ACCENT).pack(side="left")
        self.amp2_var = DoubleVar(master, value=1.0)
        Scale(self.param2_frame, from_=0.1, to=5.0, resolution=0.1, orient=HORIZONTAL, variable=self.amp2_var, length=120, bg=DARK_BG, fg=ACCENT, troughcolor=BTN_BG, highlightthickness=0).pack(side="left")
        Label(self.param2_frame, text="Frequency:", font=("Arial", 12), bg=DARK_BG, fg=ACCENT).pack(side="left")
        self.freq2_var = DoubleVar(master, value=5.0)
        Scale(self.param2_frame, from_=1.0, to=20.0, resolution=1.0, orient=HORIZONTAL, variable=self.freq2_var, length=120, bg=DARK_BG, fg=ACCENT, troughcolor=BTN_BG, highlightthickness=0).pack(side="left")
        Label(self.param2_frame, text="Phase:", font=("Arial", 12), bg=DARK_BG, fg=ACCENT).pack(side="left")
        self.phase2_var = DoubleVar(master, value=0.0)
        Scale(self.param2_frame, from_=-np.pi, to=np.pi, resolution=0.1, orient=HORIZONTAL, variable=self.phase2_var, length=120, bg=DARK_BG, fg=ACCENT, troughcolor=BTN_BG, highlightthickness=0).pack(side="left")
        self.param2_frame.pack_forget()

        # Parameter controls (Entry box instead of slider)
        self.param_frame = Frame(master, bg=DARK_BG)
        self.param_frame.pack(pady=5)
        self.param_label = Label(self.param_frame, text="", font=("Arial", 13), bg=DARK_BG, fg=ACCENT)
        self.param_label.pack(side="left")
        self.param_var = DoubleVar(master)
        self.param_entry = tk.Entry(self.param_frame, textvariable=self.param_var, width=8, font=("Arial", 13))
        self.param_entry.pack(side="left")
        self.param_frame.pack_forget()

        # Formula display
        self.formula_label = Label(master, text="", font=("Arial", 15, "italic"), fg=ACCENT, bg=DARK_BG)
        self.formula_label.pack(pady=5)

        # Process Button
        self.process_button = Button(master, text="Process Signal", font=("Arial", 16, "bold"),
                                    command=self.process_signal, bg=ACCENT, fg=DARK_BG, height=2, width=20, bd=0)
        self.process_button.pack(pady=15)

        self.result_label = Label(master, text="", font=("Arial", 13), fg=DARK_FG, bg=DARK_BG)
        self.result_label.pack(pady=5)

        # Frame for matplotlib figure
        self.plot_frame = Frame(master, bg=DARK_BG)
        self.plot_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.figure, self.axs = plt.subplots(1, 2, figsize=(13, 5))  # Larger plot
        self.figure.patch.set_facecolor(DARK_BG)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.update_parameter_controls(self.operation_type.get())

    def update_parameter_controls(self, operation):
        # Show/hide parameter controls based on operation
        if operation == "Time Scaling":
            self.param_label.config(text="Scaling factor (a):")
            self.param_var.set(1.0)
            self.param_frame.pack(pady=5)
            self.param2_frame.pack_forget()
        elif operation == "Amplitude Scaling":
            self.param_label.config(text="Amplitude (A):")
            self.param_var.set(2.0)
            self.param_frame.pack(pady=5)
            self.param2_frame.pack_forget()
        elif operation == "Time Shifting":
            self.param_label.config(text="Shift (t₀):")
            self.param_var.set(0.1)
            self.param_frame.pack(pady=5)
            self.param2_frame.pack_forget()
        else:
            self.param_frame.pack_forget()
            self.param2_frame.pack_forget()
        # Show/hide second signal selector for addition/multiplication
        if operation in ["Signal Addition", "Signal Multiplication"]:
            self.signal2_menu.grid()
            self.param2_frame.pack(pady=2)
        else:
            self.signal2_menu.grid_remove()
            self.param2_frame.pack_forget()
        # Update formula
        self.formula_label.config(text=f"Formula: {OPERATION_FORMULAS.get(operation, '')}")

    def process_signal(self):
        signal1 = self.signal_type.get()
        signal2 = self.signal2_type.get()
        operation = self.operation_type.get()
        self.result_label.config(text=f"Processing '{signal1}' and '{signal2}' with '{operation}'")

        t = np.linspace(0, 1, 500)
        def get_signal(sig_type):
            if sig_type == "Sine":
                return np.sin(2 * np.pi * 5 * t)
            elif sig_type == "Square":
                return np.sign(np.sin(2 * np.pi * 5 * t))
            elif sig_type == "Sawtooth":
                return 2 * (t - np.floor(t + 0.5))
            elif sig_type == "Step":
                return np.heaviside(t - 0.5, 1)
            elif sig_type == "Impulse":
                arr = np.zeros_like(t)
                arr[len(t)//2] = 1
                return arr
            elif sig_type == "Ramp":
                return t
            else:
                return np.zeros_like(t)

        original_signal = get_signal(signal1)
        second_signal = get_signal(signal2)

        # Operations with parameters
        if operation == "Time Scaling":
            a = self.param_var.get()
            processed_signal = np.sin(2 * np.pi * 5 * a * t) if signal1 == "Sine" else np.interp(t, t * a, original_signal, left=0, right=0)
            self.plot_signals(t, original_signal, processed_signal)
        elif operation == "Amplitude Scaling":
            A = self.param_var.get()
            processed_signal = A * original_signal
            self.plot_signals(t, original_signal, processed_signal)
        elif operation == "Time Shifting":
            t0 = self.param_var.get()
            processed_signal = np.sin(2 * np.pi * 5 * (t - t0)) if signal1 == "Sine" else np.interp(t, t - t0, original_signal, left=0, right=0)
            self.plot_signals(t, original_signal, processed_signal)
        elif operation == "Time Reversal":
            processed_signal = original_signal[::-1]
            self.plot_signals(t, original_signal, processed_signal)
        elif operation == "Signal Addition":
            processed_signal = original_signal + second_signal
            self.show_output_page(t, original_signal, second_signal, processed_signal, operation)
        elif operation == "Signal Multiplication":
            processed_signal = original_signal * second_signal
            self.show_output_page(t, original_signal, second_signal, processed_signal, operation)
        else:
            processed_signal = original_signal
            self.plot_signals(t, original_signal, processed_signal)

    def show_output_page(self, t, signal1, signal2, result, operation):
        output_win = tk.Toplevel(self.master)
        output_win.title(f"{operation} Output")
        output_win.configure(bg=DARK_BG)
        fig, axs = plt.subplots(1, 3, figsize=(18, 5))
        fig.patch.set_facecolor(DARK_BG)
        titles = ["Signal 1", "Signal 2", "Result"]
        datas = [signal1, signal2, result]
        colors = ["#00fff5", "#f5e100", "#ff2e63"]
        for i in range(3):
            axs[i].set_facecolor(DARK_BG)
            axs[i].grid(True, linestyle='--', alpha=0.5, color=BTN_BG)
            axs[i].set_xlabel(f"Time (s)", color=ACCENT, fontsize=13)
            axs[i].set_ylabel("Amplitude", color=ACCENT, fontsize=13)
            axs[i].tick_params(axis='x', color=DARK_FG)
            axs[i].tick_params(axis='y', color=DARK_FG)
            axs[i].set_title(titles[i], fontsize=15, color=ACCENT)
            axs[i].plot(t, datas[i], color=colors[i], linewidth=2)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=output_win)
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_signals(self, t, original_signal, processed_signal):
        for ax in self.axs:
            ax.clear()
            ax.set_facecolor("#222831")
            ax.grid(True, linestyle='--', alpha=0.5, color="#393e46")
            ax.set_xlabel("Time (s)", color=ACCENT, fontsize=13)
            ax.set_ylabel("Amplitude", color=ACCENT, fontsize=13)
            ax.tick_params(axis='x', colors=DARK_FG)
            ax.tick_params(axis='y', colors=DARK_FG)
        self.axs[0].set_title("Original Signal", fontsize=15, color=ACCENT)
        self.axs[0].plot(t, original_signal, color="#00fff5", label="Original", linewidth=2)
        self.axs[0].legend(facecolor=BTN_BG, edgecolor=ACCENT, fontsize=12)
        self.axs[1].set_title("Processed Signal", fontsize=15, color=ACCENT)
        self.axs[1].plot(t, processed_signal, color="#ff2e63", label="Processed", linewidth=2)
        self.axs[1].legend(facecolor=BTN_BG, edgecolor=ACCENT, fontsize=12)
        self.figure.tight_layout()
        self.canvas.draw()

    def run(self):
        self.master.mainloop()
