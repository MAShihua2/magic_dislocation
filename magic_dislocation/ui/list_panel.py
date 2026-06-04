import wx
import os
from pubsub import pub
import yaml
import logging


# setting logger 
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
continue_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(continue_formatter)

logger.addHandler(console_handler)

class ListPanel(wx.Panel):

    def __init__(self, *args, **kwargs, ):
        super(ListPanel, self).__init__(*args, **kwargs)
    
    def init_ui(self, pipeline_type="displace"):
        logger.info(f"The pipeline type is: {pipeline_type}")
        self.params = {}
        
        gbs = wx.GridBagSizer(6, 6) # distance between the widgets

        ############################ Data Information ################################
        gbs.Add(wx.StaticText(self, label="="*40 + "    Data Setting    " + "="*40), pos=(1, 1), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=5)
        # Data Information-filename
        filename_line_id = 2
        gbs.Add(wx.StaticText(self, label="Filename"), pos=(filename_line_id, 0), flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        text_ctrl = wx.FilePickerCtrl(self, message="Choose a file", wildcard="*.*", size=(150, -1), name="filename")
        gbs.Add(text_ctrl, pos=(filename_line_id, 1), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=5)
        self.Bind(wx.EVT_TEXT, self.text_enter, text_ctrl)
        
        # Data Information-file format
        format_line_id = 3
        gbs.Add(wx.StaticText(self, label="Format"), pos=(format_line_id, 0), flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        data_format_choice_box = wx.Choice(self, choices=["lammps-data"], name="format")
        gbs.Add(data_format_choice_box, pos=(format_line_id, 1), span=(1, 1), flag=wx.ALL, border=5)
        
        # Data Information-lattice
        lattice_line_id = format_line_id
        gbs.Add(wx.StaticText(self, label="Lattice Constant"), pos=(lattice_line_id, 2), flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        text_ctrl = wx.TextCtrl(self, size=(150, -1), name="lattice")
        gbs.Add(text_ctrl, pos=(lattice_line_id, 3), span=(1, 1), flag=wx.EXPAND | wx.ALL, border=5)
        self.Bind(wx.EVT_TEXT, self.text_enter, text_ctrl)
        
        structure_line_id = format_line_id
        gbs.Add(wx.StaticText(self, label="Structure"), pos=(structure_line_id, 4), flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        text_ctrl = wx.Choice(self, choices=["FCC", "BCC", "Cubic"], name="structure")
        gbs.Add(text_ctrl, pos=(structure_line_id, 5), span=(1, 1), flag=wx.EXPAND | wx.ALL, border=5)
        self.Bind(wx.EVT_TEXT, self.text_enter, text_ctrl)
        
        # Data Information-other parameters
        other_para_line_id = lattice_line_id + 1
        gbs.Add(wx.StaticText(self, label="Kwargs"), pos=(other_para_line_id, 0), flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        text_ctrl = wx.TextCtrl(self, size=(150, -1), name="kwargs")
        gbs.Add(text_ctrl, pos=(other_para_line_id, 1),  span=(1, 5), flag=wx.EXPAND | wx.ALL, border=5)
        
        
        ############################ Layerization ################################
        # Add a line to separate the different parts
        layerization_line_id = other_para_line_id + 1
        gbs.Add(wx.StaticText(self, label="="*40 + "    Layerization    " + "="*40), pos=(layerization_line_id, 1), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=5)
        
        # layerization_direction_vector
        layerization_line_id += 1
        gbs.Add(wx.StaticText(self, label="Layerization Direction"), pos=(layerization_line_id, 0),
                flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        gbs.Add(wx.TextCtrl(self, name="layer_direction_vector"), pos=(layerization_line_id, 1), span=(1, 5),
                flag=wx.EXPAND | wx.ALL, border=5)
        
        # ############################ S plane ################################
        s_plane_line_id = layerization_line_id + 1
        gbs.Add(wx.StaticText(self, label="="*40 + "    S Plane Setting    " + "="*40), pos=(s_plane_line_id, 1), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=5)
        
        s_plane_line_id += 1
        ## Center point of S plane
        gbs.Add(wx.StaticText(self, label="Center Position"), pos=(s_plane_line_id, 0),
                flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        gbs.Add(wx.TextCtrl(self, name="s_center_point"), pos=(s_plane_line_id, 1),
                flag=wx.EXPAND | wx.ALL, border=5)
        
        ## s_init_vertical_axis
        gbs.Add(wx.StaticText(self, label="Initial Direction"), pos=(s_plane_line_id, 2),
                flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        gbs.Add(wx.Choice(self, choices=["X", "Y", "Z"], name="s_init_vertical_axis"), pos=(s_plane_line_id, 3),
                flag=wx.EXPAND | wx.ALL, border=5)
        
        # s_plane_line_id += 1
        ## s_direction_vector
        gbs.Add(wx.StaticText(self, label="Rotated Direction"), pos=(s_plane_line_id, 4),
                flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        gbs.Add(wx.TextCtrl(self, value="Optional", name="s_direction_vector"), pos=(s_plane_line_id, 5), span=(1, 1),
                flag=wx.EXPAND | wx.ALL, border=5)
        
        s_plane_line_id += 1
        # s plane type
        if "loop" in pipeline_type.lower():
            self.params["s_type"] = "loop"
            gbs.Add(wx.StaticText(self, label="="*40 + "    Loop Settings    " + "="*40), pos=(s_plane_line_id, 1), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=5)
            s_plane_line_id += 1
            gbs.Add(wx.StaticText(self, label="Number of Points"), pos=(s_plane_line_id, 0),
                    flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
            gbs.Add(wx.TextCtrl(self, value="48", name="s_num_points"), pos=(s_plane_line_id, 1),
                    flag=wx.EXPAND | wx.ALL, border=5)
            
            gbs.Add(wx.StaticText(self, label="Radius"), pos=(s_plane_line_id, 2),
                    flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
            gbs.Add(wx.TextCtrl(self, name="s_radius"), pos=(s_plane_line_id, 3),
                    flag=wx.EXPAND | wx.ALL, border=5)
        elif "rectangle" in pipeline_type.lower():
            gbs.Add(wx.StaticText(self, label="="*40 + "    Rectangle Settings    " + "="*40), pos=(s_plane_line_id, 1), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=5)
            s_plane_line_id += 1
            self.params["s_type"] = "rectangle"
            gbs.Add(wx.StaticText(self, label="Length"), pos=(s_plane_line_id, 0),
                    flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
            gbs.Add(wx.TextCtrl(self, name="s_length"), pos=(s_plane_line_id, 1),
                    flag=wx.EXPAND | wx.ALL, border=5)
            
            gbs.Add(wx.StaticText(self, label="Width"), pos=(s_plane_line_id, 2),
                    flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
            gbs.Add(wx.TextCtrl(self, name="s_width"), pos=(s_plane_line_id, 3),
                    flag=wx.EXPAND | wx.ALL, border=5)
        elif "sin" in pipeline_type.lower():
            self.params["s_type"] = "sin"

            gbs.Add(wx.StaticText(self, label="="*40 + "    Sin Settings    " + "="*40), pos=(s_plane_line_id, 1), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=5)
            s_plane_line_id += 1
            gbs.Add(wx.StaticText(self, label="Length"), pos=(s_plane_line_id, 0),
                    flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
            gbs.Add(wx.TextCtrl(self, size=(50, -1), name="s_length"), pos=(s_plane_line_id, 1),
                    flag=wx.EXPAND | wx.ALL, border=5)
            
            gbs.Add(wx.StaticText(self, label="Width"), pos=(s_plane_line_id, 2),
                    flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
            gbs.Add(wx.TextCtrl(self, size=(50, -1), name="s_width"), pos=(s_plane_line_id, 3), 
                    flag=wx.EXPAND | wx.ALL, border=5)
            gbs.Add(wx.StaticText(self, label="A"), pos=(s_plane_line_id, 4),
                    flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
            gbs.Add(wx.TextCtrl(self, size=(50, -1), name="s_A"), pos=(s_plane_line_id, 5),
                    flag=wx.EXPAND | wx.ALL, border=5)
            
            s_plane_line_id += 1
            
            gbs.Add(wx.StaticText(self, label="Omega"), pos=(s_plane_line_id, 0),
                    flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
            gbs.Add(wx.TextCtrl(self, size=(50, -1), name="s_omega"), pos=(s_plane_line_id, 1),
                    flag=wx.EXPAND | wx.ALL, border=5)
            gbs.Add(wx.StaticText(self, label="Start Point Index"), pos=(s_plane_line_id, 2),
                    flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
            gbs.Add(wx.TextCtrl(self, size=(50, -1), name="s_start"), pos=(s_plane_line_id, 3), span=(1, 1),
                    flag=wx.EXPAND | wx.ALL, border=5)
            gbs.Add(wx.StaticText(self, label="End Point Index"), pos=(s_plane_line_id, 4),
                    flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
            gbs.Add(wx.TextCtrl(self, size=(50, -1), name="s_end"), pos=(s_plane_line_id, 5), span=(1, 1),
                    flag=wx.EXPAND | wx.ALL, border=5)
        
            s_plane_line_id += 1
            gbs.Add(wx.StaticText(self, label="Number of Points"), pos=(s_plane_line_id, 0),
                    flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
            gbs.Add(wx.TextCtrl(self, size=(50, -1), name="s_num_points", value="48"), pos=(s_plane_line_id, 1), span=(1, 1),
                    flag=wx.EXPAND | wx.ALL, border=5)
        

        
        ############################# Move ################################
        move_line_id = s_plane_line_id + 1
        gbs.Add(wx.StaticText(self, label="="*40 + "    Displacement Setting   " + "="*40), pos=(move_line_id, 1), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=5)
        
        # selection of layers to be moved
        move_line_id += 1
        gbs.Add(wx.StaticText(self, label="Layer Range"), pos=(move_line_id, 0),
                flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        gbs.Add(wx.TextCtrl(self, value="Optional", name="large_range"), pos=(move_line_id, 1),
                flag=wx.EXPAND | wx.ALL, border=5)
        
        # selection of layers to be moved
        gbs.Add(wx.StaticText(self, label="Burgers Vector (Cartesian)"), pos=(move_line_id, 2),
                flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        gbs.Add(wx.TextCtrl(self, name="burgers_vector"), pos=(move_line_id, 3),
                flag=wx.EXPAND | wx.ALL, border=5)
        
        
        ################################ Visualization ################################
        v_line_id = move_line_id + 1
        gbs.Add(wx.StaticText(self, label="="*40 + "    Visualization   " + "="*40), pos=(v_line_id, 1), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=5)
        
        # visualization options
        v_line_id += 1
        gbs.Add(wx.StaticText(self, label="Visualization"), pos=(v_line_id, 0),
                flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        vis_checklist_box = wx.CheckListBox(self, id=wx.ID_ANY,
                                        choices=["visualize_layer", "visualize_s", "visualize_add", "visualize_delete", "visualize_select",
                                                 "visualize_move"], name="visualization")
        gbs.Add(vis_checklist_box, pos=(v_line_id, 1), span=(1, 2),
                flag=wx.EXPAND | wx.ALL, border=5)
        
        ############################ Delete ################################
        other_line_id = v_line_id + 1
        self.params["pipeline_type"] = "displace"
        if "delete" in pipeline_type.lower():
            # range of layers to be deleted
            gbs.Add(wx.StaticText(self, label="-"*40 + "    Delete Parameters   " + "-"*40), pos=(other_line_id, 1), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=5)
            other_line_id += 1
            gbs.Add(wx.StaticText(self, label="Burgers Vector Fraction"), pos=(other_line_id, 0),
                    flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
            gbs.Add(wx.TextCtrl(self, name="burgers_vector_fraction"), pos=(other_line_id, 1),
                    flag=wx.EXPAND | wx.ALL, border=5)
            
            # selection of layers to be deleted
            gbs.Add(wx.StaticText(self, label="Burgers Vector Direction"), pos=(other_line_id, 2),
                    flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
            gbs.Add(wx.TextCtrl(self, name="burgers_vector_direction"), pos=(other_line_id, 3),
                    flag=wx.EXPAND | wx.ALL, border=5)
            self.params["pipeline_type"] = "delete_displace"
        elif "add" in pipeline_type.lower():
            # range of layers to be added
            gbs.Add(wx.StaticText(self, label="="*40 + "    Add Parameters   " + "="*40), pos=(other_line_id, 1), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=5)
            other_line_id += 1
            gbs.Add(wx.StaticText(self, label="Layers Range for Adding"), pos=(other_line_id, 0),
                    flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
            gbs.Add(wx.TextCtrl(self, name="layers_range_for_adding"), pos=(other_line_id, 1),
                    flag=wx.EXPAND | wx.ALL, border=5)
            self.params["pipeline_type"] = "add_displace"
            
        gauge_line_id = other_line_id + 1
        button = wx.Button(self, label="Run")
        gbs.Add(button, pos=(gauge_line_id, 1), span=(1, 5),
                flag=wx.EXPAND | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.run_button, button)
        
        gauge_line_id += 1
        self.gauge = wx.Gauge(self, range=100, size=(200, 25))
        gbs.Add(self.gauge, pos=(gauge_line_id, 1), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=5)

        self.gbs = gbs

        self.SetSizer(gbs)
        self.SetSize(600, 600)


    def choice(self, e):
        choice = e.GetEventObject()
        index = choice.GetSelection()
        text = choice.GetStringSelection()


    def listbox(self, e):
        listbox = e.GetEventObject()
        index = listbox.GetSelection()
        text = listbox.GetStringSelection()


    def checklist(self, e):
        checklist = e.GetEventObject()
        index_list = checklist.GetCheckedItems()
        text_list = checklist.GetCheckedStrings()


    def text_enter(self, e):
        text = e.GetEventObject()

        
    def run_button(self, e):
        self.gauge.SetValue(0)
        for i, item in enumerate(self.gbs.GetChildren()):
            name = item.GetWindow().GetName()
            if name == "staticText":
                continue
            item_type = type(item.GetWindow())
            if item_type == wx.TextCtrl:
                # label = self.gbs.Children[i-1].GetWindow().GetLabel()
                value = item.GetWindow().GetValue()
            elif item_type == wx.Choice:
                # label = self.gbs.Children[i-1].GetWindow().GetLabel()
                value = item.GetWindow().GetStringSelection()
            elif item_type == wx.CheckListBox:
                # label = self.gbs.Children[i-1].GetWindow().GetLabel()
                value = item.GetWindow().GetCheckedStrings()
            elif item_type == wx.FilePickerCtrl:
                # label = self.gbs.Children[i-1].GetWindow().GetLabel()
                value = item.GetWindow().GetPath()
            else:
                continue
                
            if name == "kwargs":
                for kwarg in value.split(";"):
                    key, value = kwarg.split(":")
                    self.params[key] = value
        
            if name == "s_init_vertical_axis":
                value = str(["X", "Y", "Z"].index(value))
            self.params[name] = value
            
        logger.info(self.params)
        
        new_params = {}
        
        for item in ["visualize_layer", "visualize_s", "visualize_add", "visualize_delete", "visualize_select", "visualize_move"]:
            if item in self.params["visualization"]:
                new_params[item] = 1
            else:
                new_params[item] = 0
        
        # convert the string to the float
        for key, value in self.params.items():
            logger.info(f"{key} {value}")
            if value == "" or value == "Optional":
                continue
            if "," in value:
                new_params[key] = [eval(v) for v in value.split(",")]
            else:
                try:
                    new_params[key] = eval(value)
                except:
                    new_params[key] = value
        
        logger.info(new_params)
        self.gauge.SetValue(20)
        # save the parameters to the yaml file
        file_path = new_params["filename"]
        print(file_path)
        file_name = file_path.split("/")[-1]
        print(file_name)
        # para_file_path = "/".join(file_path.split("/")[:-1]) + "/params.yaml"
        print(file_path)
        para_file_path = file_path.replace(file_name, "ui_params.yaml")
        with open(para_file_path, "w") as f:
            yaml.dump(new_params, f)
        print(para_file_path)
        self.gauge.SetValue(50)
        # os.system("cd ")
        os.system(f'python run_v1.py --yaml_file "{para_file_path}"')
        self.gauge.SetValue(100)
        
        logger.info("run")
        
        