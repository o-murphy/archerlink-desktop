import asyncio
from modules.env import open_file_path
from kivy.metrics import dp

from kivymd.uix.snackbar import MDSnackbar, MDSnackbarSupportingText, MDSnackbarButtonContainer, \
    MDSnackbarActionButton, MDSnackbarActionButtonText, MDSnackbarText


async def file_toast(text, path):
    action_button = MDSnackbarActionButton(
        MDSnackbarActionButtonText(
            text="Open in files"
        ),
    )
    action_button.bind(on_release=lambda x: asyncio.create_task(open_file_path(path)))

    snackbar = MDSnackbar(
        MDSnackbarSupportingText(
            text=text,
        ),
        MDSnackbarButtonContainer(
            action_button,
            pos_hint={"center_y": 0.5}
        ),
        y=dp(24),
        orientation="horizontal",
        pos_hint={"center_x": 0.5},
        size_hint_x=0.5,
        duration=3
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
