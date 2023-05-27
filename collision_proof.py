import matplotlib.pyplot as plt  # type: ignore
import numpy as np


class PointMover:
    def __init__(self, ax):
        self.ax = ax
        self.points = {
            "A": np.array([1, 3]),
            "B": np.array([5, 6]),
            "C": np.array([2, 2]),
            "D": np.array([6, 4]),
        }
        self.active_point = None
        self.connect()

    def connect(self):
        self.ax.figure.canvas.mpl_connect("button_press_event", self.on_press)
        self.ax.figure.canvas.mpl_connect("button_release_event", self.on_release)
        self.ax.figure.canvas.mpl_connect("motion_notify_event", self.on_motion)

    def on_press(self, event):
        if event.button != 1:
            return
        for point, coord in self.points.items():
            if (
                np.sqrt((coord[0] - event.xdata) ** 2 + (coord[1] - event.ydata) ** 2)
                < 0.2
            ):
                self.active_point = point
                break

    def on_release(self, event):
        if event.button != 1:
            return
        self.active_point = None

    def on_motion(self, event):
        if self.active_point is None:
            return
        self.points[self.active_point] = np.array([event.xdata, event.ydata])
        self.ax.clear()
        self.plot()

    def plot(self):
        # Plot lines
        self.ax.plot(
            [self.points["A"][0], self.points["B"][0]],
            [self.points["A"][1], self.points["B"][1]],
            label="Line A-B",
            color="blue",
        )
        self.ax.plot(
            [self.points["C"][0], self.points["D"][0]],
            [self.points["C"][1], self.points["D"][1]],
            label="Line C-D",
            color="red",
        )

        # Plot points
        for point, coord in self.points.items():
            self.ax.plot(coord[0], coord[1], "o", label=point)

        # Check orientations and intersection
        orientation_AC_D = ccw(self.points["A"], self.points["C"], self.points["D"])
        orientation_BC_D = ccw(self.points["B"], self.points["C"], self.points["D"])
        orientation_AB_C = ccw(self.points["A"], self.points["B"], self.points["C"])
        orientation_AB_D = ccw(self.points["A"], self.points["B"], self.points["D"])

        if (
            orientation_AC_D != orientation_BC_D
            and orientation_AB_C != orientation_AB_D
        ):
            intersection_label = "Lines Intersect"
            intersection_color = "green"
        else:
            intersection_label = "Lines Do Not Intersect"
            intersection_color = "black"

        self.ax.annotate(intersection_label, xy=(3, 1), color=intersection_color)

        # Display clockwise and counterclockwise values
        self.ax.text(1.5, 1, f"Orientation AC-D: {str(orientation_AC_D)}", fontsize=8)
        self.ax.text(1.5, 0.8, f"Orientation BC-D: {str(orientation_BC_D)}", fontsize=8)
        self.ax.text(1.5, 0.6, f"Orientation AB-C: {str(orientation_AB_C)}", fontsize=8)
        self.ax.text(1.5, 0.4, f"Orientation AB-D: {str(orientation_AB_D)}", fontsize=8)

        # Set plot properties
        self.ax.set_xlim([0, 8])
        self.ax.set_ylim([0, 8])
        self.ax.legend()
        self.ax.set_title("Visualization of Proof")
        plt.grid(True)
        plt.draw()


def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def visualize_proof():
    fig, ax = plt.subplots()

    mover = PointMover(ax)
    mover.plot()

    plt.show()


visualize_proof()
