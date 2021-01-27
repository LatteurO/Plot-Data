from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import filedialog as fd
from tkinter import Scrollbar
from PIL import ImageTk,Image

from plot import Plot
from PlotLine import PlotLine
from importLtSpiceData import ImportLTSpiceData
from importMyDaq import ImportMyDaq
from importLabVIew import ImportLabView


class Interface(Frame):
    title = None
    plot = None
    lineWidgets = []


    def __init__(self, window, **kwargs):
        self.window = window
        self.plot = Plot()

        Frame.__init__(self, window, width=1000, height=700, **kwargs)
        self.add_menubar()

        Label(self.window, text="Create a graph").pack(side=TOP)
        # Title
        title_fram = LabelFrame(self.window, text='Title', padx=40, pady=10)
        title_fram.pack(fill="both", expand="no")
        self.title = StringVar()
        def upt_title(*args):
            self.plot.setTitle(self.title.get())

        self.title.trace_add("write", upt_title)
        Entry(title_fram, textvariable=self.title).pack()

        # Axis name
        self.add_axe_name_frame()

        # limit
        self.add_xy_limit_frame()

        self.add_plot_option_frame()
        self.lineFrame = LabelFrame(self.window, text="Lines to plot")
        self.lineFrame.pack(fill="both",expand='yes')

        Button(self.window, text='plot', command=self.show_plot).pack()

    def update_title_frame(self,plot):
        self.title.set(plot.get_title())

    def load_plot(self,plot):
        self.remove_lines_widget()
        self.plot=plot
        self.title.set(plot.get_title())
        self.update_axe_name_frame(plot)



    def add_xy_limit_frame(self):


        limit_frame = LabelFrame(self.window, text="Limit (ex: 0;0.1)", padx=40, pady=10)
        limit_frame.pack(fill="both", expand="no")
        self.check_xLimit = IntVar()
        Checkbutton(limit_frame, text="Abscissa :", variable=self.check_xLimit, command=self.update_xlim_frame).pack(side=LEFT)
        self.xLim_text = StringVar()

        def upt_xlim(*args):
            x_slim_split=self.xLim_text.get().__str__().split(';')
            #TODO:CHECK VALID LIMIT SEMENTIC
            if (self.check_xLimit.get() == 0):
                self.plot.set_x_limit(None)
            elif (self.check_xLimit.get()==1) and len(x_slim_split)==2:
                x_start, x_end=x_slim_split
                self.plot.set_x_limit([float(x_start),float(x_end)])

        self.xLim_text.trace_add("write", upt_xlim)
        self.xLim_box = Entry(limit_frame, textvariable=self.xLim_text)
        self.xLim_box.config(state=DISABLED)
        self.xLim_box.pack(side=LEFT)
        self.check_yLimit = IntVar()
        Checkbutton(limit_frame, text="Ordinate: ", variable=self.check_yLimit, command=self.update_ylim_frame).pack(side=LEFT)
        self.yLim_text = StringVar()

        def upt_ylim(*args):
            y_slim_split = self.yLim_text.get().split(';')
            # TODO:CHECK VALID LIMIT SEMENTIC
            if(self.check_yLimit.get()==0):
                self.plot.set_y_limit(None)
            elif (self.check_yLimit.get() == 1) and len(y_slim_split) == 2:
                y_start, y_end=y_slim_split
                self.plot.set_y_limit([float(y_start),float(y_end)])

        self.yLim_text.trace_add("write", upt_ylim)
        self.yLim_box = Entry(limit_frame, textvariable=self.yLim_text)
        self.yLim_box.pack(side=LEFT)
        self.yLim_box.config(state=DISABLED)

    def update_ylim_frame(self):
        if self.check_yLimit.get() == 1:
            self.yLim_box.config(state=NORMAL)
        else:
            self.yLim_box.config(state=DISABLED)

    def update_xlim_frame(self):
        if self.check_xLimit.get() == 1:
            self.xLim_box.config(state=NORMAL)
        else:
            self.xLim_box.config(state=DISABLED)

    def update_xy_limit_frame(self,plot):
        x_lim=plot.get_x_limit()
        if( x_lim is None):
            self.check_xLimit.set(0)
        else:
            self.check_xLimit.set(1)
            self.xLim_text.set(str(x_lim[0])+';'+str(x_lim[1]))
        self.update_xlim_frame()

        y_lim = plot.get_y_limit()
        if (y_lim is None):
            self.check_yLimit.set(0)
        else:
            self.check_yLimit.set(1)
            self.yLim_text.set(str(y_lim[0]) + ';' + str(y_lim[1]))
        self.update_ylim_frame()


    def add_axe_name_frame(self):
        cadre_axe = LabelFrame(self.window, text="Axis name: ", padx=40, pady=10)
        cadre_axe.pack(fill="both", expand="no")
        axisLabel = Label(cadre_axe, text="Abscissa :").pack(side=LEFT)
        self.axis_Text = StringVar()
        def upt_xlabel(*args):
            self.plot.set_xlabel(self.axis_Text.get())
        self.axis_Text.trace_add("write", upt_xlabel)
        axe_box = Entry(cadre_axe, textvariable=self.axis_Text, width=20).pack(side=LEFT)
        ordonneeLabel = Label(cadre_axe, text="Ordinate:").pack(side=LEFT)
        self.ordonnee_Text = StringVar()
        def upt_ylabel(*args):
            self.plot.set_ylabel(self.ordonnee_Text.get())
        self.ordonnee_Text.trace_add("write",upt_ylabel)
        ordonnee_box = Entry(cadre_axe, textvariable=self.ordonnee_Text, width=20).pack(side=LEFT)

    def update_axe_name_frame(self,plot):
        xlabel,ylabel=plot.get_label()
        self.axis_Text.set(xlabel)
        self.ordonnee_Text.set(ylabel)

    def add_plot_option_frame(self):

        def grid_btn_click():
            if self.grid_check.get()==1:
                self.plot.set_grid_activate(True)
            else:
                self.plot.set_grid_activate(False)

        plot_options_frame = LabelFrame(self.window, text='Plot options')
        plot_options_frame.pack(fill="both",expand='no')

        self.grid_check=IntVar(value=0)
        Checkbutton(plot_options_frame,variable=self.grid_check,command=grid_btn_click).pack(side=LEFT)
        Label(plot_options_frame,text='Grid').pack(side=LEFT)

        def legend_btn_click():
            if self.legend_check.get()==1:
                self.plot.enableLegend()
            else:
                self.plot.disableLegend()
        self.legend_check = IntVar(value=1)
        Checkbutton(plot_options_frame, variable=self.legend_check, command=legend_btn_click,).pack(side=LEFT)
        Label(plot_options_frame, text='Legend').pack(side=LEFT)

    def update_plot_opt_frame(self):
        self.legend_check.set(self.plot.show_legend())
        self.grid_check.set(self.plot.show_grid())

    def add_line_widget(self, plot_line):

        def add_color_chooser_btn(widget_frame):

            def color_choosen():
                color_resp_rgb, color_resp_hex = askcolor(title="Choose color")
                if color_resp_hex != None:
                    color_chooser_btn.config(bg=color_resp_hex)
                    plot_line.set_colot(color_resp_hex)

            def reset_color_choosen_bg():
                color_chooser_btn.config(bg=origin_btn_color)
                plot_line.set_colot(None)

            color_chooser_btn = Button(widget_frame, text='color', command=color_choosen)
            color_chooser_btn.pack(side=LEFT)
            origin_btn_color = color_chooser_btn.cget("background")

            if plot_line.get_color_code() is not None:
                color_chooser_btn.config(bg=plot_line.get_color_code())


            m = Menu(widget_frame, tearoff=0)
            m.add_command(label="default color", command=reset_color_choosen_bg)

            def right_click_color(event):
                m.tk_popup(event.x_root, event.y_root)

            color_chooser_btn.bind("<Button-3>", right_click_color)

        def enable_or_disable_line(*args):
            print("check enable?")
            if is_selected.get() == 1:
                plot_line.enable()
                legent_entry.config(state=NORMAL)
            else:
                plot_line.disable()
                legent_entry.config(state=DISABLED)

        def remove_line(*args):
            widget_frame.destroy()
            self.plot.remove_plot_line(plot_line)


        # UI PART
        widget_frame = Frame(self.lineFrame)
        widget_frame.pack()

        is_selected = IntVar()
        check = Checkbutton(widget_frame, variable=is_selected, command=enable_or_disable_line)
        check.pack(side=LEFT)




        Label(widget_frame, text="legend:").pack(side=LEFT)

        legend = StringVar()
        def upt_legend(*args):
            plot_line.set_legend(legend.get())
        legend.trace_add("write",upt_legend)
        legent_entry = Entry(widget_frame, textvariable=legend)
        legent_entry.pack(side=LEFT)

        if plot_line.is_enable():
            is_selected.set(1)
            check.select()
        else:
            is_selected.set(0)
            check.deselect()
            legent_entry.config(state=DISABLED)

        if plot_line.get_legend() is not None:
            legend.set(plot_line.get_legend())

        add_color_chooser_btn(widget_frame)

        remove_btn = Button(widget_frame, text="X", command=remove_line)
        remove_btn.pack(side=LEFT)

        line_widget = {
            'plot_line': plot_line,
            'legend': legend,
            'frame':widget_frame
        }

        self.lineWidgets.append(line_widget)

    def update_lines_frame(self):
        self.remove_lines_widget()
        plot_lines=self.plot.get_plot_lines()
        for line in plot_lines:
            self.add_line_widget(line)

    def remove_lines_widget(self):
        for line_widget in self.lineWidgets:
            line_widget['frame'].destroy()
        self.lineWidgets=[]




    def save_plot(self):
        file=fd.asksaveasfilename(filetypes=(('All Files', '*.*'),))
        print(file)
        self.plot.save_plot(file)

    def open_plot(self):
        file=fd.askopenfilename(title = "Select file",filetypes =(("all files","*.*"),))
        print(file)
        plot=Plot(file_source=file)
        self.plot = plot
        self.update_UI()

    def update_UI(self):
        self.update_title_frame(self.plot)
        self.update_axe_name_frame(self.plot)
        self.update_xy_limit_frame(self.plot)
        self.update_lines_frame()
        self.update_plot_opt_frame()
        self.update_plot_opt_frame()

    def add_menubar(self):
        menu = Menu(self.window)

        import_file_menu = Menu(menu, tearoff=0)
        #import_file_menu.add_command(label="Plot data")
        import_file_menu.add_command(label="LTSpice", command=self.import_LTSpice)
        import_file_menu.add_command(label="MyDaq",command=self.import_mydaq)
        import_file_menu.add_command(label="LabView",command=self.import_labview)

        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label="Open",command=self.open_plot)
        file_menu.add_command(label="Save",command=self.save_plot)

        def add_cmd_menu(parent_menu):

            cmd_menu = Menu(menu, tearoff=0)
            def upt_xylim():
                self.update_xy_limit_frame(self.plot)
            cmd_menu.add_command(label='Update Limit Frame',command=upt_xylim)
            def upt_label():
                self.update_axe_name_frame(self.plot)
            cmd_menu.add_command(label='update axis name',command=upt_label)
            def upt_plot_lint():
                self.update_lines_frame()
            cmd_menu.add_command(label='update plot line',command=upt_plot_lint)

            def rm_plot_lines():
                self.remove_lines_widget()
            cmd_menu.add_command(label='remove plot line frame',command=rm_plot_lines)


            parent_menu.add_cascade(label="cmd", menu=cmd_menu)



        menu.add_cascade(label="File", menu=file_menu)
        menu.add_cascade(label="Import file", menu=import_file_menu)
        #add_cmd_menu(menu)


        self.window.config(menu=menu)

    def import_LTSpice(self):
        self.import_datas(ImportLTSpiceData)

    def import_mydaq(self):
        self.import_datas(ImportMyDaq)

    def import_labview(self):
        self.import_datas(ImportLabView)

    def import_datas(self, Import_stategy_class):
        file = fd.askopenfilename()
        if file != None:
            import_plot_datas = Import_stategy_class(file)
            for line in import_plot_datas.get_plot_lines():
                self.plot.addPlotLine(line)
                self.add_line_widget(line)

    def show_plot(self):

        self.plot.show_plot()


window = Tk()

window.title("Plot")
# window.resizable(width=False,height=False)
interface = Interface(window)
interface.mainloop()
interface.destroy()
