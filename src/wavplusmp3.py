#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# wavplusmp3.py
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

#from wavplusmp3bitrate import ChooserUI
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
import os, sys, signal, subprocess


#Comment the first line and uncomment the second before installing
#or making the tarball (alternatively, use project variables)
UI_FILE = "wavplusmp3.ui"
UI_BIT = "wavplusmp3bitrate.ui"
#UI_FILE = "/usr/local/share/wavplusmp3/ui/wavplusmp3.ui"

class bitRate(Gtk.Window):
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_BIT)
		self.builder.connect_signals(self)

		self.bitwindow = self.builder.get_object('window1')
		button_start = self.builder.get_object('buttonStart')
		radio1 = self.builder.get_object('radiobutton1')
		radio2 = self.builder.get_object('radiobutton2')
		radio3 = self.builder.get_object('radiobutton3')
		radio4 = self.builder.get_object('radiobutton4')

		self.bitwindow.show_all()

	def on_buttonStart_clicked(buttonStart, self):
		print("test")

class GUI(Gtk.Window):

	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		self.window = self.builder.get_object('window')
		layout1 = self.builder.get_object('layout1')
		button1 = self.builder.get_object('button1')

		self.window.set_keep_above = "true"

		self.window.show_all()

		########## check for ffmpeg ##########

		try:
			checkffmpeg = subprocess.check_call(["ffmpeg", "-version"], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
		except:
			noffmpeg = Gtk.MessageDialog(window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "No ffmpeg detected! This is required in order to use this program. Please download using your package manager.")
			noffmpeg.run()
			noffmpeg.destroy()
			sys.exit(1)

	def on_button1_clicked(self, button1):

		########## create file chooser dialog ##########

		newdialg = Gtk.FileChooserDialog("Choose a wav file...", None, Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		self.addfilters(newdialg)
		resp = newdialg.run()

		if resp == Gtk.ResponseType.OK:
			#print("Wav file selected")
			########## attempt wav->mp3 conversion ##########

			self.wav_file = newdialg.get_filename()
			bitRate()

		elif resp == Gtk.ResponseType.CANCEL:
			print("Cancelled")
		newdialg.destroy()

	########## add filters to dialog ##########

	def addfilters(self,newdialg):
		filter_wavs = Gtk.FileFilter()
		filter_wavs.set_name("*Wav Files")
		filter_wavs.add_mime_type("audio/x-wav")
		newdialg.add_filter(filter_wavs)

#################### DESTROY WINDOW ####################

	def on_window_destroy(self, window):
		Gtk.main_quit()

def main():
	app = GUI()
	Gtk.main()

if __name__ == "__main__":
	sys.exit(main())
