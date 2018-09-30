import wx
from lib.queries import *
from lib.db import Query
from lib.reader import READER
from lib.solver import solve
from lib.plot import TSP_PLOT

class PREFERENCES_DIALOG(wx.Dialog):
    def __init__(self,parent,reader):
        super(PREFERENCES_DIALOG,self).__init__(parent,title="Preferences",size=(450,200))
        panel = wx.Panel(self)
        self.reader = reader

        wx.StaticText(panel,label="TSP Directory Path",pos=(5,5)).SetFont(
            wx.Font(10,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))

        self.path = wx.TextCtrl(panel,pos=(5,30),size=(300,-1),value=reader.getPath())
        self.confirm = wx.Button(panel, label="Browse",pos=(320,30))
        self.file = wx.DirDialog(self,defaultPath = self.reader.getPath())

        self.Bind(wx.EVT_BUTTON,self.editPath,self.confirm)
    
    def editPath(self,event):
        self.file.ShowModal()
        self.reader.setPath(self.file.GetPath())
        self.path.SetValue(self.reader.getPath())
        
class TSP_GUI(wx.Frame):
    def __init__(self,parent,title):
        super(TSP_GUI,self).__init__(parent,title=title,size=(1024,600))
        self._panel = wx.Panel(self,id=wx.ID_ANY,size=(600,400))
        self.db = Query()
        self.reader = READER()
        self.plotter = TSP_PLOT(self._panel)

        #Preferences Tab
        self._menubar = wx.MenuBar()
        self._menu = wx.Menu()
        self._file_path = self._menu.Append(wx.ID_PREFERENCES)
        self._menubar.Append(self._menu,"File")
        self.SetMenuBar(self._menubar)

        self._font = wx.Font(12,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)

        self._uploadLabel = wx.StaticText(self._panel,label="Upload Problem",pos=(5,20))
        self._upload_problem_input = wx.TextCtrl(self._panel,pos=(5,50))
        self._upload_problem_submit = wx.Button(self._panel,label="Submit",pos=(125,50))

        self._problems_label = wx.StaticText(self._panel,label="Problems",pos=(5,100))
        self._problems_list_names = wx.ListBox(self._panel, pos=(5,125),size=(90,100),style=wx.LB_SINGLE)

        self._solution_label_times = wx.StaticText(self._panel,label="Solutions",pos=(125,100))
        self._solutions_list_times = wx.ListBox(self._panel,pos=(125,125),size=(100,100))

        self._loaded_label = wx.StaticText(self._panel,label="",pos=(5,255))
        self._load_button = wx.Button(self._panel,label="Load",pos=(125,250))
        
        self._solve_problem = wx.StaticText(self._panel,pos=(7,322))

        self._solve_time_label = wx.StaticText(self._panel,label="Time",pos=(130,300))
        self._solve_input = wx.TextCtrl(self._panel,pos=(130,320),size=(75,-1))
        self._solve_submit = wx.Button(self._panel,label="Solve",pos=(215,320))
        self._save_solved_button = wx.Button(self._panel,label="Save Solution",pos=(5,350))

        #Set Label Fonts
        self._uploadLabel.SetFont(self._font)
        self._problems_label.SetFont(self._font)
        self._solution_label_times.SetFont(self._font)
        self._solve_time_label.SetFont(self._font)
        self._loaded_label.SetFont(wx.Font(11,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))
        self._solve_problem.SetFont(wx.Font(11,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))

        #Hide widgets
        self._load_button.Hide()
        self._solve_time_label.Hide()
        self._solve_input.Hide()
        self._solve_submit.Hide()
        self._save_solved_button.Hide()



    def initialise(self):
        self.Show(True)    
        
class TSP_GUI_LOGIC(TSP_GUI):
    def __init__(self,parent,title):
        super(TSP_GUI_LOGIC,self).__init__(parent,title)
        self.setProblems()

        self.Bind(wx.EVT_BUTTON,self.uploadProblem,self._upload_problem_submit)
        self.Bind(wx.EVT_LISTBOX,self.selectProblem,self._problems_list_names)
        self.Bind(wx.EVT_LISTBOX,self.selectSolution,self._solutions_list_times)
        self.Bind(wx.EVT_MENU,self.editPath,self._file_path)
        self.Bind(wx.EVT_BUTTON,self.loadSelected,self._load_button)
        self.Bind(wx.EVT_BUTTON, self.solveLoaded, self._solve_submit)
        self.Bind(wx.EVT_BUTTON,self.saveSolved,self._save_solved_button)

        self.initialise()

    def selectProblem(self,event):
        self._loaded_name = self._problems_list_names.GetString(self._problems_list_names.GetSelection())
        self._loaded_time = None
        self.setSolutionTimes(self._loaded_name)
        self._loaded_label.SetLabel(self._loaded_name)

        self._loaded_label.Show()
        self._load_button.Show()

    def setProblems(self):
        self._problems_list_names.Set(self.db.getProblems())
        
    def setSolutionTimes(self,name):
        self._solutions_list_times.Set(self.db.getSolutionTimes(name))

    def uploadProblem(self,event):
        problem = self._upload_problem_input.GetValue()
        a = self.reader.readIn(problem)
        self.db.addProblem(name = problem,size = a[0]["size"],comment = a[0]["comment"])

        nodes = a[1]
        for node in nodes:
            self.db.addCity(name=problem,id=int(node[0]),x = float(node[1]),y= float(node[2]))
        
        self.db.save()
        self.setProblems()

    def editPath(self,event):
        PREFERENCES_DIALOG(self,self.reader).Show()

    def selectSolution(self,event):
        self._loaded_time = int(self._solutions_list_times.GetString(self._solutions_list_times.GetSelection()))
        self._loaded_label.SetLabel(self._loaded_name + ", " + str(self._loaded_time) + " secs")
        
        self._load_button.Show()
        self._loaded_label.Show()

    def loadSelected(self,event):

        if (self._loaded_name and not self._loaded_time):

            self._loaded_tour = self.db.getCities(self._loaded_name)
            self._solve_problem.SetLabel(self._loaded_name)
    
            self.plotter.updatePlot(self.getx(self._loaded_tour),self.gety(self._loaded_tour))

        elif (self._loaded_name and self._loaded_time):

            #load solution
            a = self.db.getSolutionCities(self._loaded_name,int(self._loaded_time))
            b = self.db.getCities(self._loaded_name)
            c = []

            for i in a:
                for j in range(len(b)):
                    if i == b[j][0]:
                        c.append(b[j])

            self._loaded_tour = c
            self.plotter.updatePlot(self.getx(),self.gety())
            self._solve_problem.SetLabel(self._loaded_name + ", " + str(self._loaded_time) + " secs")

        self._load_button.Hide()
        self._loaded_label.Hide()
            
        self._solve_input.Show()
        self._solve_submit.Show()
        self._solve_time_label.Show()
    
    def getx(self):
        a = [a[1] for a in self._loaded_tour]
        a.append(a[0])
        return a

    def gety(self):
        a = [a[2] for a in self._loaded_tour]
        a.append(a[0])
        return a

    def solveLoaded(self,event):
        if self._loaded_tour:  
            self._solve_time = int(self._solve_input.GetValue())
            a = solve(self._loaded_tour,self._solve_time)
            self._solution_tour_length = a[0]
            self._solution_tour_str = a[1]
            self._solution_tour = a[2]
            self._save_solved_button.Show()
            

    def saveSolved(self,event):
        if self._solution_tour:
            self.db.addSolution(self._loaded_name,self._solution_tour_length,self._solve_time,self._solution_tour_str)
            self.db.save()
            self.setSolutionTimes(self._loaded_name)