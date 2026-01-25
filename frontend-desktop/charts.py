from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class MatplotlibCanvas(FigureCanvas):
    """Matplotlib canvas styled for Dark Slate UI."""

    def __init__(self, parent=None, chart_type="bar"):
        # Dark slate background #1e293b to match card background
        self.figure = Figure(figsize=(7, 4), dpi=100)
        self.figure.patch.set_facecolor("#1e293b")
        self.axes = self.figure.add_subplot(111)
        self.chart_type = chart_type

        super().__init__(self.figure)
        self.setParent(parent)
        
        self.setStyleSheet("background-color: transparent;")

        # Adjusted margins for visibility (Left for Y-axis label, Bottom for rotated X-axis)
        self.figure.subplots_adjust(left=0.18, right=0.92, top=0.88, bottom=0.32)

    # ================= Common =================
    def _base_style(self):
        self.axes.set_facecolor("#1e293b")
        
        for spine in ["top", "right"]:
            self.axes.spines[spine].set_visible(False)

        self.axes.spines["left"].set_color("#475569")
        self.axes.spines["bottom"].set_color("#475569")
        self.axes.spines["left"].set_linewidth(1.2)
        self.axes.spines["bottom"].set_linewidth(1.2)

        # Reduced font size for better fit
        self.axes.tick_params(axis="both", labelsize=9, colors="#cbd5e1", pad=4)
        self.axes.grid(axis="y", linestyle="--", linewidth=0.8, alpha=0.1, color="#ffffff")
        self.axes.set_axisbelow(True)

    # ================= Distribution =================
    def plot_equipment_distribution(self, distribution):
        self.axes.clear()
        self._base_style()

        if not distribution:
            self.axes.text(
                0.5,
                0.5,
                "No data available",
                ha="center",
                va="center",
                fontsize=11,
                color="#64748b",
                transform=self.axes.transAxes,
            )
            self.draw()
            return

        labels = list(distribution.keys())
        values = list(distribution.values())
        # High contrast neon palette
        colors = [
            "#818cf8", # Indigo 400
            "#a78bfa", # Violet 400
            "#f472b6", # Pink 400
            "#34d399", # Emerald 400
            "#60a5fa", # Blue 400
            "#fbbf24", # Amber 400
            "#f87171", # Red 400
        ]

        if self.chart_type == "bar":
            self._bar(labels, values, colors)
        elif self.chart_type == "pie":
            self._pie(labels, values, colors)
        elif self.chart_type == "doughnut":
            self._doughnut(labels, values, colors)
        elif self.chart_type == "line":
            self._line(labels, values, colors)

        self.draw()

    # ================= Bar =================
    def _bar(self, labels, values, colors):
        bars = self.axes.bar(
            labels,
            values,
            color=colors[: len(labels)],
            edgecolor="#1e293b",
            linewidth=1.0,
        )

        for bar in bars:
            h = bar.get_height()
            self.axes.text(
                bar.get_x() + bar.get_width() / 2,
                h + 0.1,
                f"{int(h)}",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
                color="#f1f5f9",
            )

        self.axes.set_ylabel("Count", fontsize=10, fontweight="bold", color="#f1f5f9")
        
        # Rotate x labels with better alignment
        self.figure.autofmt_xdate(rotation=30, ha="right")

    # ================= Pie =================
    def _pie(self, labels, values, colors):
        wedges, texts, autotexts = self.axes.pie(
            values,
            labels=labels,
            colors=colors[: len(labels)],
            autopct="%1.0f%%",
            startangle=90,
            textprops={"fontsize": 9, "color": "#f1f5f9"},
            wedgeprops={"edgecolor": "#1e293b", "linewidth": 2},
            pctdistance=0.75,
            labeldistance=1.1
        )
        # Ensure labels are visible
        for t in texts:
            t.set_color("#f1f5f9")
        for at in autotexts:
            at.set_color("#1e293b")
            at.set_fontweight("bold")

    # ================= Doughnut =================
    def _doughnut(self, labels, values, colors):
        wedges, texts, autotexts = self.axes.pie(
            values,
            labels=labels,
            colors=colors[: len(labels)],
            autopct="%1.0f%%",
            startangle=90,
            textprops={"fontsize": 9, "color": "#f1f5f9"},
            wedgeprops={
                "width": 0.5,
                "edgecolor": "#1e293b",
                "linewidth": 2,
            },
            pctdistance=0.75,
            labeldistance=1.1
        )
        for t in texts:
            t.set_color("#f1f5f9")
        for at in autotexts:
            at.set_color("#1e293b")
            at.set_fontweight("bold")

    # ================= Line =================
    def _line(self, labels, values, colors):
        x = np.arange(len(labels))

        self.axes.plot(
            x,
            values,
            marker="o",
            linewidth=2.5,
            color=colors[0],
            markerfacecolor="#1e293b",
            markeredgecolor=colors[0],
            markeredgewidth=2,
        )

        for i, val in enumerate(values):
            self.axes.text(
                i,
                val + 0.2,
                f"{int(val)}",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
                color="#f1f5f9",
            )

        self.axes.set_xticks(x)
        self.axes.set_xticklabels(labels, rotation=30, ha="right")
        self.axes.set_ylabel("Count", fontsize=10, fontweight="bold", color="#f1f5f9")

    # ================= Upload Trends =================
    def plot_upload_trends(self, uploads):
        self.axes.clear()
        self._base_style()

        if not uploads:
            self.axes.text(
                0.5,
                0.5,
                "No upload history",
                ha="center",
                va="center",
                fontsize=11,
                color="#64748b",
                transform=self.axes.transAxes,
            )
            self.draw()
            return

        uploads = sorted(uploads, key=lambda x: x.get("uploaded_at", ""))
        x = np.arange(len(uploads))
        labels = [f"#{i + 1}" for i in range(len(uploads))]

        flow = [u.get("avg_flowrate", 0) for u in uploads]
        press = [u.get("avg_pressure", 0) for u in uploads]
        temp = [u.get("avg_temperature", 0) for u in uploads]

        ax2 = self.axes.twinx()
        ax2.spines["top"].set_visible(False)
        ax2.spines["left"].set_visible(False)
        ax2.spines["bottom"].set_visible(False)
        ax2.spines["right"].set_color("#475569") 
        ax2.spines["right"].set_linewidth(1.2)
        ax2.tick_params(axis="y", colors="#cbd5e1", labelsize=9)

        # Plot Lines
        self.axes.plot(x, flow, marker="o", linewidth=2.5, label="Flowrate", color="#818cf8")
        self.axes.plot(x, temp, marker="^", linewidth=2.5, label="Temperature", color="#f472b6")
        ax2.plot(x, press, marker="s", linewidth=2.5, label="Pressure", color="#34d399")

        self.axes.set_xticks(x)
        self.axes.set_xticklabels(labels)
        self.axes.set_xlabel("Upload Sequence", fontsize=10, fontweight="bold", color="#f1f5f9")

        self.axes.set_ylabel("Flowrate / Temperature", fontsize=10, fontweight="bold", color="#f1f5f9")
        ax2.set_ylabel("Pressure", fontsize=10, fontweight="bold", color="#f1f5f9")

        # Legend
        lines, labels_ = self.axes.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        leg = self.axes.legend(
            lines + lines2,
            labels_ + labels2,
            loc="upper left",
            fontsize=9,
            frameon=True,
            facecolor="#1e293b",
            edgecolor="#334155",
            labelcolor="#f1f5f9",
            fancybox=True
        )

        self.draw()
