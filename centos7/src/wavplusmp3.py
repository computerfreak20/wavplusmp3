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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
import os, sys, signal, subprocess, datetime


#Comment the first line and uncomment the second before installing
#or making the tarball (alternatively, use project variables)
UI_FILE = "wavplusmp3.ui"
UI_BIT = "wavplusmp3bitrate.ui"

DATIEM = "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
LOGSTRING = "\n#################### wavplusmp3 log | "+DATIEM+" ####################\n\n"
LOGSTR2 = ""

#UI_FILE = "/usr/local/share/wavplusmp3/ui/wavplusmp3.ui"

class createLog(Gtk.Window):
	def __init__(self):
		try:
			logop = open("log.txt", "a")
			if LOGSTR2 == "":
				logop.write(LOGSTRING)
			else:
				logop.write(LOGSTRING+LOGSTR2)
				logop.close()
		except:
			log_failure = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Log error!")
			log_failure.format_secondary_text("Failed to write to the log file. Bad permissions?")
			log_failure.run()
			log_failure.destroy()

class bitRate(Gtk.Window):
	def __init__(self, wav_file):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_BIT)
		self.builder.connect_signals(self)

		self.bitwindow = self.builder.get_object('window1')
		button_start = self.builder.get_object('buttonStart')
		box2 = self.builder.get_object('box2')
		self.radio1 = self.builder.get_object('radiobutton1')
		self.radio2 = self.builder.get_object('radiobutton2')
		self.radio3 = self.builder.get_object('radiobutton3')
		self.radio4 = self.builder.get_object('radiobutton4')

		self.wav_file = wav_file
		self.BRATE = "vbr"

		self.bitwindow.show_all()

	########## attempt wav->mp3 conversion ##########

	def on_buttonStart_clicked(self, buttonStart):
		createLog()
		try:
			self.real_file_name = os.path.basename(self.wav_file)
			self.edit_wav = self.real_file_name[:-4]

			convert_success = Gtk.MessageDialog(self.bitwindow, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Success")
			convert_success.format_secondary_text(self.real_file_name+" successfully converted to "+self.edit_wav+".mp3 @ "+self.BRATE+"bps \n Now exiting...")

			if self.BRATE != "vbr":
				convertfile = subprocess.check_call(["ffmpeg", "-i", self.wav_file, "-vn", "-ar", "44100", "-ac", "2", "-ab", self.BRATE, "-y", "-f", "mp3", self.edit_wav+".mp3"], stdout=open("log.txt", "a"), stderr=subprocess.STDOUT)
				convert_success.run()
				convert_success.destroy()
				Gtk.main_quit()
			else:
				convertfile = subprocess.check_call(["ffmpeg", "-i", self.wav_file, "-vn", "-ar", "44100", "-ac", "2", "-aq", "5", "-y", "-f", "mp3", self.edit_wav+".mp3"], stdout=open("log.txt", "a"), stderr=subprocess.STDOUT)
				convert_success.run()
				convert_success.destroy()
				Gtk.main_quit()
		except:
			convert_failure = Gtk.MessageDialog(self.bitwindow, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Conversion failed!")
			convert_failure.run()
			convert_failure.destroy()
			LOGSTR2 = "CONVERSION FAILED!!!"
			Gtk.main_quit()

	def on_radiobutton1_toggled(self, radiobutton1):
		if self.radio1.get_active() == True:
			self.BRATE = "vbr"

	def on_radiobutton2_toggled(self, radiobutton2):
		if self.radio2.get_active() == True:
			self.BRATE = "128k"

	def on_radiobutton3_toggled(self, radiobutton3):
		if self.radio3.get_active() == True:
			self.BRATE = "256k"

	def on_radiobutton4_toggled(self, radiobutton4):
		if self.radio4.get_active() == True:
			self.BRATE = "320k"

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
			noffmpeg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "No ffmpeg detected! This is required in order to use this program. Please download using your package manager.")
			noffmpeg.run()
			noffmpeg.destroy()
			Gtk.main_quit()

	def on_button1_clicked(self, button1):

		########## create file chooser dialog ##########

		newdialg = Gtk.FileChooserDialog("Choose a wav file...", None, Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		self.addfilters(newdialg)
		resp = newdialg.run()

		if resp == Gtk.ResponseType.OK:

			########## open bitrate dialog ##########

			self.wav_file = newdialg.get_filename()
			newdialg.destroy()
			bitRate(self.wav_file)

		elif resp == Gtk.ResponseType.CANCEL:
			newdialg.destroy()

	########## add filters to dialog ##########

	def addfilters(self, newdialg):
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
