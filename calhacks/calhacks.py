"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""

    ...


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )

# Create a form that takes in a video file. This framework is called Reflex.
def submit_video_file() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.heading("Submit a Video File", size="9"),
        rx.form(
            rx.upload(
                id="my_upload",
            ),
            rx.button("Submit"),
        ),
    )

app = rx.App()
app.add_page(index)
app.add_page(submit_video_file, route="/submit")
