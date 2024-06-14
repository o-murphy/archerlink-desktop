import asyncio

from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.snackbar import (MDSnackbar, MDSnackbarSupportingText, MDSnackbarButtonContainer,
                                 MDSnackbarActionButton, MDSnackbarActionButtonText, MDSnackbarText)

from modules.env import open_file_path

MDApp.get_running_app()


async def file_toast(text, path, err=False):

    async def on_action():
        snackbar.dismiss()
        await open_file_path(path)

    app = MDApp.get_running_app()
    action_button = MDSnackbarActionButton(
        MDSnackbarActionButtonText(
            text="Open in files"
        ),
        style="outlined"
    )
    action_button.bind(on_release=lambda x: asyncio.create_task(on_action()))

    snackbar = MDSnackbar(
        MDSnackbarSupportingText(
            text=text,
            **{
                "theme_text_color": "Custom",
                "text_color": app.theme_cls.errorContainerColor,
            } if err else {}
        ),
        MDSnackbarButtonContainer(
            action_button,
            pos_hint={"center_y": 0.5}
        ),
        y=dp(24),
        orientation="horizontal",
        pos_hint={"center_x": 0.5},
        size_hint_x=0.5,
        duration=3,

        **{
            "background_color": app.theme_cls.onErrorContainerColor
        } if err else {},
    )
    snackbar.open()


async def toast(text):
    MDSnackbar(
        MDSnackbarText(
            text=text,
        ),
        y=dp(24),
        pos_hint={"center_x": 0.5},
        size_hint_x=0.8,
    ).open()
