import json

class PlotLine():
    xdata=[]
    ydata=[]
    legend=None
    color=None
    visible=True

    def __init__(self,xdata=None,ydata=None,json_data=None):
        if(json_data is not None):
            data = json_data
            print(data)
            self.legend = data['legend']
            self.visible = data['enable']
            self.xdata = [float(x) for x in data['xdata']]
            self.ydata = [float(y) for y in data['ydata']]
            self.color = data['color']
        else:
            if(len(xdata)!=len(ydata)):
                raise Exception("len(xdata)!=len(ydata)")
            self.xdata=xdata
            self.ydata=ydata

    def print_json(self):
       to_print={
           'legend':self.legend,
           'enable':self.visible,
           'xdata':self.xdata,
           'ydata':self.ydata,
           'color':self.color
       }
       return to_print

    def is_enable(self):
        return self.visible

    def set_colot(self,color):
        self.color=color

    def get_color_code(self):
        return self.color

    def enable(self):
        self.visible=True

    def disable(self):
        self.visible=False

    def set_legend(self,legend):
        self.legend=legend

    def get_legend(self):
        return self.legend

    def get_x_data(self):
        return self.xdata

    def get_y_data(self):
        return self.ydata
