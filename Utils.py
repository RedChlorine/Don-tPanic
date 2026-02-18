from PySide6.QtGui import QColor

def get_panic_color(days_remaining):
    """Returns a color based on how close the deadline is of an assignment """

    if days_remaining <= 1:
        return QColor("#d32f2f") # Colors are passed as strings of hex - red

    elif days_remaining <= 5:
        return QColor("#f57c00") # amber

    return QColor("#388e3c") # green


def calculate_days_remaining(date_str):
    #PLACEHOLDER
    return 2
