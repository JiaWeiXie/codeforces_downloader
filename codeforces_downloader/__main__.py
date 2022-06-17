import gradio
import environs

from codeforces_downloader.ui import DownloaderInterface

if __name__ == "__main__":
    env = environs.Env()
    env.read_env()
    SERVER_PORT = env.int("SERVER_PORT", default=None)
    DEBUG = env.bool("DEBUG", default=False)

    interface = DownloaderInterface()
    interface.start(True)
    interface.stop()
    gradio.close_all()
