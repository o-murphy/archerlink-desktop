import asyncio
import subprocess
import sys

from kivy.metrics import dp
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarSupportingText, MDSnackbarButtonContainer, \
    MDSnackbarActionButton, MDSnackbarActionButtonText, MDSnackbarCloseButton, MDSnackbarText


async def open_file_path(filepath):
    if sys.platform == "win32":
        # Use 'explorer' with '/select,' to highlight the file
        subprocess.Popen(['explorer', '/select,', filepath])
    elif sys.platform == "darwin":
        # Use 'open' with '-R' to reveal the file in Finder
        subprocess.Popen(['open', '-R', filepath])
    else:
        # On Linux, there is no standard way to highlight a file, just open the directory
        subprocess.Popen(['xdg-open', filepath])


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
            # MDSnackbarCloseButton(
            #     icon="close",
            # ),
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
