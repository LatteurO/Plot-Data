from matplotlib import pyplot as plt
from plotLine import PlotLine
import json

class Plot():
    title = ''
    showLegend = True
    xlabel = ''
    ylabel = ''
    x_limit_start = None
    x_limit_end = None
    y_limit_start = None
    y_limit_end = None
    plotLines = []
    has_grid=False



    def __init__(self,file_source=None):
        #TODO: load plot from file
        print()
        if file_source is not None:
            with open(file_source,) as read_file:
                data=json.load(read_file)

                if(data['version']==0.1):
                    self.title=data['title']
                    self.xlabel=data['xlabel']
                    self.ylabel=data['ylabel']
                    self.plotLines=[]
                    self.showLegend=data['legend']
                    self.has_grid=data['grid']
                    for line_data in data['plot_lines']:
                        self.plotLines.append(PlotLine(json_data=line_data))
                        print(line_data)

    def show_plot(self):
        plt.clf()
        plt.figure
        plt.title(self.get_title())

        count = 0
        for plot_line in self.get_plot_lines():
            if plot_line.is_enable():
                if plot_line.get_color_code() is not None:
                    plt.plot(plot_line.get_x_data(), plot_line.get_y_data(),plot_line.get_color_code(),label=plot_line.get_legend())
                else:
                    plt.plot(plot_line.get_x_data(), plot_line.get_y_data(),label=plot_line.get_legend())
                count += 1

        if (self.x_limit_end is not None ) and (self.x_limit_start is not None):
            plt.xlim(self.x_limit_start,self.x_limit_end)
        if (self.y_limit_end is not None) and (self.y_limit_start is not None):
            plt.ylim(self.y_limit_start, self.y_limit_end)

        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        if self.showLegend:
            plt.legend()

        if self.has_grid:
            plt.grid()
        plt.show()

    def save_plot(self,file):
        with open(file, 'w') as outfile:
            to_print = {
                'version': 0.1,
                'title': self.title,
                'xlabel': self.xlabel,
                'ylabel': self.ylabel,
                'legend':self.showLegend,
                'grid':self.has_grid,
                'plot_lines': [i.print_json() for i in self.plotLines]
            }
            print(to_print)
            json.dump(to_print,outfile)

    def set_grid_activate(self,activate_grid):
        self.has_grid=activate_grid

    def set_xlabel(self, xlabel):
        self.xlabel = xlabel

    def set_ylabel(self, ylabel):
        self.ylabel = ylabel

    def get_title(self):
        return self.title

    def get_label(self):
        return self.xlabel, self.ylabel

    def setTitle(self, title):
        self.title = title

    def enableLegend(self):
        self.showLegend = True

    def disableLegend(self):
        self.showLegend = False

    def addPlotLine(self, plotLine):
        self.plotLines.append(plotLine)

    def get_plot_lines(self):
        return self.plotLines

    def remove_plot_line(self, plot_line):
        self.plotLines.remove(plot_line)

    def set_x_limit(self, xlimit):
        if xlimit is None:
            self.x_limit_start, self.x_limit_end = [None, None]
        else:
            self.x_limit_start, self.x_limit_end = xlimit

    def set_y_limit(self, ylimit):
        if ylimit is None:
            self.y_limit_start, self.y_limit_end = [None, None]
        else:
            self.y_limit_start, self.y_limit_end = ylimit

    def get_x_limit(self):
        if (self.x_limit_end is not None ) and (self.x_limit_start is not None):
            return self.x_limit_start,self.x_limit_end

        return None

    def get_y_limit(self):
        if (self.y_limit_end is not None) and (self.y_limit_start is not None):
            return self.y_limit_start, self.y_limit_end

        return None

    def show_legend(self):
        return self.showLegend

    def show_grid(self):
        return self.has_grid
