import customtkinter as ctk
from gui import PacketLossCheckerApp


def main():
    # Set appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Run application
    app = PacketLossCheckerApp()
    app.run()


if __name__ == "__main__":
    main()