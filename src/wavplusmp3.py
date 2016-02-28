#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# main.py
# The MIT License (MIT)
# Copyright (C) 2016 computerfreak20
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and ths permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTIBILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from wavplusmp3file import ChooserUI
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
import os, sys, signal


#Comment the first line and uncomment the second before installing
#or making the tarball (alternatively, use project variables)
UI_FILE = "wavplusmp3.ui"
#UI_FILE = "/usr/local/share/wavplusmp3/ui/wavplusmp3.ui"


class GUI(ChooserUI):
    
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)
        
		window = self.builder.get_object('window')
		filechooser = self.builder.get_object('filechooserdialog1')
		layout1 = self.builder.get_object('layout1')
		button1 = self.builder.get_object('button1')

		window.set_keep_above = "true"

		window.show_all()

	def on_button1_clicked(button1, button):
		print("titties")
		test = ChooserUI();

	def on_window_destroy(self, window):
		Gtk.main_quit()

def main():
	#fd = FileChooser()
	app = GUI()
	Gtk.main()
	
if __name__ == "__main__":
	sys.exit(main())

