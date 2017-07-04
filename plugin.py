# -*- coding: utf-8 -*-
# SkinPanel for Skin OpenPlusHD
# Copyright (c) openplus 2016
# Writed by Iqas & Villak 
# v.1.0-r0
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import os.path
import time
import gettext
from Plugins.Plugin import PluginDescriptor
from boxbranding import getBoxType, getMachineBrand, getMachineName
from Components.ActionMap import ActionMap
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Components.config import getConfigListEntry, ConfigText, ConfigYesNo, ConfigSubsection, ConfigSelection, config, configfile
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.ScrollLabel import ScrollLabel
from Components.Language import language
from Components.Pixmap import Pixmap
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Screens.Screen import Screen

lang = language.getLanguage()
os.environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("SkinPanel", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/SkinPanel/locale/"))

def _(txt):
	t = gettext.dgettext("SkinPanel", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

config.plugins.skinpanel = ConfigSubsection()
config.plugins.skinpanel.onmenu = ConfigYesNo(default=True)
config.plugins.skinpanel.winfobar = ConfigYesNo(default=False)
config.plugins.skinpanel.wsecinfobar = ConfigYesNo(default=False)
config.plugins.skinpanel.fwinfobar = ConfigYesNo(default=False)
config.plugins.skinpanel.fwsecinfobar = ConfigYesNo(default=False)
config.plugins.skinpanel.wemc = ConfigYesNo(default=False)
config.plugins.skinpanel.btinfobar = ConfigYesNo(default=True)
config.plugins.skinpanel.extmenu = ConfigYesNo(default=False)
config.plugins.skinpanel.eventname = ConfigYesNo(default=False)
config.plugins.skinpanel.seceventname = ConfigYesNo(default=False)
config.plugins.skinpanel.secdescript = ConfigYesNo(default=False)
config.plugins.skinpanel.sececminf = ConfigYesNo(default=True)
config.plugins.skinpanel.seccryptinf = ConfigYesNo(default=True)
config.plugins.skinpanel.secfrec = ConfigYesNo(default=True)
config.plugins.skinpanel.secprov = ConfigYesNo(default=True)
config.plugins.skinpanel.secmini = ConfigYesNo(default=True)

help_txt = _("Choose the options you like best, save changes and then restart enigma to apply the changes.")



##############################################################################

class skinpanel_setup(Screen, ConfigListScreen):
	skin = """<screen name="skinpanel_setup" position="center,center" size="1920,1080" title="OpenPlus! SkinPanel Configuration" backgroundColor="transparent" flags="wfNoBorder">
    <ePixmap pixmap="openplusHD/menu/pincel.png" position="361,460" size="250,359" alphatest="blend" zPosition="-11" />
    <widget position="640,312" size="901,343" name="config" scrollbarMode="no" font="Caviar_bold; 22" itemHeight="35" backgroundColor="un6e6e6e" foregroundColor="white" />
    <eLabel position="640,660" size="901,2" backgroundColor="white" zPosition="5" foregroundColor="white" />
    <widget name="text" position="650,666" size="883,158" zPosition="5" halign="left" font="Caviar_bold; 22" backgroundColor="un6e6e6e" foregroundColor="white" transparent="1" />
    <panel name="menu_template_net" />
    <panel name="button_template_rava_n" />
     </screen>"""
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("OpenPlusHD! Skin Configuration"))
		self.list = []
                self.list.append(getConfigListEntry(_("Skinpanel in Menu"), config.plugins.skinpanel.onmenu))
		self.list.append(getConfigListEntry(_("Weather Yahoo in Infobar"), config.plugins.skinpanel.winfobar))
                self.list.append(getConfigListEntry(_("Weather Yahoo in SecondInfobar"), config.plugins.skinpanel.wsecinfobar))
                self.list.append(getConfigListEntry(_("Weather Foreca in Infobar"), config.plugins.skinpanel.fwinfobar))
                self.list.append(getConfigListEntry(_("Weather Foreca in SecondInfobar"), config.plugins.skinpanel.fwsecinfobar))
                self.list.append(getConfigListEntry(_("Weather Yahoo in Mediaplayer EMC"), config.plugins.skinpanel.wemc))
                self.list.append(getConfigListEntry(_("Bitrate in Infobar"), config.plugins.skinpanel.btinfobar))
                self.list.append(getConfigListEntry(_("Menu Extended, with icons"), config.plugins.skinpanel.extmenu))
                self.list.append(getConfigListEntry(_("Event Name runnig text in Infobar"), config.plugins.skinpanel.eventname))
                self.list.append(getConfigListEntry(_("Event Name runnig text in second Infobar"), config.plugins.skinpanel.seceventname))
                self.list.append(getConfigListEntry(_("Event Description runnig text in second Infobar"), config.plugins.skinpanel.secdescript))
                self.list.append(getConfigListEntry(_("Camd/ECM Info in second Infobar"), config.plugins.skinpanel.sececminf))
                self.list.append(getConfigListEntry(_("Crypt Info in second Infobar"), config.plugins.skinpanel.seccryptinf))
                self.list.append(getConfigListEntry(_("Frequency Info in second Infobar"), config.plugins.skinpanel.secfrec))
                self.list.append(getConfigListEntry(_("Provider Info in second Infobar"), config.plugins.skinpanel.secprov))
                self.list.append(getConfigListEntry(_("Signal Info in second Infobar"), config.plugins.skinpanel.secmini))
		ConfigListScreen.__init__(self, self.list, session=session)
		self["text"] = ScrollLabel("")
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		#self["key_yellow"] = StaticText(_("Get data"))
                #self["key_blue"] = StaticText(_("Restart  GUI"))
		self["text"].setText(help_txt)
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
                        "ok": self.save,
			#"yellow": self.getdata,
                        #"blue": self.restartGUI,
		}, -2)
		if os.path.isfile("/etc/.openplushdrun"):
                        os.remove("/etc/.openplushdrun")
                        self.save(False)


	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close(False)

	#def restartGUI(self):
                #self.session.open(TryQuitMainloop, 3)
                
        def Restartbox(self, val):
		if val:
			self.session.open(TryQuitMainloop, 3)
		else:
			self.close()  

        def save(self, mode = True):
          if mode:
            self.session.openWithCallback(self.Restartbox,MessageBox,_('Restart your %s %s to apply settings\nRestart now?') % (getMachineBrand(), getMachineName()), MessageBox.TYPE_YESNO)
          for i in self["config"].list:
            i[1].save()
            configfile.save()
            ##
            ## All changes off by default
            ##
            self.cstring("/usr/share/enigma2/openplusHD/skin_infobars.xml",'<panel name="menu_template_infobar_bitrate" />', '<panel name="menu_template_infobar_bitrate_off" />')
            print "Bitrate in infobar off"
            if config.plugins.skinpanel.btinfobar.value:
              self.cstring("/usr/share/enigma2/openplusHD/skin_infobars.xml", '<panel name="menu_template_infobar_bitrate_off" />', '<panel name="menu_template_infobar_bitrate" />')
              print "Bitrate in infobar on"
              
            self.cstring("/usr/share/enigma2/openplusHD/skin_infobars.xml",'<panel name="menu_template_infobar_yweather" />', '<panel name="menu_template_infobar_yweather_off" />')
            print "weather in infobar off"
            if config.plugins.skinpanel.winfobar.value:
              self.cstring("/usr/share/enigma2/openplusHD/skin_infobars.xml", '<panel name="menu_template_infobar_yweather_off" />', '<panel name="menu_template_infobar_yweather" />')
              print "weather in infobar on"
              
            self.cstring("/usr/share/enigma2/openplusHD/skin_secinfobars.xml",'<panel name="menu_template_infobar_yweather" />', '<panel name="menu_template_infobar_yweather_off" />')
            print "weather in secinfobar off"
            if config.plugins.skinpanel.wsecinfobar.value:
              self.cstring("/usr/share/enigma2/openplusHD/skin_secinfobars.xml", '<panel name="menu_template_infobar_yweather_off" />', '<panel name="menu_template_infobar_yweather" />')
              print "weather in secinfobar on"
              
            self.cstring("/usr/share/enigma2/openplusHD/skin_infobars.xml",'<panel name="menu_template_infobar_fweather" />', '<panel name="menu_template_infobar_fweather_off" />')
            print "weather in infobar off"
            if config.plugins.skinpanel.fwinfobar.value:
              self.cstring("/usr/share/enigma2/openplusHD/skin_infobars.xml", '<panel name="menu_template_infobar_fweather_off" />', '<panel name="menu_template_infobar_fweather" />')
              print "weather in infobar on"
              
            self.cstring("/usr/share/enigma2/openplusHD/skin_secinfobars.xml",'<panel name="menu_template_infobar_fweather" />', '<panel name="menu_template_infobar_fweather_off" />')
            print "weather in secinfobar off"
            if config.plugins.skinpanel.fwsecinfobar.value:
              self.cstring("/usr/share/enigma2/openplusHD/skin_secinfobars.xml", '<panel name="menu_template_infobar_fweather_off" />', '<panel name="menu_template_infobar_fweather" />')
              print "weather in secinfobar on"  
            
            self.cstring("/usr/share/enigma2/openplusHD/skin.xml",'<panel name="menu_template_infobar_yweather" />', '<panel name="menu_template_infobar_yweather_off" />')
            print "weather in EMC off"
            if config.plugins.skinpanel.wemc.value:
              self.cstring("/usr/share/enigma2/openplusHD/skin.xml", '<panel name="menu_template_infobar_yweather_off" />', '<panel name="menu_template_infobar_yweather" />')
              print "weather in EMC on"
            
            self.cstring("/usr/share/enigma2/openplusHD/skin.xml",'<panel name="menu_template_icons" />', '<ePixmap pixmap="openplusHD/menu/menup.png" position="385,428" size="250,359" alphatest="blend" zPosition="-12" />')
            print "Extended menu off"
            if config.plugins.skinpanel.extmenu.value:
              self.cstring("/usr/share/enigma2/openplusHD/skin.xml", '<ePixmap pixmap="openplusHD/menu/menup.png" position="385,428" size="250,359" alphatest="blend" zPosition="-12" />', '<panel name="menu_template_icons" />')
              print "Extended menu on"
              
            self.cstring("/usr/share/enigma2/openplusHD/skin_infobars.xml",'<panel name="menu_template_infobar_eventnamerun" />', '<panel name="menu_template_infobar_eventname" />')
            print "EventName infobar off"
            if config.plugins.skinpanel.eventname.value:
              self.cstring("/usr/share/enigma2/openplusHD/skin_infobars.xml", '<panel name="menu_template_infobar_eventname" />', '<panel name="menu_template_infobar_eventnamerun" />')
              print "EventName infobar run on"  
              
            self.cstring("/usr/share/enigma2/openplusHD/skin_secinfobars.xml",'<panel name="menu_template_infobar_eventnamerun" />', '<panel name="menu_template_infobar_eventname" />')
            print "EventName run secinfobar off"
            if config.plugins.skinpanel.seceventname.value:
              self.cstring("/usr/share/enigma2/openplusHD/skin_secinfobars.xml", '<panel name="menu_template_infobar_eventname" />', '<panel name="menu_template_infobar_eventnamerun" />')
              print "EventName run secinfobar run on"  
            
            self.cstring("/usr/share/enigma2/openplusHD/skin_secinfobars.xml",'<panel name="menu_template_infobar_descriptionrun" />', '<panel name="menu_template_infobar_description" />')
            print "Description secinfobar off"
            if config.plugins.skinpanel.secdescript.value:
              self.cstring("/usr/share/enigma2/openplusHD/skin_secinfobars.xml", '<panel name="menu_template_infobar_description" />', '<panel name="menu_template_infobar_descriptionrun" />')
              print "Description secinfobar run on"
              
            self.cstring("/usr/share/enigma2/openplusHD/skin_secinfobars.xml",'<panel name="menu_template_camcryptecm" />', '<panel name="menu_template_camcryptecm_off" />')
            print "CAM/ECM secinfobar off"
            if config.plugins.skinpanel.sececminf.value:
              self.cstring("/usr/share/enigma2/openplusHD/skin_secinfobars.xml", '<panel name="menu_template_camcryptecm_off" />', '<panel name="menu_template_camcryptecm" />')
              print "CAM/ECM secinfobar on"    
            
            self.cstring("/usr/share/enigma2/openplusHD/skin_secinfobars.xml",'<panel name="menu_template_provider" />', '<panel name="menu_template_provider_off" />')
            print "provider secinfobar off"
            if config.plugins.skinpanel.secprov.value:
              self.cstring("/usr/share/enigma2/openplusHD/skin_secinfobars.xml", '<panel name="menu_template_provider_off" />', '<panel name="menu_template_provider" />')
              print "provider secinfobar on"    
        
            self.cstring("/usr/share/enigma2/openplusHD/skin_secinfobars.xml",'<panel name="menu_template_frec" />', '<panel name="menu_template_frec_off" />')
            print "frec secinfobar off"
            if config.plugins.skinpanel.secfrec.value:
              self.cstring("/usr/share/enigma2/openplusHD/skin_secinfobars.xml", '<panel name="menu_template_frec_off" />', '<panel name="menu_template_frec" />')
              print "frec secinfobar on"
              
            self.cstring("/usr/share/enigma2/openplusHD/skin_secinfobars.xml",'<panel name="menu_template_mini_health" />', '<panel name="menu_template_mini_health_off" />')
            print "mini_health secinfobar off"
            if config.plugins.skinpanel.secmini.value:
              self.cstring("/usr/share/enigma2/openplusHD/skin_secinfobars.xml", '<panel name="menu_template_mini_health_off" />', '<panel name="menu_template_mini_health" />')
              print "mini_health secinfobar on"
            
            self.cstring("/usr/share/enigma2/openplusHD/skin_secinfobars.xml",'<panel name="menu_template_crypto_info" />', '<panel name="menu_template_crypto_info_off" />')
            print "cryptinfo secinfobar off"
            if config.plugins.skinpanel.seccryptinf.value:
              self.cstring("/usr/share/enigma2/openplusHD/skin_secinfobars.xml", '<panel name="menu_template_crypto_info_off" />', '<panel name="menu_template_crypto_info" />')
              print "cryptinfo secinfobar on"  
                     
        def cstring(self,filename, char_a, char_b):
          file = open(filename, "r")
          buffer = file.read()
          file.close()
          file = open(filename, "w")
          file.write(buffer.replace(char_a, char_b))
          file.close()


def main(session, **kwargs):
  session.open(skinpanel_setup)
  
  
def menu(menuid, **kwargs):
	if menuid == "mainmenu":
		return [(_("OpenPlusHD SkinPanel"), main, "OpenPlusHD SkinPanel", 7)]
	return []

def Plugins(**kwargs):
	if config.plugins.skinpanel.onmenu.value:
		result = [
		PluginDescriptor(name=_("OpenPlusHD SkinPanel"),
		where=PluginDescriptor.WHERE_MENU,
		fnc=menu),
		PluginDescriptor(name=_("OpenPlusHD SkinPanel"),
		description=_("Configure OpenPlusHD Skin"),
		where = [PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU],
		icon="skin.png",
		fnc=main)
		]
		return result
	else:
		result = [
		PluginDescriptor(name=_("OpenPlusHD SkinPanel"),
		description=_("Your city weather for Openplus!"),
		where = [PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU],
		icon="skin.png",
		fnc=main)
		]
		return result
