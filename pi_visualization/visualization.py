"""Visualizacion y animacion de la convergencia de metodos para calcular pi."""

from __future__ import annotations

from decimal import Decimal

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

from methods import PiMethod
from utils import format_decimal


class PiVisualizationApp:
    """App interactiva con dos vistas y tabla dinamica."""

    def __init__(
        self,
        methods: list[PiMethod],
        pi_real: Decimal,
        max_iterations: int,
        animation_interval_ms: int,
        use_log_scale_y_error: bool,
        min_plot_error: Decimal,
    ) -> None:
        self.methods = methods
        self.pi_real = pi_real
        self.max_iterations = max_iterations
        self.animation_interval_ms = animation_interval_ms
        self.use_log_scale_y_error = use_log_scale_y_error
        self.min_plot_error = min_plot_error

        self.mode = "error"
        self.current_iteration = 0
        self.is_running = False

        self.iterations: list[int] = []
        self.pi_history: dict[str, list[float]] = {method.name: [] for method in methods}
        self.error_history: dict[str, list[float]] = {method.name: [] for method in methods}

        self.figure, self.main_ax = plt.subplots(figsize=(13, 7))
        self.figure.canvas.manager.set_window_title("Convergencia de pi")
        plt.subplots_adjust(left=0.08, right=0.67, bottom=0.2, top=0.9)

        self.table_ax = self.figure.add_axes([0.70, 0.25, 0.28, 0.60])
        self.table_ax.axis("off")

        self.error_button_ax = self.figure.add_axes([0.12, 0.06, 0.16, 0.08])
        self.approx_button_ax = self.figure.add_axes([0.30, 0.06, 0.16, 0.08])
        self.play_button_ax = self.figure.add_axes([0.48, 0.06, 0.16, 0.08])

        self.error_button = Button(self.error_button_ax, "Ver Error")
        self.approx_button = Button(self.approx_button_ax, "Ver Aproximacion")
        self.play_button = Button(self.play_button_ax, "Play")

        self.error_button.on_clicked(self._show_error_view)
        self.approx_button.on_clicked(self._show_approx_view)
        self.play_button.on_clicked(self._toggle_play_pause)

        self.lines: dict[str, object] = {}
        for method in self.methods:
            line, = self.main_ax.plot(
                [],
                [],
                color=method.color,
                linewidth=2,
                label=method.name,
            )
            self.lines[method.name] = line

        self.real_pi_line = self.main_ax.axhline(
            y=float(self.pi_real),
            color="black",
            linestyle="--",
            linewidth=1.4,
            label="pi real",
        )
        self.real_pi_line.set_visible(False)

        self.table = None
        self._create_table()
        self._configure_axes()
        self._refresh_legend()

        self.animation = FuncAnimation(
            self.figure,
            self._on_frame,
            interval=self.animation_interval_ms,
            blit=False,
            cache_frame_data=False,
        )
        # La animacion solo comienza al presionar Play.
        self.animation.event_source.stop()

    def _configure_axes(self) -> None:
        """Configura ejes segun el modo seleccionado."""
        self.main_ax.set_xlabel("Iteracion")
        self.main_ax.set_xscale("log")
        self.main_ax.set_xlim(1, max(2, self.max_iterations))

        if self.mode == "error":
            self.main_ax.set_title("Convergencia por Error Absoluto")
            self.main_ax.set_ylabel("Error absoluto")
            if self.use_log_scale_y_error:
                self.main_ax.set_yscale("log")
            else:
                self.main_ax.set_yscale("linear")
            self.real_pi_line.set_visible(False)
        else:
            self.main_ax.set_title("Convergencia de Aproximaciones de pi")
            self.main_ax.set_ylabel("Aproximacion de pi")
            self.main_ax.set_yscale("linear")
            self.real_pi_line.set_visible(True)

        self.main_ax.grid(True, which="both", linestyle=":", alpha=0.5)

    def _refresh_legend(self) -> None:
        """Actualiza la leyenda segun el modo actual."""
        handles = [self.lines[method.name] for method in self.methods]
        if self.mode == "approximation":
            handles.append(self.real_pi_line)
        self.main_ax.legend(handles=handles, loc="upper right")

    def _create_table(self) -> None:
        """Crea tabla lateral dinamica con valor y error por metodo."""
        rows = []
        for method in self.methods:
            rows.append(
                [
                    method.name,
                    "",
                    format_decimal(method.get_current_value()),
                    format_decimal(method.get_error()),
                ]
            )

        self.table = self.table_ax.table(
            cellText=rows,
            colLabels=["Metodo", "Color", "Pi aprox", "Error"],
            loc="center",
            cellLoc="left",
        )
        self.table.auto_set_font_size(False)
        self.table.set_fontsize(9)
        self.table.scale(1.0, 1.5)

        for row_idx, method in enumerate(self.methods, start=1):
            color_cell = self.table[(row_idx, 1)]
            color_cell.set_facecolor(method.color)
            color_cell.get_text().set_text("   ")

    def _update_table(self) -> None:
        """Actualiza la tabla con datos de la iteracion actual."""
        for row_idx, method in enumerate(self.methods, start=1):
            self.table[(row_idx, 2)].get_text().set_text(format_decimal(method.get_current_value()))
            self.table[(row_idx, 3)].get_text().set_text(format_decimal(method.get_error()))

    def _show_error_view(self, _event: object) -> None:
        """Activa modo de visualizacion de error absoluto."""
        self.mode = "error"
        self._configure_axes()
        self._refresh_lines()
        self._refresh_legend()
        self.figure.canvas.draw_idle()

    def _show_approx_view(self, _event: object) -> None:
        """Activa modo de visualizacion de aproximacion de pi."""
        self.mode = "approximation"
        self._configure_axes()
        self._refresh_lines()
        self._refresh_legend()
        self.figure.canvas.draw_idle()

    def _toggle_play_pause(self, _event: object) -> None:
        """Inicia o pausa la animacion."""
        if self.current_iteration >= self.max_iterations:
            return

        if self.is_running:
            self.is_running = False
            self.animation.event_source.stop()
            self.play_button.label.set_text("Play")
        else:
            self.is_running = True
            self.animation.event_source.start()
            self.play_button.label.set_text("Pausa")

        self.figure.canvas.draw_idle()

    def _refresh_lines(self) -> None:
        """Refresca curvas segun el modo actual sin recalcular iteraciones."""
        x_data = self.iterations
        for method in self.methods:
            if self.mode == "error":
                y_data = self.error_history[method.name]
            else:
                y_data = self.pi_history[method.name]
            self.lines[method.name].set_data(x_data, y_data)

        self.main_ax.relim()
        self.main_ax.autoscale_view(scalex=False, scaley=True)

    def _on_frame(self, _frame_index: int) -> list[object]:
        """Actualiza un frame de la animacion."""
        if not self.is_running:
            return list(self.lines.values()) + [self.real_pi_line]

        if self.current_iteration >= self.max_iterations:
            self.is_running = False
            self.animation.event_source.stop()
            self.play_button.label.set_text("Play")
            return list(self.lines.values()) + [self.real_pi_line]

        self.current_iteration += 1
        self.iterations.append(self.current_iteration)

        for method in self.methods:
            method.update()
            current_pi = method.get_current_value()
            current_error = method.get_error()

            self.pi_history[method.name].append(float(current_pi))
            plot_error = current_error if current_error > self.min_plot_error else self.min_plot_error
            self.error_history[method.name].append(float(plot_error))

        self._refresh_lines()
        self._update_table()

        return list(self.lines.values()) + [self.real_pi_line]

    def show(self) -> None:
        """Muestra la interfaz interactiva."""
        plt.show()
