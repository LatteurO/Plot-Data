from dataImport import ImportData
from plotLine import PlotLine
import numpy  as np
class ImportLTSpiceData (ImportData):
    y = []
    x = []
    titleC=None
    def __init__(self,file):
        self.file=file
        cLine = 0;
        with  open(self.file, 'r') as fichier:
            line = fichier.readline()

            # Compte le nombre de donnees
            while (line != ""):
                cLine += 1
                line = fichier.readline()


        # *******************reouverture du flux d'entree
        with open(self.file, 'r') as fichier:
            line = fichier.readline()
            self.titleC = line.split("\t")
            nbrElement = len(self.titleC)

            line = fichier.readline()
            y = []
            x = []

            for i in range(nbrElement):
                y.append([])
                x.append([])

            # donnees[0]=line.split("\t")
            # devut des nombre

            for i in range(cLine):
                s = line.split("\t")
                s = np.array(s)

                if len(s) != nbrElement:
                    break;
                # s.shape=(1,nbrElement);
                for i in range(1, nbrElement):
                    x[i].append(float(s[0]))
                    y[i].append(float(s[i]))

                line = fichier.readline()
            self.x=x[1:]
            self.y=y[1:]
        self.titleC=self.titleC[1:]
    def getTitles(self):
        return self.titleC

    def get_plot_lines(self):
        lines=[]
        for i in range(len(self.x)):
            line = PlotLine(xdata=self.x[i],ydata=self.y[i])
            line.set_legend(self.getTitles()[i])
            lines.append(line)
        return lines
