from dataImport import ImportData
from plotLine import PlotLine
class ImportMyDaq(ImportData):

    def __clean(self,nbr):
        return nbr.replace("E", "e").replace(",", ".")

    legend=[]
    xdata=[]
    ydata=[]

    def __init__(self,file):
        with open(file, 'r') as fichier:
            line = fichier.readline()

            # Première ligne
            legend = line.split("\t")
            Element = [];
            for E in legend:
                if E != ' ' and E != '\n' and E != '':
                    Element.append(E)

            self.legend = Element[1:]

            line = fichier.readline();
            line = fichier.readline()
            line = line.split("\t")
            if (line[0] != "delta t"):
                raise Exception
            line = line[1:]
            delta = []

            for i in line:
                if (i != '' and i != '\n'):
                    delta.append(float(self.__clean(i)))
            # check
            if (len(delta) != len(self.legend)):
                print('Erreur find delta')
                raise Exception

            line = fichier.readline();
            line = fichier.readline();
            line = fichier.readline();  # première ligne de donnée

            xdata = []
            ydata = []
            for i in range(len(self.legend)):
                xdata.append([])
                ydata.append([])

            while (line != ""):
                line = line.split("\t")
                index = 0
                for j in range(0, len(line)):
                    if (j % 2 == 0):
                        if (len(xdata[index]) == 0):
                            lastx = -1 * delta[index];
                        else:
                            lastx = xdata[index][len(xdata[index]) - 1]

                        xdata[index].append(lastx + delta[index])
                    else:
                        ydata[index].append(float(self.__clean(line[j])))
                        index += 1
                line = fichier.readline()


            self.xdata=xdata
            self.ydata=ydata

    def get_plot_lines(self):
        lines = []
        for i in range(len(self.xdata)):
            line = PlotLine(xdata=self.xdata[i], ydata=self.ydata[i])
            line.set_legend(self.legend[i])
            lines.append(line)
        return lines