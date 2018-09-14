def is_left_click(widget, touch):
    """Check if the touch was on the widget and was a left click."""
    # Return False if was outside the widget.
    if not widget.collide_point(*touch.pos):
        return False

    # Return False if touch was not.
    if not 'button' in touch.profile:
        return False

    # Return False if button is not left.
    if touch.button != 'left':
        return False

    # Is a left click.
    return True
