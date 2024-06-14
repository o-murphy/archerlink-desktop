import asyncio

from kivy.metrics import dp
from kivymd.uix.snackbar import (MDSnackbar, MDSnackbarSupportingText, MDSnackbarButtonContainer,
                                 MDSnackbarActionButton, MDSnackbarActionButtonText, MDSnackbarText)

from env import open_file_path


async def file_toast(app, text, path, err=False):
    async def dismiss():
        snackbar.dismiss()

    async def on_action():
        await dismiss()
        await open_file_path(path)

    action_button = MDSnackbarActionButton(
        MDSnackbarActionButtonText(
            text="Open in files"
        ),
        style="outlined"
    )
    # close_button = MDSnackbarCloseButton(
    #     icon="close",
    # )

    action_button.bind(on_release=lambda x: asyncio.create_task(on_action()))
    # close_button.bind(on_release=lambda x: asyncio.create_task(dismiss()))

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
