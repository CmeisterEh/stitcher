# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 16:10:10 2022

@author: Main Floor
"""


import os

from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
from datetime import datetime
from ToolTip import ToolTip as TTip
from PyPDF2 import PdfFileMerger
from PopupMenu import PopupMenu as Popup



logFile = "log.txt"


class stitcher(Frame):
    def __init__(self, Parent = None, Root = None):
        Frame.__init__(self, Parent)

        #######
        ## Important Global variables for the Class
        self.Root = Root                      ## Main GUI Window (Root of window)
        self.Parent = Parent                  ## Parent Frame that the current Frame Lives in
        self.logFile = "log.txt"              ## Default name for error logging file
        self.inputFolder = None               ## Specifyable Default location to look for input
        self.outputFolder = None              ## Specifyable Default location to put output


        self.createWidgets()



    def createWidgets(self):
        self.createFiles()
        self.createMenu()
        self.createBody()
        self.pack_NotificationBar()

        self.PopupMenu()     #Initiate Popup Menu
        self.give_Popup()    #Bind it to the desired widgets


    def createFiles(self):

        ## Create Appropriate Log Folder
        try:
            self.current_dir = os.getcwd()
            if ( os.path.exists(self.current_dir + os.sep + "log") == False ):              # Make an error and log output directory
                os.mkdir(self.current_dir + os.sep + "log")
        except:
            self.userNotification("Error: Problem with \"Log\" folder")

        ## Create appropriate file name for log file, with absolute referencing
        self.current_dir = os.getcwd()
        log = self.logFile
        date_time = datetime.now()                                             # Obtain Current Date and Time
        timestamp = date_time.strftime("%G %b %d %I-%M%p")
        log = self.current_dir + os.sep +  "log" + os.sep + timestamp + "-" + log


        ## Create Log File
        try:
            file = open(log, 'w')                                              # Opening or creating log file
        ## Preamble Text when file is first created
            date_time = datetime.now()                                             # Obtain Current Date and Time
            file.write( date_time.strftime("%G %b %d %I:%M%p") + " " + "log.txt" )
            file.write("\n")
            file.write( "CRC begins" )
            file.write("\n")
            file.close()
            self.logFile = log                                                     # Name of logFile for future writes

        except:
            self.userNotification("Error: Problem with log file")
            #print("Log file failed to open")                                  # If log file fails to create

    def createBody(self):

        ##########################################
        ##########################################
        ## All of the input file options in one frame

        self.topFrame = Frame(self.master)
        self.topFrame.pack(expand = YES, fill = X)

        self.topFrame.widgets = []  #widgets = [widget, properties, row]

        self.topFrame_createNew()



        ###############################################
        ###############################################
        ## All of the bottom frame options in one row

        self.bottomFrame = Frame(self.master)
        self.bottomFrame.pack(expand = YES, fill = X)



        ## Find or Create Directory
        if self.outputFolder == None:
            current_dir = os.getcwd()
            if ( os.path.exists( current_dir + os.sep + "output" ) == False ):
                os.mkdir( current_dir + os.sep + "output" )
            self.outputFolder = current_dir + os.sep + "output" + os.sep




        self.widg11 = Label( self.bottomFrame, text = "Output Files", font = ('Times', '16', 'underline') )
        self.widg11.grid(row = 4, column = 0, columnspan = 3, sticky = W)



        self.widg12 = Label(self.bottomFrame, text = "Output File", font = ('Times', '12'))
        self.widg12.grid(row = 5, column = 0, sticky = W)

        ##Text box here
        self.widg13 = Entry( self.bottomFrame, width = 40)
        self.widg13.grid( row = 5, column = 1, columnspan = 2, sticky = W)
        self.widg13.insert(0, "FileName.pdf")



        self.widg14 = Label(self.bottomFrame, text = "Output Folder", font = ('Times', '12'))
        self.widg14.grid(row = 6, column = 0, sticky = W)


        self.file_dir3 = StringVar()
        self.widg15 = Entry( self.bottomFrame, textvariable = self.file_dir3, width = 47, font = "TkFixedFont" )
        #self.widg8 = Text(self.master, width = 40, height = 1)
        self.widg15.insert(0, self.outputFolder)
        self.widg15.xview( END )
        #self.widg8.mark_set( "insert", 'end' )
        self.widg15.config( state = 'readonly')
        self.widg15.config( bg = "light gray" )
        self.widg15.grid( row = 6, column = 1, columnspan = 2, sticky = W)

        self.widg16 = Button(self.bottomFrame, text = "Browse" )
        self.widg16.config(command = (lambda file_dir = self.outputFolder, widget = self.widg15 : self.browse_output(file_dir, widget) ))
        self.widg16.grid( row = 6, column = 3, sticky = W )

        self.widg17 = Label(self.bottomFrame, text = "Open after merging?", font = ('Times', '12'))
        self.widg17.grid ( row = 7, column = 0, columnspan = 2, sticky = W)
        self.widg17.ToolTip = TTip(self.widg17, text = "Open the output file when you hit \"Merge\"", time = 15000)

        self.widg18_var = IntVar()
        self.widg18 =  Checkbutton(self.bottomFrame, variable = self.widg18_var)
        self.widg18.grid( row = 7, column = 1)
        self.widg18.ToolTip = TTip(self.widg18, text = "Open the output file when you hit \"Merge\"", time = 15000)

        self.widg19 = Button(self.bottomFrame, text = "Merge!", command = self.mergeOperations)
        self.widg19.grid( row = 7, column = 3, sticky = E )
        self.widg19.ToolTip = TTip(self.widg19, text = "3...2...1...Merge those PDF's!", time = 15000)



        self.widg20 = Label(self.bottomFrame, text ="Open Containing Folder?", font = ('Times', '12') )
        self.widg20.grid(row = 8, column = 0, columnspan = 2, sticky = W)
        self.widg20.ToolTip = TTip(self.widg20, text = "Open the folder containing your output when you hit \"Merge\"", time = 15000)

        self.widg21_var = IntVar()
        self.widg21 = Checkbutton(self.bottomFrame, variable = self.widg21_var)
        self.widg21.grid(row = 8, column = 1)
        self.widg21.ToolTip = TTip(self.widg21, text = "Open the folder containing your output when you hit \"Merge\"", time = 15000)

    def topFrame_createNew(self):
        ## need to create two rows to start with
        ## need to append those rows to a list

        ## Find or Create Directory
        if self.inputFolder == None:
            current_dir = os.getcwd()
            if ( os.path.exists( current_dir + os.sep + "input" ) == False ):
                os.mkdir( current_dir + os.sep + "input" )
            self.inputFolder = current_dir + os.sep + "input" + os.sep



        self.topFrame.widgets = []  # widgets =   [ Initial Title Widget
                                    #               Input Row 1
                                    #               Input Row 2
                                    #               etc
                                    #               Ending [+] Button Widget]

                                    # Input Row = [ Label, String Variable, Entry, Browse Button, [-] Button]

        rowofwidgets = [] #Label | StringVar | Entry | Browse Button | - Button
        widg = Label( self.topFrame, text = "Input Files", font = ('Times', '16', 'underline') )
        widg.grid(row = 0, column = 0, columnspan = 3, sticky = W)
        rowofwidgets.append(widg)
        self.topFrame.widgets.append(rowofwidgets)

        for row in range(2):

            thisRow = row + 1

            rowofwidgets = []

            widg = Label(self.topFrame, text = "Input File", font = ('Times', '12'))
            widg.grid(row = thisRow, column = 0, sticky = W)
            rowofwidgets.append(widg)

            file_dir = StringVar()
            rowofwidgets.append(file_dir)

            widg = Entry( self.topFrame, textvariable = file_dir, width = 48, font = "TkFixedFont" )
            #self.widg8 = Text(self.master, width = 40, height = 1)
            widg.insert(0, self.inputFolder)
            widg.xview( END )
            #self.widg8.mark_set( "insert", 'end' )
            widg.config( state = 'readonly')
            widg.config( bg = "light gray" )
            widg.grid( row = thisRow, column = 1, columnspan = 2, sticky = W)
            rowofwidgets.append(widg)

            widg = Button(self.topFrame, text = "Browse", command = (lambda file_dir = self.inputFolder, widget = widg : self.browse_input(file_dir, widget) ) )
            widg.grid( row = thisRow, column = 3, sticky = W )
            rowofwidgets.append(widg)

            widg = Button(self.topFrame, text = "-", width = 1)
            widg.config(command = (lambda myself = widg: self.topFrame_remove(myself)) )
            widg.grid( row = thisRow, column = 4, sticky = W)
            rowofwidgets.append(widg)

            self.topFrame.widgets.append(rowofwidgets)



        rowofwidgets = []
        widg = Button(self.topFrame, text = "+", width = 1, command = self.topFrame_insert)
        widg.grid( row = thisRow + 1, column = 4, sticky = W)
        rowofwidgets.append(widg)
        self.topFrame.widgets.append(rowofwidgets)

    def topFrame_insert(self):

        ###############################
        ## Basic operation
        ## Pops off the last widget, which is always the [+] insertion widget
        ## Inserts a new row in its place
        ## Puts a new [+] widget  right below it



        widg = self.topFrame.widgets.pop()
        widg[0].destroy()

        row = len(self.topFrame.widgets) - 1
        thisRow = row + 1

        rowofwidgets = []   #Label | StringVar | Entry | Browse Button | - Button

        widg = Label(self.topFrame, text = "Input File", font = ('Times', '12'))
        widg.grid(row = thisRow, column = 0, sticky = W)
        rowofwidgets.append(widg)

        file_dir = StringVar()
        rowofwidgets.append(file_dir)

        widg = Entry( self.topFrame, textvariable = file_dir, width = 48, font = "TkFixedFont" )

        widg.insert(0, self.inputFolder)
        widg.xview( END )
        widg.config( state = 'readonly')
        widg.config( bg = "light gray" )
        widg.grid( row = thisRow, column = 1, columnspan = 2, sticky = W)
        rowofwidgets.append(widg)

        widg = Button(self.topFrame, text = "Browse", command = (lambda file_dir = self.inputFolder, widget = widg : self.browse_input(file_dir, widget) ) )
        widg.grid( row = thisRow, column = 3, sticky = W )
        rowofwidgets.append(widg)

        widg = Button(self.topFrame, text = "-", width = 1)
        widg.config(command = (lambda myself = widg: self.topFrame_remove(myself)) )
        widg.grid( row = thisRow, column = 4, sticky = W)
        rowofwidgets.append(widg)

        self.topFrame.widgets.append(rowofwidgets)

        rowofwidgets = []
        widg = Button(self.topFrame, text = "+", width = 1, command = self.topFrame_insert)

        widg.grid( row = thisRow+1, column = 4, sticky = W)
        rowofwidgets.append(widg)
        self.topFrame.widgets.append(rowofwidgets)

        self.Root.update()

    def topFrame_remove(self, myself):

        if len(self.topFrame.widgets) > 4:
            widgets = self.topFrame.widgets.pop()
            for widget in widgets:
                widget.destroy()

            widgets = self.topFrame.widgets.pop()
            for widget in widgets:
                if type(widget) == StringVar:
                    widget.set('')
                    continue
                widget.destroy()

            row = len(self.topFrame.widgets) - 1
            thisRow = row + 1

            rowofwidgets = []
            widg = Button(self.topFrame, text = "+", width = 1, command = self.topFrame_insert)
            widg.grid( row = thisRow + 1, column = 4, sticky = W)
            rowofwidgets.append(widg)
            self.topFrame.widgets.append(rowofwidgets)
            self.topFrame.update()

        else:

            self.userNotification("Warning: Cannot Delete Last Two Inputs")

    def browse_input(self, filepath, widget):

        self.output_dir = filedialog.askopenfilename(parent = self.master, title = "PDF Input Folder", initialdir = filepath)
        #print(self.output_dir)
        if (type(self.output_dir) == str) and (self.output_dir != "") :
            if self.output_dir != "":
                widget.config ( state = NORMAL )
                widget.delete(0, END)
                widget.insert(0, self.output_dir)
                widget.xview( END )
                widget.config( state = "readonly" )

    def browse_output(self, filepath, widget):

        self.output_dir = filedialog.askdirectory(parent = self.master, title = "PDF Output File", initialdir = filepath)
        #print(self.output_dir)
        if (type(self.output_dir) == str) and (self.output_dir != "") :
            if self.output_dir != "":
                widget.config ( state = NORMAL )
                widget.delete(0, END)
                widget.insert(0, self.output_dir)
                widget.xview( END )
                widget.config( state = "readonly" )

    def mergeOperations(self):

        ########################
        ########################
        ########################
        ## Input File Names
        input_widgets = self.topFrame.widgets.copy()                           # widgets =   [ Initial Title Widget
                                                                               #               Input Row 1
                                                                               #               Input Row 2
                                                                               #               etc
                                                                               #               Ending [+] Button Widget]
                                                                               # Input Row = [ Label, String Variable, Entry, Browse Button, [-] Button]

        input_widgets.pop(0)                                                   # Ignore first title widget, remove it from list
        input_widgets.pop()                                                    # Ignore last [+] button widget, rmeove it from list


        ###############################
        ## List of Entry  Widgets
        input_entryWidgets = []
        for row in input_widgets:
            input_entryWidgets.append(row[2])

        #############################
        ## List of File Locations

        Files = [widget.get() for widget in input_entryWidgets]

        ############################
        ## Check File Location if actually a Folder Location

        Files = [file for file in Files if list(os.path.split(file))[-1] != ""]

        ############################
        ## Check if Files are actually Files

        valid_Files = []
        if len(Files) > 0:
            for file in Files:
                try:
                    fhandle = open(file, 'rb')
                    valid_Files.append(file)
                except:
                    split_file = os.path.split(file)
                    split_file = list(split_file)
                    split_file = split_file[-1]
                    self.userNotification("Error: cannot open input " + split_file)
        else:
            self.userNotification("Warning: No input Files")
            return None
        Files = valid_Files
        if not(len(Files) > 0):
            self.userNotification("Error: Input Files Do Not Exist or Cannot be Opened")
            return None

        #############################
        ## Check if Files are actually PDF's
        valid_Files = []
        if len(Files) > 0:
            for file in Files:
                split_file = os.path.split(file)
                split_file = list(split_file)
                split_file = split_file[-1]
                split_file = split_file.lower()
                if split_file.find(".pdf"):
                    valid_Files.append(file)
        else:
            self.userNotification("Error: Input Files Do Not Exist or Cannot be Opened")
            return None
        Files = valid_Files
        if not(len(Files) > 0):                                                # Returns error if no Files are PDF's
            self.userNotification("Warning: No input files ending in \".pdf\"")
            return None

        ######################
        ## Check Number of Files

        if not(len(Files) >= 2):
            self.userNotification("Warning: Not enough Input Files ending in \".pdf\"")
            return None

        ########################
        ########################
        ########################
        ## Obtain output File Name and Folder Location

        outputFile_Widget        = self.widg13
        outputFolder_Widget      = self.widg15

        outputFile = self.widg13.get()
        outputFolder = self.widg15.get()

        #######################
        ## Output File Name Specified (nonzero length)

        if not(len(outputFile) > 0):
            self.userNotification("Warning: Output File Name not Specified")
            return None

        #######################
        ## Output File Name, Remove .pdf

        outputFile = outputFile.lower()
        if (outputFile.find(".pdf")):
            location = outputFile.find(".pdf")
            outputFile = outputFile[0:location]
        outputFile = outputFile + ".pdf"


        ######################
        ## Output Folder Location
        if not(os.path.exists(outputFolder)):
            self.userNotification("Warning: Output Folder Path Does not Exist")

        ########################
        ########################
        ########################
        ## Merge Operations

        try:
            merge_handler  = PdfFileMerger()

            inputs = []                                                            # Open All of the Input Files
            for File in Files:
                in_File = open(File, 'rb')
                inputs.append(in_File)

            for handle in inputs:                                                  # Merge the input PDF's
                merge_handler.append(handle)

            out_File = open(outputFolder + outputFile, 'wb+')                         # Open the output File
            merge_handler.write(out_File)                                                  # Write the merged result to the output file

            for handle in inputs:                                                  # Close all of the input Files
                handle.close()
            out_File.close()                                                       # Close the output File

            if self.widg18_var.get() == True:
                os.startfile(outputFolder + outputFile)
                self.userNotification("Complete: Open Resulting PDF")
            if self.widg21_var.get() == True:
                os.startfile(outputFolder)
                self.userNotification("Complete: Open Containing Folder")

            self.userNotification()




        except:
            self.userNotification("Error: Something went wrong during merging")

    def bottom_NotificationBar(self):
        ''' Notification bar under the normal GUI widgets. Provides user feedback '''

        ## A frame for the bottom notifications bar
        self.bottomBar_Frame = Frame(self.master)

        ## Text widget
        self.bottomBar_Frame.string = StringVar()
        self.bottomBar_Frame.widg1 = Entry( self.bottomBar_Frame, textvariable = self.bottomBar_Frame.string )
        self.bottomBar_Frame.widg1.pack( side = LEFT, expand = YES, fill = 'x', anchor = W )
        self.bottomBar_Frame.widg1.ToolTip = TTip(self.bottomBar_Frame.widg1, text = "Displays Error Messages, and tells you when an operation is complete", time = 15000)

        ## Button widget acting as a colour notification
        self.bottomBar_Frame.widg2 = Button( self.bottomBar_Frame,  width = 2, height = 1, bd = 0, pady = 0) #bg = 'red',
        self.bottomBar_Frame.widg2.config( state = DISABLED )
        self.bottomBar_Frame.widg2.pack( side = RIGHT )
        self.bottomBar_Frame.widg2.ToolTop = TTip(self.bottomBar_Frame.widg2, text = "Red = Error\nYellow = Entry Missing\nGreen = Good\nGray = Nothing has happened yet", time = 15000)

    def userNotification(self, inputs = "Operation Complete"):

        ## Get current time
        date_time = datetime.now()                                             # Obtain Current Date and Time
        log = date_time.strftime("%G %b %d %I_%M%p") + " "                     # Something that shows the Time, Edit Required

        inputs_temp = inputs.split(":")
        if debugging == True: print(inputs_temp)

        ## Change Colour indicator
        if inputs_temp[0] == "Input Error":
            self.bottomBar_Frame.widg2.config( bg = "yellow" )
        elif inputs_temp[0] == "Operation Error":
            self.bottomBar_Frame.widg2.config( bg = "yellow")
        else:
            self.bottomBar_Frame.widg2.config( bg = "red" )


        if inputs_temp[0] == "Operation Complete":
            self.bottomBar_Frame.widg2.config( bg = 'green' )

        inputs = date_time.strftime("%I:%M%p ") + inputs

        ## Write Text to Screen
        self.bottomBar_Frame.widg1.config( state = NORMAL )
        self.bottomBar_Frame.widg1.delete(0, END)
        self.bottomBar_Frame.widg1.insert(0, inputs)
        self.bottomBar_Frame.widg1.config( state = "readonly" )


        ## Update Error and Log Directory
        try:
            file = open(self.logFile, 'a')
            file.write(inputs)
            file.close()
        except:
            self.bottomBar_Frame.widg1.config( state = NORMAL )
            self.bottomBar_Frame.widg1.delete(0, END)
            self.bottomBar_Frame.widg1.insert(0, "Log File Write Error")
            self.bottomBar_Frame.widg1.config( state = "readonly" )

    def pack_NotificationBar(self):
        ## Make sure to pack last
        self.bottom_NotificationBar()
        self.bottomBar_Frame.pack(expand = YES, fill = 'x')


    def createMenu(self):

        self.menubar = Menu(self.master)
        self.Root.config(menu = self.menubar)


        FileMenu = Menu(self.menubar, tearoff = False)
        FileMenu.add_command(label = "Select Input Folder", command = self.inputFile_folder)
        FileMenu.add_command(label = "Select Output Folder", command = self.outputFile_folder)
        FileMenu.add_command(label = "Exit", command = self.Root.destroy )
        self.menubar.add_cascade(label = "File", menu = FileMenu)

        clearMenu = Menu(self.menubar, tearoff = False)
        clearMenu.add_command(label = "Clear Input", command = self.input_clear)
        clearMenu.add_command(label = "Clear output", command = self.output_clear )
        clearMenu.add_command(label = "Clear All", command = self.input_output_clear )
        self.menubar.add_cascade(label = "Clear Options", menu = clearMenu)


        helpMenu = Menu(self.menubar, tearoff = False)
        helpMenu.add_command(label = "Help Files", command = self.help_menu)
        self.menubar.add_cascade(label = "Help", menu = helpMenu)


        aboutMenu = Menubutton(self.menubar)
        self.menubar.add_cascade(label = "About", menu = aboutMenu, command = self.about)

    def input_clear(self):

        current_dir = os.getcwd()
        if ( os.path.exists( current_dir + os.sep + "input" ) == False ):
                os.mkdir( current_dir + os.sep + "input" )
        current_dir = current_dir + os.sep + "input" + os.sep

        self.inputFolder = current_dir

        widgets = self.topFrame.widgets.copy()
        widgets.pop()
        widgets.pop(0) #Label | StringVar | Entry | Browse Button | - Button

        for widget in widgets:
            entry_widget = widget[2]
            browse_widget = widget[3]

            entry_widget.config ( state = NORMAL )
            entry_widget.delete(0, END)
            entry_widget.insert(0, self.inputFolder)
            entry_widget.xview( END )
            entry_widget.config( state = "readonly" )
            browse_widget.config(command = (lambda file_dir = self.inputFolder, widget = entry_widget : self.browse_input(file_dir, widget) ))

        self.Root.update()

    def output_clear(self):

        current_dir = os.getcwd()
        if ( os.path.exists( current_dir + os.sep + "output" ) == False ):
                os.mkdir( current_dir + os.sep + "output" )
        current_dir = current_dir + os.sep + "output" + os.sep
        self.outputFolder = current_dir

        self.widg15.config( state = NORMAL )


        self.widg15.delete(0, END)
        self.widg15.insert(0, self.outputFolder)
        self.widg15.xview(END)
        self.widg15.config( state = "readonly" )

        self.widg16.config( command = (lambda file_dir = self.outputFolder, widget = self.widg15 : self.browse_output(file_dir, widget) ) )

        self.Root.update()

    def input_output_clear(self):
        self.input_clear()
        self.output_clear()

    def inputFile_folder(self):

        current_dir = os.getcwd()
        if ( os.path.exists( current_dir + os.sep + "input" ) == False ):
                os.mkdir( current_dir + os.sep + "input" )
        current_dir = current_dir + os.sep + "input" + os.sep
        inputFolder = filedialog.askdirectory(parent = self.master, title = "Input File Default Path", initialdir = current_dir)

        if inputFolder != "" :
            self.inputFolder = inputFolder


        widgets = self.topFrame.widgets.copy()
        widgets.pop()
        widgets.pop(0) #Label | StringVar | Entry | Browse Button | - Button

        for widget in widgets:
            entry_widget = widget[2]
            browse_widget = widget[3]

            entry_widget.config ( state = NORMAL )
            entry_widget.delete(0, END)
            entry_widget.insert(0, self.inputFolder)
            entry_widget.xview( END )
            entry_widget.config( state = "readonly" )
            browse_widget.config(command = (lambda file_dir = self.inputFolder, widget = entry_widget : self.browse_input(file_dir, widget) ))

        self.Root.update()


    def outputFile_folder(self):

        current_dir = os.getcwd()
        if ( os.path.exists( current_dir + os.sep + "output" ) == False ):
                os.mkdir( current_dir + os.sep + "output" )
        current_dir = current_dir + os.sep + "output" + os.sep
        outputFolder = filedialog.askdirectory(parent = self.master, title = "Output File Default Path", initialdir = current_dir)

        if outputFolder != "" :
            self.outputFolder = outputFolder

        self.widg15.config( state = 'normal')
        self.widg15.delete(0, END)
        self.widg15.insert(0, self.outputFolder)
        self.widg15.xview(END)
        self.widg15.config( state = "readonly" )

        self.widg16.config( command = (lambda file_dir = self.outputFolder, widget = self.widg16 : self.browse_output(file_dir, widget) ) )

    def help_menu(self):
        try:
            os.startfile("SupportFiles" + os.sep + "Help.pdf")                     # Start Help file
        except:
            self.userNotification("Error: Support File Not Found")


    def about(self, event = None):

        if debugging == True: print( "About Popup Information" )

        ## Obtain Parent window handle
        parentName = self.master.winfo_parent()
        parent     = self.master._nametowidget(parentName)                 # event.widget is your widget

        text = "Chad Unterschultz \nBsc in Electrical Engineering\nMeng in Control Systems"

        ## Create window dependent on parent window
        self.about_window = Toplevel(parent)
        self.about_window.focus_set()
        self.about_window.title("About the author")
        self.about_window.widg1 = Label(self.about_window, text = text)
        self.about_window.widg1.grid(row = 0, column = 0, sticky = W)
        self.about_window.widg2 = Button(self.about_window, text = "Okay", command = self.about_window.destroy)
        self.about_window.widg2.grid(row = 1, column = 0, sticky = E)
        self.about_window.resizable(False, False)
        self.about_window.update()

        ## Parent window location, top left corner
        gui_x_location = parent.winfo_rootx()
        gui_y_location = parent.winfo_rooty()

        if debugging == True: print("gui Location: ", gui_x_location, gui_y_location)

        ## Parent window dimensions
        gui_height = parent.winfo_height()
        gui_width =  parent.winfo_width()

        if debugging == True: print("gui size: ", gui_height, gui_width)

        ## Dependent window dimensions
        popup_height = self.about_window.winfo_height()
        popup_width  = self.about_window.winfo_width()

        if debugging == True: print("popup size: ", popup_height, popup_width)

        ## Place dependent window in center of parent window, find the buffer space
        Top_space = (gui_height - popup_height) / 2                            # Space above and below widget
        Top_space = int(Top_space)                                             # Round down
        Side_space = (gui_width - popup_width) / 2                             # Space to either side of widget
        Side_space = int(Side_space)                                           # Round down

        if debugging == True: print("Space: ", Top_space, Side_space)

        ## Place dependent window in center of parent window, factor in buffer space
        new_x = gui_x_location + Side_space
        new_y = gui_y_location + Top_space                                     # This Doesn't seem to be perfectly centered on the window
                                                                               # Horizontally centered, but not vertically
        self.about_window.wm_geometry("+%d+%d" % (new_x, new_y))
        self.about_window.update()                                             # Force GUI program to update

        if debugging == True: print("Location: ", new_x, new_y)

    def PopupMenu(self, event = None):

        ## Popup Menu options
        self.Menu = Menu(self.master, tearoff = 0)
        self.Menu.add_command(label  = "Cut",   command = self.popupCut )
        self.Menu.add_command(label  = "Copy",  command = self.popupCopy)
        self.Menu.add_command(label  = "Clear", command = self.popupClear )
        self.Menu.add_command(label  = "Paste", command = self.popupPaste )




    def PopupMenu_feature(self, Widget, event = None):
        ## When right click, popup menu appears
        Widget.bind("<Button-3>", self.showMenu, add = "+")

    def showMenu(self, event = None):
        ## Menu 'posts' to the screen at the x-y location of the button click
        self.Menu.post(event.x_root, event.y_root)


    def give_Popup(self):

        ## Give all widgets in the top frame a copy/paste popup window
        for widget in self.topFrame.winfo_children():                      # List of all widgets in frame
            if isinstance(widget, Entry) | isinstance(widget, Text):           # Check if any widgets are Entry or Text
                self.PopupMenu_feature(widget)                                 # Give popup features to Entry or Text widgets

        ## Give all widgets in the Bottom frame a copy/paste popup window
        for widget in self.bottomFrame.winfo_children():                   # List of all widgets in frame
            if isinstance(widget, Entry) | isinstance(widget, Text):           # Check if any widgets are Entry or Text
                self.PopupMenu_feature(widget)                                 # Give popup features to Entry or Text Widgets




    def popupClear(self):

        ## Gets the handle for the currently selected widget
        widget = self.master.focus_get() #Current Widget of interest
        text = "Empty"


        ## Cannot Clear an Entry widget, read only
        if isinstance(widget, Entry):                                          #entry type widget
            state = widget.config()
            state = state['state']
            state = state[-1]

            widget.config(state = "normal")
            widget.delete(0, END)
            widget.config(state = state)

            #self.master.bell
            #self.userNotification("Cannot Clear")

        ## Clear Text widget
        if isinstance(widget, Text):                                           # Test if widget is a Text widget
            state = widget.cget('state')                                       # Save current widget state
            widget.config( state = NORMAL )                                    # Convert state to NORMAL, so that the widget can be interacted with
            index = widget.delete(1.0, 'end')                                  # Delete all widget contents
            widget.config( state = state )                                     # Return widget to its prior state

        if debugging == True: print("Clear complete")

    def popupPaste(self):

        ## Obtain handle to the Entry of Text widget currently selected
        widget = self.master.focus_get() #Current Widget of interest
        text = "Empty"

        ## Cannot Paste to an Entry widget as those are readonly
        if isinstance(widget, Entry):                                          # Check if Entry type widget
            self.master.bell
            self.userNotification("Warning: Cannot Paste")

        ## Paste to a Text widget
        if isinstance(widget, Text):                                           # Check if Text type widget
            state = widget.cget('state')                                       # Get current  state, hold for later
            widget.config( state = NORMAL )                                    # Convert to NORMAL mode so that we know it is editable
            index = widget.index(INSERT)                                       # Looks for current cursor location
            if debugging == True: print("index", index)
            text = self.selection_get(selection = 'CLIPBOARD')                 # Gets text from Clipboard
            widget.insert(index, text)                                         # Insert text from clipboard to cursor location
            widget.config( state = state )                                     # Return widget to the state it was before we touched it



        print("Paste complete")
        print("Text: ", text)

    def popupCopy(self):

        ## Obtain handle to the Entry of Text widget currently selected
        widget = self.master.focus_get() #Current Widget of interest
        text = "Empty"

        ## Copy from Entry widget means to copy everything
        if isinstance(widget, Entry):                                          # Check if entry type widget
            state = widget.cget('state')                                       # Get Current Widget  State
            widget.config( state = NORMAL )                                    # Make widget NORMAL so that it can be interacted with
            text = widget.get()                                                # Get all of the current text
            widget.config( state = state )                                     # Restore State to the way it was before
            self.clipboard_clear()                                             # Clear Clipboard to copy to it
            self.clipboard_append(text)                                        # Append to empty clipboard, equivalent to a copy

        if isinstance(widget, Text):                                           # Check if Text type widget
            state = widget.cget('state')                                       # Get current Widget State
            widget.config( state = NORMAL )                                    # Make widget NORMAL so that it can be interacted with

            ## Check if text is selected
            inrange = widget.tag_ranges("sel")                                 # Check if Text is selected
            if inrange == True:                                                # Text Selected
                text = widget.get('sel.first', 'sel.last')                     # Get the selected text

            else:                                                              # Text not selected
                self.userNotification("Warning: No Text Selected")

            widget.config( state = state )                                     # Return widget state to the way is was before

            ## Copy text to the clipboard
            self.clipboard_clear()                                             # Clear clipboard to copy to it
            self.clipboard_append(text)                                        # Append to the empty clipboard


        if debugging == True: print("copy complete")
        if debugging == True: print("Text: ", text)
        pass



    def popupCut(self):

        ## Obtain handle to the Entry or Text widget currently selected
        widget = self.master.focus_get() #Current Widget of interest
        text = "Empty"

        ## Cannot Cut from Entry widget, editing disabled
        if isinstance(widget, Entry):                                          # Check if widget is an "Entry" type
            self.master.bell
            self.userNotification("Warning: Cannot Cut")

        ## Cut from Text widget
        if isinstance(widget, Text):                                           # Check if widget is a "Text" type
            state = widget.cget('state')                                       # Obtain current state of widget, NORMAL or DISABLED
            widget.config( state = NORMAL )                                    # Change widget to NORMAL so that it can be edited
            inrange = widget.tag_ranges("sel")                                 # Check the Current Widget Highlighting
            if inrange == True:                                                # If something is highlighted, then true
                text = widget.get('sel.first', 'sel.last')                     # Copy what is highlighted
                widget.delete('sel.first', 'sel.last')                         # Delete what is highlighted (effectively a cut)
            else:                                                              # Nothing is highlighted
                self.userNotification("Warning: No Text Selected")                      # Inform the user that nothing was highlighted
            widget.config( state = state )                                     # Restore state back to normal

            self.clipboard_clear()                                             # Ensure Clipboard is empty before copying to it
            self.clipboard_append(text)                                        # Append to an empty clipboard

        if debugging == True: print("cut complete")                            # To help aid debugging
        if debugging == True: print("Text: ", text)









if __name__ == "__main__":

    debugging = True

    Root = Tk()

    Root.title("PDF Stitcher")



    Frame_test = Frame(Root)
    Frame_test.pack()
    test = stitcher(Frame_test, Root)

    Root.mainloop()




