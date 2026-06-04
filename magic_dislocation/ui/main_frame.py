import wx
import wx.aui
from magic_dislocation.ui.list_panel import ListPanel
from magic_dislocation.ui.nav_panel import NavPanel
from pubsub import pub


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='MagicDislocation_v1',size=(900,600))
        self.aui_manager = wx.aui.AuiManager(self,wx.aui.AUI_MGR_TRANSPARENT_HINT)

        self.nav_panel = NavPanel(self)
        self.list_panel = ListPanel(self)

        self.aui_manager.AddPane(self.nav_panel, self._get_default_pane_info().Left().Row(0).BestSize(300,-1))
        self.aui_manager.AddPane(self.list_panel, self._get_default_pane_info().CenterPane().Position(0).BestSize(600, -1))
        pub.subscribe(self._on_pipeline_type_selected, 'pipeline_type.selected')
        self.aui_manager.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_SASH_SIZE, 1)
        self.aui_manager.Update()

        self.Maximize(True)
        self._register_listeners()


    def _get_default_pane_info(self):
        return wx.aui.AuiPaneInfo().CaptionVisible(False).PaneBorder(False).CloseButton(False).PinButton(False).Gripper(
            False)


    def _on_pipeline_type_selected(self, notebook):
        self.aui_manager.DetachPane(self.list_panel)
        self.list_panel.Destroy()
        self.list_panel = ListPanel(self)
        self.list_panel.init_ui(notebook)
        
        self.aui_manager.AddPane(self.list_panel, self._get_default_pane_info().CenterPane().Position(0).BestSize(600, -1))
        self.aui_manager.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_SASH_SIZE, 1)
        self.aui_manager.Update()
        
        
    def on_frame_closing(self, e):
        self.aui_manager.UnInit()
        del self.aui_manager
        self.Destroy()


    def _register_listeners(self):
        self.Bind(wx.EVT_CLOSE, self.on_frame_closing)