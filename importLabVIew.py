from dataImport import ImportData
from plotLine import PlotLine
class ImportLabView(ImportData):
    y=[]
    x=[]
    title=None
    def __init__(self,file):
        with open(file, 'r') as fichier:
            line = fichier.readline()  # sep=,
            if (line.__contains__("sep") == False):
                raise Exception("Not LabView Format")
            line = fichier.readline()  # title
            line = fichier.readline().split(",")

            xdata = []
            ydata = []
            if (len(line) == 3):
                # exemple labview1.csv
                line = fichier.readline()  # to,dt,y
                data = line.replace("\"", "").split(",")
                tO = float(data[0])
                dt = float(data[1])
                n = int(data[2].replace("[", "").split("]")[0])
                data = line.split("{")[1].split("}")[0]
                data = data.split(",")
                t = tO
                for e in data:

                    s = e.replace("i", "j").replace(" ", "")
                    if (s.__contains__("....")):
                        break
                    xdata.append(t)
                    ydata.append(complex(s).real)
                    t += dt

            elif (len(line) == 2):

                # exemple labview.csv

                line = fichier.readline()  # inverval
                dt = float(line.replace("\"", "").split(",")[1])

                line = fichier.readline()  # first dataline

                while line != "" and line != "\n":
                    data = line.replace("\"", "").split(",")

                    xdata.append(float(data[0]))
                    ydata.append(float(data[1]))
                    line = fichier.readline()

            self.x=xdata
            self.y=ydata
            self.title=''

    def get_plot_lines(self):
        return [PlotLine(xdata=self.x,ydata=self.y)]