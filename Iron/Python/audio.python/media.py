from System import *
from System.Windows import * 
from System.Windows.Controls import *
from System.Windows.Input import *
from System.Windows.Media import *
from System.Windows.Media.Imaging import * # for bitmap
from System.Collections.Generic import *
from System.Windows.Threading import DispatcherTimer
from System.Windows.Browser import *
from System.IO import StringReader
import clr
clr.AddReference("System.Xml")
from System.Xml import *

_isScrubberLocked = False
_positionTimer = None
_loop = False
_src = ""
_poster = ""
_volume = 0.5
_width = 300;
_height = 150
_autoPlay = True
_muted = False
_controls = False
_autoBuffer = False
_ended = False

class SourceElement(object):
    src = ""
    type = ""
    title = ""
    artist = ""

class MediaInfo(object):
    def __init__(self, xml):
		self._xml = xml
		self.Sources = List[String]()
		self.Video = True
		self.Loop = True
		self.Autoplay = True
		self.Volume = .5
		self.Width = 300
		self.Height = 150
		self.Poster = ""
		self.Controls = True
		self.Autobuffer = True
		self.Muted = False
        
		reader = XmlReader.Create(StringReader(self._xml))
		while (reader.Read()):
			if reader.Name == "video":
				self.Video = reader.ReadElementContentAsBoolean()
			elif reader.Name == "width":
				self.Width = reader.ReadElementContentAsDouble()
			elif reader.Name == "height":
				self.Height = reader.ReadElementContentAsDouble()
			elif reader.Name == "autoplay":
				self.Autoplay = reader.ReadElementContentAsString()
			elif reader.Name == "volume":
				self.Volume = reader.ReadElementContentAsDouble()
			elif reader.Name == "poster":
				self.Poster = reader.ReadElementContentAsString()
			elif reader.Name == "loop":
				self.Loop = reader.ReadElementContentAsBoolean()
			elif reader.Name == "controls":
				self.Controls = reader.ReadElementContentAsBoolean()
			elif reader.Name == "autobuffer":
				self.Autobuffer = reader.ReadElementContentAsBoolean()
			elif reader.Name == "muted":
				self.Muted = reader.ReadElementContentAsBoolean()
			elif reader.Name == "sources":
				item = None
				while (reader.Read()):
					if reader.Name == "source":
						item = reader.ReadElementContentAsString()
						self.Sources.Add(item)
    
class SelectableSourceElementList (List[SourceElement]):
    LastItem = True
    def __init__(self):
        self._SelectedIndex = 0
        
    def Next(self):
        self._SelectedIndex = self._SelectedIndex + 1
        
        if self._SelectedIndex + 1 > self.Count:
            self._SelectedIndex = 0
            LastItem = True
        else:
            LastItem = False
            
    def Previous(self):
        self._SelectedIndex = self._SelectedIndex - 1
        if self._SelectedIndex < 0:
            self._SelectedIndex = self.Count - 1
            
    def SetSelectedItem(self, value):
        pass
    def GetSelectedItem(self):
        if self[self._SelectedIndex] != None:
            return self[self._SelectedIndex]
        else:
            return None
    SelectedItem = property(GetSelectedItem, SetSelectedItem)
    
    def SetSelectedIndex(self, value):
        self._SelectedIndex = value
    def GetSelectedIndex(self):
        return self._SelectedIndex
    SelectedIndex = property(GetSelectedIndex, SetSelectedIndex) 

def ConvertHexToColor(hexColor):
    c = Color()
    c = Color.FromArgb(
        Convert.ToUInt32(hexColor.Substring(1, 2), 16), 
        Convert.ToUInt32(hexColor.Substring(3, 2), 16), 
        Convert.ToUInt32(hexColor.Substring(5, 2), 16), 
        Convert.ToUInt32(hexColor.Substring(7, 2), 16))				
    return c
    
def DomGetFullPathToDir():
    content = ""
    try:
        path = HtmlPage.Document.DocumentUri.ToString()
        segments = path.Split('/')
        content = path.Replace(segments[segments.Length - 1], "")
    except:
        pass
    return content
            
def EnsureAbsoluteFilePath(initialPath):
    if String.IsNullOrEmpty(initialPath):
        return String.Empty

    if initialPath.ToLower().Contains("http://"):
        return initialPath
    else:
        s = DomGetFullPathToDir()
        return s + initialPath
        
def Opened(s, e):
    me.Player.Play()
    
def _Play():
    if me.Player.CurrentState != MediaElementState.Playing:
        me.Poster.Visibility = Visibility.Collapsed
        
        if MediaCollection.Count > 0:
            if me.Player.Position.TotalSeconds == 0: # only queue up next video if the current one is finished playing
                me.Player.Source = Uri(MediaCollection.SelectedItem.src, UriKind.Absolute)
                me.Caption.Text = ""
                
        if me.Player.AutoPlay == False:
            me.Player.MediaOpened += Opened
        else:
            if  me.Player.CurrentState != MediaElementState.Playing: # don't try to play if it's already playing
                me.Player.Play()
        
def _Stop():
    me.Poster.Visibility = Visibility.Visible; # make any present poster visible

def Next():
    me.Player.Pause()
    me.Player.Position = TimeSpan(0, 0, 0)
    if MediaCollection.Count > 1:
        MediaCollection.Next()
    _Play()
    
def Previous():
    me.Player.Pause()
    me.Player.Position = TimeSpan(0, 0, 0)
    if MediaCollection.Count > 1:
        MediaCollection.Previous()
    _Play()

# event handlers
def positionTimer_Tick(s,e):
    if me.Player.Position.TotalSeconds > 0 and not _isScrubberLocked:
        me.Scrubber.Value = Convert.ToDouble(me.Player.Position.Ticks) / Convert.ToDouble(me.Player.NaturalDuration.TimeSpan.Ticks)
        me.MsgCurrentTime.Text = String.Format("{0:00}:{1:00}:{2:00}", 
            me.Player.Position.Hours, me.Player.Position.Minutes, me.Player.Position.Seconds)

def Player_MediaOpened(s, e):
    me.Scrubber.Value = 0
    me.MsgTotalTime.Text = String.Format("{0:00}:{1:00}:{2:00}", 
        me.Player.NaturalDuration.TimeSpan.Hours, 
        me.Player.NaturalDuration.TimeSpan.Minutes, 
        me.Player.NaturalDuration.TimeSpan.Seconds)
    
def Player_CurrentStateChanged(s, e):
    if me.Player.CurrentState == MediaElementState.Playing:
        me.ShowPauseButton.Begin()
        _positionTimer.Start()
        
    elif me.Player.CurrentState == MediaElementState.Paused:
        me.ShowPlayButton.Begin()
        _positionTimer.Stop()
        
    if me.Player.CurrentState == MediaElementState.Stopped:
        me.ShowPlayButton.Begin()
        _positionTimer.Stop()
        me.Scrubber.Value = 0
        
def Player_DownloadProgressChanged(s, e):
    me.DownloadProgressTrack.RenderTransform.ScaleX = me.Player.DownloadProgress
    
def Scrubber_MouseLeave(s, e):
    global _isScrubberLocked
    _isScrubberLocked = False

def Scrubber_MouseMove(s, e):
    global _isScrubberLocked
    _isScrubberLocked = True

def Scrubber_MouseLeftButtonUp(s, e):
    global _isScrubberLocked
    me.Player.Position = TimeSpan.FromSeconds(me.Scrubber.Value * me.Player.NaturalDuration.TimeSpan.TotalSeconds)
    _isScrubberLocked = False
    
def BtnPlayPause_MouseLeftButtonUp(s, e):
    if me.Player.CurrentState == MediaElementState.Playing:
        me.Player.Pause()
    elif me.Player.CurrentState == MediaElementState.Paused:
        _Play()
    elif me.Player.CurrentState == MediaElementState.Stopped:
        _Play()
        
def Poster_MouseLeftButtonDown(s, e):
    _Play()      

def BtnPlayPause_MouseLeave(s, e):
    me.PlayPauseSymbol_MouseLeave.Begin()

def BtnPlayPause_MouseEnter(s, e):
    me.PlayPauseSymbol_MouseEnter.Begin()
    
def VolumeSlider_ValueChanged(s, e):
    me.Player.Volume = me.VolumeSlider.Value
    
def ShowControlPanel_Completed(s, e):
    me.ControlPanelTimer.Begin()

def ShowVolumeSlider_Completed(s, e):
    me.VolumeSliderTimer.Begin()

def VolumeSliderCanvas_MouseMove(s, e):
    me.VolumeSliderTimer.Begin()

def VolumeSliderTimer_Completed(s, e):
    me.HideVolumeSlider.Begin()
    
def ControlPanelTimer_Completed(s, e):
    me.HideControlPanel.Begin()    

def BtnVolume_MouseLeftButtonUp(s, e):
    me.ShowVolumeSlider.Begin()
    
def Player_MouseMove(s, e):
    if settings.Video:
        me.ShowControlPanel.Begin()  
    
def Player_MouseLeave(s, e):
    me.ControlPanelTimer.Begin()      
    
def BtnVolume_MouseEnter(s, e):
    me.VolumeSymbol_MouseEnter.Begin()    
    
def BtnVolume_MouseLeave(s, e):   
    me.VolumeSymbol_MouseLeave.Begin()
    
def NextSymbol_MouseEnter(s, e):
	if mediaCount > 1:
		me.NextSymbol_MouseEnter.Begin()
    
def NextSymbol_MouseLeave(s, e):
	if mediaCount > 1:  
		me.NextSymbol_MouseLeave.Begin()
    
def PreviousSymbol_MouseEnter(s, e):
	if mediaCount > 1:
		me.PreviousSymbol_MouseEnter.Begin()
    
def PreviousSymbol_MouseLeave(s, e): 
	if mediaCount > 1:  
		me.PreviousSymbol_MouseLeave.Begin() 
    
def FullSymbol_MouseEnter(s, e):
    me.FullSymbol_MouseEnter.Begin()
    
def FullSymbol_MouseLeave(s, e):   
    me.FullSymbol_MouseLeave.Begin()          
    
def Player_MarkerReached(s, e):
    me.Caption.Text = e.Marker.Text
    
def FullSymbol_MouseLeftButtonDown(s, e):
    Application.Current.Host.Content.IsFullScreen = not Application.Current.Host.Content.IsFullScreen
    me.Width = Application.Current.Host.Content.ActualWidth
    me.Height = Application.Current.Host.Content.ActualHeight
    
def BrowserHost_Resize(s, e):
    me.Width = Application.Current.Host.Content.ActualWidth
    me.Height = Application.Current.Host.Content.ActualHeight

def Player_MediaEnded(s, e):
    me.Player.Position = TimeSpan(0, 0, 0)
    me.Poster.Visibility = Visibility.Collapsed
    
    if MediaCollection.Count > 0: # is there a playlist?
        if _loop: # just keep looping
            MediaCollection.Next()
            _Play()
        else:
            MediaCollection.Next()
            if MediaCollection.SelectedIndex > 0: # check to see if we've finished the playlist
                _Play()
            else:
                _Stop()
    elif _loop:
        _Play()
    else:
        _Stop()
        
def Player_MediaFailed(s, e):
    me.Caption.Text = "Issue loading file: " + MediaCollection.SelectedItem.src
    
def GoNext(s, e):
	if mediaCount > 1:  
		Next()

def GoPrevious(s, e):
    if mediaCount > 1:  
		Previous()   

# if XAML was not loaded do not process further
if me != None:
	# register for events
	me.Player.MediaOpened += Player_MediaOpened
	me.Player.CurrentStateChanged += Player_CurrentStateChanged
	me.Player.DownloadProgressChanged += Player_DownloadProgressChanged
	me.Player.MarkerReached += Player_MarkerReached
	me.Player.MediaEnded += Player_MediaEnded
	me.Player.MediaFailed += Player_MediaFailed
	me.Player.MouseMove += Player_MouseMove

	me.Scrubber.MouseLeftButtonUp += Scrubber_MouseLeftButtonUp
	me.Scrubber.MouseMove += Scrubber_MouseMove
	me.Scrubber.MouseLeave += Scrubber_MouseLeave

	me.BtnPlayPause.MouseEnter += BtnPlayPause_MouseEnter
	me.BtnPlayPause.MouseLeave += BtnPlayPause_MouseLeave
	me.BtnPlayPause.MouseLeftButtonUp += BtnPlayPause_MouseLeftButtonUp

	me.BtnVolume.MouseEnter +=  BtnVolume_MouseEnter
	me.BtnVolume.MouseLeave +=  BtnVolume_MouseLeave
	me.BtnVolume.MouseLeftButtonUp += BtnVolume_MouseLeftButtonUp

	me.VolumeSlider.ValueChanged += VolumeSlider_ValueChanged
	me.ShowVolumeSlider.Completed += ShowVolumeSlider_Completed
	me.VolumeSliderTimer.Completed += VolumeSliderTimer_Completed
	me.VolumeSliderCanvas.MouseMove += VolumeSliderCanvas_MouseMove

	me.ControlPanel.MouseMove += Player_MouseMove
	me.ShowControlPanel.Completed += ShowControlPanel_Completed
	me.Player.MouseLeave += Player_MouseLeave
	me.ControlPanelTimer.Completed += ControlPanelTimer_Completed

	me.NextSymbol.MouseEnter +=  NextSymbol_MouseEnter
	me.NextSymbol.MouseLeave +=  NextSymbol_MouseLeave
	me.NextSymbol.MouseLeftButtonDown += GoNext

	me.PreviousSymbol.MouseLeftButtonDown += GoPrevious
	me.PreviousSymbol.MouseEnter +=  PreviousSymbol_MouseEnter
	me.PreviousSymbol.MouseLeave +=  PreviousSymbol_MouseLeave

	me.Poster.MouseLeftButtonDown += Poster_MouseLeftButtonDown

	me.FullSymbol.MouseLeftButtonDown += FullSymbol_MouseLeftButtonDown
	me.FullSymbol.MouseEnter +=  FullSymbol_MouseEnter
	me.FullSymbol.MouseLeave +=  FullSymbol_MouseLeave
	Application.Current.Host.Content.Resized += BrowserHost_Resize

	# set to True if you want to override the element colors defined in the XAML
	if False:
		# must be ARGB format
		ButtonOffHexValue = "#ffbbbbbb" # color of buttons when mouse is not over
		ButtonOverHexValue = "#ffeeeeee" # color of buttons when mouse is hovering
		PanelBackgroundHexValue = "#66ffffff" # The control panel background color
		TextColorHexValue = "#ff808080" # the color of the timecode and caption
		MediaBackDropHexValue = "#ff000000" # the color of the overall media player background
		
		# set colors
		fillColor = SolidColorBrush(ConvertHexToColor(ButtonOffHexValue))
		me.PlaySymbol.Fill = fillColor 
		me.PauseSymbol.Fill = fillColor
		me.SpeakerShape.Fill = fillColor
		me.VolumeShape1.Stroke = fillColor
		me.VolumeShape2.Stroke = fillColor
		me.NextA.Fill = fillColor
		me.NextB.Fill = fillColor
		me.PreviousA.Fill = fillColor
		me.PreviousB.Fill = fillColor
		me.FullA.Fill = fillColor
		me.FullB.Fill = fillColor
		me.FullC.Fill = fillColor
		me.FullD.Fill = fillColor

		background = SolidColorBrush(ConvertHexToColor(PanelBackgroundHexValue))
		me.VolumeSliderBackground.Fill = background
		me.ControlPanelBackground.Fill = background
		foreground = SolidColorBrush(ConvertHexToColor(TextColorHexValue))
		me.MsgCurrentTime.Foreground = foreground
		me.Caption.Foreground = foreground
		me.TimeDivider.Foreground = foreground
		me.MsgTotalTime.Foreground = foreground
		backdrop = SolidColorBrush(ConvertHexToColor(MediaBackDropHexValue))
		me.MediaBackground.Fill = backdrop
		me.LayoutRoot.Background = backdrop

		# set the storyboard To values for mouseleave events
		buttonOffHexValue = ConvertHexToColor(ButtonOffHexValue) 
		me.Stop_MouseLeaveValue.To = buttonOffHexValue
		me.Play_MouseLeaveValue.To = buttonOffHexValue
		me.Pause_MouseLeaveValue.To = buttonOffHexValue
		me.Volume_MouseLeaveValue.To = buttonOffHexValue
		me.Volume1_MouseLeaveValue.To = buttonOffHexValue
		me.Volume2_MouseLeaveValue.To = buttonOffHexValue
		me.NextA_MouseLeaveValue.To = buttonOffHexValue
		me.NextB_MouseLeaveValue.To = buttonOffHexValue
		me.PreviousA_MouseLeaveValue.To = buttonOffHexValue
		me.PreviousB_MouseLeaveValue.To = buttonOffHexValue
		me.FullA_MouseLeaveValue.To = buttonOffHexValue
		me.FullB_MouseLeaveValue.To = buttonOffHexValue
		me.FullC_MouseLeaveValue.To = buttonOffHexValue
		me.FullD_MouseLeaveValue.To = buttonOffHexValue           

		# set the storyboard To values for mouseenter events
		buttonOverHexValue = ConvertHexToColor(ButtonOverHexValue)
		me.Stop_MouseEnterValue.To = buttonOverHexValue
		me.Play_MouseEnterValue.To = buttonOverHexValue
		me.Pause_MouseEnterValue.To = buttonOverHexValue
		me.Volume_MouseEnterValue.To = buttonOverHexValue
		me.Volume1_MouseEnterValue.To = buttonOverHexValue
		me.Volume2_MouseEnterValue.To = buttonOverHexValue
		me.NextA_MouseEnterValue.To = buttonOverHexValue
		me.NextB_MouseEnterValue.To = buttonOverHexValue
		me.PreviousA_MouseEnterValue.To = buttonOverHexValue
		me.PreviousB_MouseEnterValue.To = buttonOverHexValue
		me.FullA_MouseEnterValue.To = buttonOverHexValue
		me.FullB_MouseEnterValue.To = buttonOverHexValue
		me.FullC_MouseEnterValue.To = buttonOverHexValue
		me.FullD_MouseEnterValue.To = buttonOverHexValue

	# UI update timer
	_positionTimer = DispatcherTimer()
	_positionTimer.Interval = TimeSpan(0, 0, 0, 0, 100)
	_positionTimer.Tick += positionTimer_Tick
	_positionTimer.Start()

	#get XML from page DOM
	name = Application.Current.Host.InitParams["xamlid"].Split("-")[0]
	xmlSettings = HtmlPage.Document.GetElementById(name + "-settings").text
	settings = MediaInfo(xmlSettings)

	# assign values declared in markup
	_loop = settings.Loop
	me.Width = settings.Width
	me.Height = settings.Height

	if settings.Poster != "":
		me.Poster.Source = BitmapImage(Uri(EnsureAbsoluteFilePath(settings.Poster), UriKind.Absolute))

	ap = settings.Autoplay
	me.Player.AutoPlay = ap
	if not ap:
		me.Poster.Visibility = Visibility.Visible
	    
	me.Player.Volume = settings.Volume
	me.Player.IsMuted = settings.Muted
	if not settings.Controls:
		me.ControlPanel.Visibility = Visibility.Collapsed
	    
	if not settings.Video:
		me.Player.Visibility = Visibility.Collapsed
		me.LayoutRoot.RowDefinitions[0].Height = GridLength(0)
		me.MediaBackground.Visibility = Visibility.Collapsed 
		me.Poster.Visibility = Visibility.Collapsed
		me.FullSymbol.Visibility = Visibility.Collapsed
		me.SplitterCD.Width = GridLength(0)
		me.FullCD.Width = GridLength(0)
		me.ControlPanel.Opacity = 1
	    
	MediaCollection = SelectableSourceElementList()
	for i in range( 0, settings.Sources.Count):
		s = SourceElement()
		s.src = EnsureAbsoluteFilePath(settings.Sources[i])
		MediaCollection.Add(s)
		
	mediaCount = settings.Sources.Count
		
	if mediaCount == 1:
		me.PreviousSymbol.Cursor = Cursors.Arrow
		me.PreviousA.Fill = SolidColorBrush(ConvertHexToColor("#FF333333")) 
		me.PreviousB.Fill = SolidColorBrush(ConvertHexToColor("#FF333333")) 
		me.NextSymbol.Cursor = Cursors.Arrow
		me.NextA.Fill = SolidColorBrush(ConvertHexToColor("#FF333333")) 
		me.NextB.Fill = SolidColorBrush(ConvertHexToColor("#FF333333")) 
		
	me.Player.Source = Uri(MediaCollection.SelectedItem.src, UriKind.RelativeOrAbsolute)