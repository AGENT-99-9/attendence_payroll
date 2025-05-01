def formRow(self, label, widget):
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(label))
        hbox.addWidget(widget)
        return hbox