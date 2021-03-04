from UserInterface import WaitWindow

################################################
# Show and close wait promptation in multithread
################################################


class ShowWaitWindow():

    wait = ''
    multithreadprompt = ''

    def __init__(self, text):
        self.wait = WaitWindow.WaitWindow(text)
        self.multithreadprompt = WaitWindow.MultiThreadPrompt(self.wait)

    def show_wait_window(self):
        self.multithreadprompt.show_wait_box()

    def close_wait_window(self):
        self.multithreadprompt.terminate_thread()