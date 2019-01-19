from appJar import gui


class DcsRosettaApp:
    TA_OUTPUT = 'Output'

    def __init__(self):
        self.app = gui('DCS Rosetta', '600x400')
        self.app.addButton("Browse", self.browse)
        self.app.addTextArea(self.TA_OUTPUT)
        self.app.go()

    def browse(self):
        file_name = self.app.openBox(dirName='~/Saved Games', fileTypes=[('DCS', '*.miz'), ('DCS', '*.cmp')])
        self.app.setTextArea(self.TA_OUTPUT, file_name)


if __name__ == '__main__':
    app = DcsRosettaApp()
