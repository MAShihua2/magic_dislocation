import wx
from pubsub import pub
import wx.lib.agw.customtreectrl as customtreectrl

class NoteTree(customtreectrl.CustomTreeCtrl):
    def __init__(self, parent):
        super().__init__(parent,agwStyle=customtreectrl.TR_HAS_BUTTONS|customtreectrl.TR_FULL_ROW_HIGHLIGHT|customtreectrl.TR_ELLIPSIZE_LONG_ITEMS|customtreectrl.TR_TOOLTIP_ON_LONG_ITEMS)

        self.root = self.AddRoot("Pipeline Type")
        self._load_pipeline_types()
        self._init_ui()
        
        wx.CallAfter(self.DoSelectItem,self.GetRootItem().GetChildren()[0])

        # _init_event
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self._check_tree_sel)

    
    def _load_pipeline_types(self):
        pipelines = ['Displace','Add-Displace','Delete-Displace']

        for pipeline in pipelines:
            root_node = self.AppendItem(self.root, pipeline)
            self.AppendItem(root_node, 'Rectangle')
            self.AppendItem(root_node, 'Loop')
            self.AppendItem(root_node, 'Sin')
        self.ExpandAll()

    def _init_ui(self):
        panel_font = self.GetFont()
        panel_font.SetPointSize(panel_font.GetPointSize() + 1)
        self.SetFont(panel_font)

        self.EnableSelectionGradient(False)
        self.EnableSelectionGradient(False)

        self.SetForegroundColour("#ececec")
        self.SetBackgroundColour("#2a2a2a")
        self.SetHilightFocusColour("#646464")
        self.SetHilightNonFocusColour("#646464")

        self.SetSpacing(20)
        self.SetIndent(10)

    
    def _check_tree_sel(self, e):
        item_name = e.GetEventObject().GetSelection()._text
        if item_name == 'Pipeline Type':
            pub.sendMessage('root.selected')
            return

        parent = e.GetEventObject().GetSelection().GetParent()._text
        final_name = f"{parent}-{item_name}" if parent != 'Pipeline Type' else item_name
        if item_name != 'Pipeline Type':
            pub.sendMessage('pipeline_type.selected', notebook=final_name)
        else:
            pub.sendMessage('root.selected')
        

class NavPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        v_sizer = wx.BoxSizer(wx.VERTICAL)

        self.btn_new_note = wx.Button(self,style=wx.NO_BORDER)
        self.btn_new_note.SetLabelMarkup('<span fgcolor="white" weight="bold" size="large">MagicDislocation</span>')

        v_sizer.Add(self.btn_new_note, flag=wx.ALIGN_CENTER|wx.TOP, border=40)
        v_sizer.AddSpacer(20)

        self.note_tree = NoteTree(self)

        v_sizer.Add(self.note_tree, proportion=1,flag=wx.EXPAND)
        self.SetSizer(v_sizer)

        self.SetBackgroundColour("#2a2a2a")
        