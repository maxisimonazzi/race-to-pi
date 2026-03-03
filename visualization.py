"""Visualizacion y animacion de la convergencia de metodos para calcular pi."""

from __future__ import annotations

from decimal import Decimal

import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, CheckButtons

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
        enable_blit: bool,
        redraw_axes_every_n_frames: int,
        redraw_table_every_n_frames: int,
    ) -> None:
        """Construye la interfaz, controles y estructura de animacion incremental."""
        self.methods = methods
        self.pi_real = pi_real
        self.max_iterations = max_iterations
        self.animation_interval_ms = animation_interval_ms
        self.use_log_scale_y_error = use_log_scale_y_error
        self.min_plot_error = min_plot_error
        self.enable_blit = enable_blit
        self.redraw_axes_every_n_frames = max(1, redraw_axes_every_n_frames)
        self.redraw_table_every_n_frames = max(1, redraw_table_every_n_frames)

        self.mode = "error"
        self.current_iteration = 0
        self.is_running = False
        self.selected_methods = {method.name: True for method in methods}
        self.methods_by_name = {method.name: method for method in methods}
        self._table_method_names: list[str] = []

        self.iterations: list[int] = []
        self.pi_history: dict[str, list[float]] = {method.name: [] for method in methods}
        self.error_history: dict[str, list[float]] = {method.name: [] for method in methods}

        self.figure, self.main_ax = plt.subplots(figsize=(14, 8))
        self.figure.canvas.manager.set_window_title("La carrera de pi")
        self.figure.suptitle("La carrera de π", fontsize=18, fontweight="bold", y=0.995)
        self.figure.text(
            0.5,
            0.94,
            "Comparativa de métodos de convergencia para el cálculo de π",
            ha="center",
            fontsize=12,
        )
        plt.subplots_adjust(left=0.08, right=0.67, bottom=0.2, top=0.82)

        self.checkbox_ax = self.figure.add_axes([0.68, 0.58, 0.30, 0.35])
        self.checkbox_ax.set_title("Metodos visibles", fontsize=11)
        checkbox_labels = [method.name for method in self.methods]
        checkbox_states = [True for _ in self.methods]
        self.check_buttons = CheckButtons(self.checkbox_ax, checkbox_labels, checkbox_states)
        self.check_buttons.on_clicked(self._toggle_method_visibility)
        self._style_check_buttons()

        self.table_ax = self.figure.add_axes([0.68, 0.18, 0.30, 0.37])
        self.table_ax.axis("off")

        self.error_button_ax = self.figure.add_axes([0.12, 0.06, 0.16, 0.08])
        self.approx_button_ax = self.figure.add_axes([0.30, 0.06, 0.16, 0.08])
        self.play_button_ax = self.figure.add_axes([0.48, 0.06, 0.16, 0.08])
        self.reset_button_ax = self.figure.add_axes([0.66, 0.06, 0.12, 0.08])

        self.error_button = Button(self.error_button_ax, "Ver Error")
        self.approx_button = Button(self.approx_button_ax, "Ver Aproximacion")
        self.play_button = Button(self.play_button_ax, "Play")
        self.reset_button = Button(self.reset_button_ax, "Reset")

        self.error_button.on_clicked(self._show_error_view)
        self.approx_button.on_clicked(self._show_approx_view)
        self.play_button.on_clicked(self._toggle_play_pause)
        self.reset_button.on_clicked(self._reset_app_state)

        self.lines: dict[str, object] = {}
        for method in self.methods:
            line, = self.main_ax.plot(
                [],
                [],
                color=method.color,
                linewidth=2,
            )
            self.lines[method.name] = line

        self.real_pi_line = self.main_ax.axhline(
            y=float(self.pi_real),
            color="black",
            linestyle="--",
            linewidth=1.4,
        )
        self.real_pi_line.set_visible(False)

        self.table = None
        self._create_table()
        self._configure_axes()
        self._refresh_lines()

        self.animation = FuncAnimation(
            self.figure,
            self._on_frame,
            interval=self.animation_interval_ms,
            blit=self.enable_blit,
            cache_frame_data=False,
        )
        # La animacion solo comienza al presionar Play.
        self.animation.event_source.stop()

    def _configure_axes(self) -> None:
        """Configura ejes segun el modo seleccionado."""
        self.main_ax.set_xlabel("Iteracion", fontweight="bold")
        self.main_ax.set_xscale("log")
        self.main_ax.set_xlim(1, max(2, self.max_iterations))

        if self.mode == "error":
            self.main_ax.set_ylabel("Error absoluto", fontweight="bold")
            if self.use_log_scale_y_error:
                self.main_ax.set_yscale("log")
            else:
                self.main_ax.set_yscale("linear")
            self.real_pi_line.set_visible(False)
        else:
            self.main_ax.set_ylabel("Aproximacion de pi", fontweight="bold")
            self.main_ax.set_yscale("linear")
            self.real_pi_line.set_visible(True)

        self.main_ax.grid(True, which="both", linestyle=":", alpha=0.5)

    def _get_visible_methods(self) -> list[PiMethod]:
        """Devuelve la lista de metodos actualmente visibles."""
        return [method for method in self.methods if self.selected_methods[method.name]]

    def _style_check_buttons(self) -> None:
        """Aumenta el tamano visual de las casillas para mejorar la seleccion."""
        method_colors = [method.color for method in self.methods]
        item_count = len(self.methods)

        # Matplotlib >= 3.7: agranda realmente caja y marca del checkbox.
        if hasattr(self.check_buttons, "set_label_props"):
            self.check_buttons.set_label_props(
                {
                    "color": method_colors,
                    "fontsize": [11] * item_count,
                }
            )
        else:
            for label, method in zip(self.check_buttons.labels, self.methods):
                label.set_color(method.color)
                label.set_fontsize(11)

        if hasattr(self.check_buttons, "set_frame_props"):
            self.check_buttons.set_frame_props(
                {
                    "sizes": [260] * item_count,
                    "linewidths": [1.6] * item_count,
                }
            )
        else:
            rectangles = getattr(self.check_buttons, "rectangles", [])
            for rectangle in rectangles:
                x_pos, y_pos = rectangle.get_xy()
                width = rectangle.get_width()
                height = rectangle.get_height()
                center_x = x_pos + width / 2
                center_y = y_pos + height / 2
                new_width = width * 2.0
                new_height = height * 2.0
                rectangle.set_width(new_width)
                rectangle.set_height(new_height)
                rectangle.set_xy((center_x - new_width / 2, center_y - new_height / 2))

        if hasattr(self.check_buttons, "set_check_props"):
            self.check_buttons.set_check_props(
                {
                    "sizes": [170] * item_count,
                    "linewidths": [2.8] * item_count,
                }
            )
        else:
            check_lines = getattr(self.check_buttons, "lines", [])
            for line_pair in check_lines:
                for line in line_pair:
                    line.set_linewidth(2.8)

    def _create_table(self) -> None:
        """Crea tabla lateral dinamica con valor y error por metodo."""
        if self.table is not None:
            self.table.remove()
            self.table = None

        self.table_ax.clear()
        self.table_ax.axis("off")

        visible_methods = self._get_visible_methods()
        self._table_method_names = [method.name for method in visible_methods]
        if not visible_methods:
            self.table_ax.text(
                0.5,
                0.5,
                "Ningun metodo seleccionado",
                ha="center",
                va="center",
                fontsize=10,
            )
            return

        rows = []
        for method in visible_methods:
            rows.append(
                [
                    "",
                    method.name,
                    format_decimal(method.get_current_value()),
                    format_decimal(method.get_error()),
                ]
            )

        self.table = self.table_ax.table(
            cellText=rows,
            colLabels=["Color", "Metodo", "Pi aprox", "Error"],
            loc="center",
            cellLoc="left",
            colWidths=[0.10, 0.36, 0.25, 0.30],
        )
        self.table.auto_set_font_size(False)
        self.table.set_fontsize(8)
        self.table.scale(1.0, 1.5)

        for row_idx, method in enumerate(visible_methods, start=1):
            color_cell = self.table[(row_idx, 0)]
            color_cell.set_facecolor(method.color)
            color_cell.get_text().set_text("   ")

    def _update_table(self) -> None:
        """Actualiza la tabla con datos de la iteracion actual."""
        if self.table is None:
            return
        for row_idx, method_name in enumerate(self._table_method_names, start=1):
            method = self.methods_by_name[method_name]
            self.table[(row_idx, 2)].get_text().set_text(format_decimal(method.get_current_value()))
            self.table[(row_idx, 3)].get_text().set_text(format_decimal(method.get_error()))

    def _toggle_method_visibility(self, method_name: str) -> None:
        """Muestra u oculta un metodo en grafico y tabla."""
        if hasattr(self.check_buttons, "get_status"):
            method_names = [method.name for method in self.methods]
            method_index = method_names.index(method_name)
            self.selected_methods[method_name] = bool(self.check_buttons.get_status()[method_index])
        else:
            self.selected_methods[method_name] = not self.selected_methods[method_name]
        self._refresh_lines()
        self._create_table()
        self.figure.canvas.draw_idle()

    def _show_error_view(self, _event: object) -> None:
        """Activa modo de visualizacion de error absoluto."""
        self.mode = "error"
        self._configure_axes()
        self._refresh_lines()
        self.figure.canvas.draw_idle()

    def _show_approx_view(self, _event: object) -> None:
        """Activa modo de visualizacion de aproximacion de pi."""
        self.mode = "approximation"
        self._configure_axes()
        self._refresh_lines()
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

    def _reset_app_state(self, _event: object) -> None:
        """Reinicia toda la aplicacion al estado inicial."""
        self.is_running = False
        self.animation.event_source.stop()
        self.play_button.label.set_text("Play")

        # Reinstancia cada metodo para limpiar su estado interno incremental.
        self.methods = [method.__class__(color=method.color, pi_real=self.pi_real) for method in self.methods]
        self.methods_by_name = {method.name: method for method in self.methods}
        self.selected_methods = {method.name: True for method in self.methods}

        self.current_iteration = 0
        self.iterations = []
        self.pi_history = {method.name: [] for method in self.methods}
        self.error_history = {method.name: [] for method in self.methods}
        self.mode = "error"

        if hasattr(self.check_buttons, "get_status"):
            for index, is_active in enumerate(self.check_buttons.get_status()):
                if not is_active:
                    self.check_buttons.set_active(index)

        self._configure_axes()
        self._create_table()
        self._refresh_lines()
        self.figure.canvas.draw_idle()

    def _refresh_lines(self, recalculate_axes: bool = True) -> None:
        """Refresca curvas segun el modo actual sin recalcular iteraciones."""
        x_data = self.iterations
        has_visible_methods = False
        for method in self.methods:
            line = self.lines[method.name]
            if not self.selected_methods[method.name]:
                line.set_visible(False)
                line.set_data([], [])
                continue

            has_visible_methods = True
            if self.mode == "error":
                y_data = self.error_history[method.name]
            else:
                y_data = self.pi_history[method.name]
            line.set_visible(True)
            line.set_data(x_data, y_data)

        if has_visible_methods and recalculate_axes:
            self.main_ax.relim()
            self.main_ax.autoscale_view(scalex=False, scaley=True)
        elif not has_visible_methods and self.mode == "error":
            self.main_ax.set_ylim(float(self.min_plot_error), 1.0)
        elif not has_visible_methods:
            pi_float = float(self.pi_real)
            self.main_ax.set_ylim(pi_float - 1.0, pi_float + 1.0)

        self.main_ax.set_xlim(1, max(2, self.max_iterations))

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

        recalculate_axes = (self.current_iteration % self.redraw_axes_every_n_frames) == 0
        redraw_table = (self.current_iteration % self.redraw_table_every_n_frames) == 0

        self._refresh_lines(recalculate_axes=recalculate_axes)
        if redraw_table or self.current_iteration == 1:
            self._update_table()

        return list(self.lines.values()) + [self.real_pi_line]

    def show(self) -> None:
        """Muestra la interfaz interactiva."""
        plt.show()
