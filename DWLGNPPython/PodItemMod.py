#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

PodItemMod.py
Created on 24/jul/2013

@author: friend
'''
import codecs, os #, sys  #from lxml import etree
import xml.etree.ElementTree as ET
from PodItemUtils import get_pydate_from_german_str_date

import __init__; __init__._insert_parent_dir_to_path_if_needed()
import local_settings as ls

class PodItemCannotBeInstantiated(ValueError):
  pass

class PodItem(object):
  '''
  This class models a RSS item-tag element with the following characteristics:
  1) it recognizes its "item" xml-trunk by searching the date
     that is placed at the beginning of the <title>-tag
  2) once having its "item" xml-trunk, it can access its mp3 URL,
     so download its corresponding audio mp3, when invoked
  3) it also can extract the audio transcript that is available through the <description>-tag
  
  At the end, there are only two pieces of information that will be locally stored, ie:
  1) the audio mp3;
  2) the audio transcript text.
  
  This program is sensitive to the way the date is informed in the XML, because it does not
    have a proper tag for itself. If the process that mounts the XML is changed and if this
    change also modifies the position or format of the identifying date, this program
    will possibly stop working, ie, it's dependent on the assumptions that the other-side-XML will
    be maintained the way it is now.   
  '''

  def __init__(self, item_obj):
    if item_obj == None:
      raise PodItemCannotBeInstantiated, 'item_obj is None, it should an XML ElementTree'
    self.create_attribs_before_init_attribs()
    self.item_obj = item_obj
    self.init_attribs()
    
  def create_attribs_before_init_attribs(self):
    self.poditem_date       = None
    self.poditem_title      = None
    self.poditem_mp3_url    = None
    self.poditem_transcript = None
  
  def init_attribs(self):
    self.init_poditem_date_and_title()
    self.init_poditem_mp3_url()
    self.init_poditem_transcript()

  def init_poditem_date_and_title(self):
    title_obj = self.item_obj.find('title')
    if title_obj == None:
      raise PodItemCannotBeInstantiated, '<title> tag has not been found'
    self.poditem_title = title_obj.text
    try:
      german_str_date = self.poditem_title.split(' ')[0] 
      self.poditem_date = get_pydate_from_german_str_date(german_str_date)
    except IndexError:
      raise PodItemCannotBeInstantiated, 'Expected initial German date has not been found'
    
  def init_poditem_mp3_url(self):
    '''
      <enclosure url="http://radio-download.dw.de/Events/podcasts/de/2288_DKpodcast_lgn_de/19C7028F_1-podcast-2288-16972987.mp3" 
        type="audio/mpeg" length="3111056"/>
    '''
    enclosure = self.item_obj.find('enclosure')
    if enclosure == None:
      raise PodItemCannotBeInstantiated, '<enclosure> tag has not been found'
    # AttributeError may be raised if enclosure.text has not the attribute 'text' 
    self.poditem_mp3_url = enclosure.get('url')
    if self.poditem_mp3_url == None:
      raise PodItemCannotBeInstantiated, 'Mp3 URL has not been found'
      
    
  def init_poditem_transcript(self):
    description = self.item_obj.find('description')
    if description == None:
      raise PodItemCannotBeInstantiated, '<description> tag has not been found'
    # AttributeError may be raised if enclosure.text has not the attribute 'text' 
    self.poditem_transcript = description.text
  
  def form_german_date_dict(self):
    '''
    This is just a helper method to help interpolate the date into the title string and 
      adds some also explanatory content to this OO class.
    '''
    intday   = self.poditem_date.day
    intmonth = self.poditem_date.month
    intyear  = self.poditem_date.year
    return {'intday':intday, 'intmonth':intmonth,'intyear':intyear}
    
  def download_mp3(self):
    os.chdir(ls.get_media_data_dir_abspath(self.poditem_date.year, self.poditem_date.month))
    comm = 'wget -c "%s"' %self.poditem_mp3_url
    print self.poditem_title
    print 'Downloading', self.poditem_mp3_url
    ans = raw_input('Confirm (Y*/n) ? ')
    if ans in ['n', 'N']:
      return
    os.system(comm)

  def fetch_mp3_and_save_transcript(self):
    '''
    The <title>-tag starts as in the following example:
     
     <title>24.07.2013 – Langsam gesprochene Nachrichten</title>
    
    ie, the string '24.07.2013' is a German-formatted-date that is extracted at the beginning of the title.
    Read also the docstring above for the whole class
    '''
    german_date_str = '%(intday)02d.%(intmonth)02d.%(intyear)02d' %self.form_german_date_dict()
    root = ET.XML(self.rss_xml_data)
    nodes = root.find('//item')
    for node in nodes:
      if node.text.startswith(german_date_str):
        item = node.getparent()
        enclosure = item.get('enclosure')
        url = enclosure.get('url')
        print url
        description = item.get('description')
        print description 

  def write_individual_transcription_file(self):
    extensionless_filename = self.poditem_title
    if extensionless_filename == None or extensionless_filename == '':
      return
    # protect this line below at next refactoring!!!
    output_filename = extensionless_filename[ len('dd.mm.yyyy ') : ]
    date_prefix = '%d-%02d-%02d' %(self.poditem_date.year, self.poditem_date.month, self.poditem_date.day) 
    output_filename   = '%s %s.txt' %(date_prefix, output_filename)
    output_text       = unicode(self.poditem_title + '\n\n' + self.poditem_transcript)
    data_dir_abspath  = ls.get_media_data_dir_abspath(self.poditem_date.year, self.poditem_date.month)
    outfile_abspath   = os.path.join(data_dir_abspath, output_filename)
    file_and_location = '%s in %s' %(output_filename, data_dir_abspath)
    if os.path.isfile(outfile_abspath):
      print file_and_location
      print '  ==>> already exists.'
      return
    outfile = codecs.open(outfile_abspath, 'w', encoding='utf-8')
    print 'Saving', file_and_location
    outfile.write(output_text)
    outfile.close()

  def form_attribs_dict(self):
    return {                                            
      'poditem_date'       :self.poditem_date         ,        
      'poditem_title'      :self.poditem_title        , 
      'poditem_mp3_url'    :self.poditem_mp3_url      , 
      'poditem_transcript' :self.poditem_transcript   , 
    }
    
  def __unicode__(self):
    outstr = unicode('''PodItem:
    poditem_title     = %(poditem_title)s  
    poditem_date      = %(poditem_date)s       
    poditem_mp3_url   = %(poditem_mp3_url)s
    ---------------------------------------------------------------------  
    poditem_transcript:
       %(poditem_transcript)s
    ''') %self.form_attribs_dict()
    return outstr

  def __str__(self):
    return unicode(self.__unicode__())

def test1():
  item_text = '''<?xml version="1.0" encoding="UTF-8"?>
  <item>
   <title>25.07.2013 – Langsam gesprochene Nachrichten</title>
   <link>http://www.dw.de/25-07-2013-langsam-gesprochene-nachrichten/a-16975221?maca=de-DKpodcast_lgn_de-2288-xml-mrss</link>
   <description>Trainiere dein Hörverstehen mit den Nachrichten der Deutschen Welle von Donnerstag – als Text und als verständlich gesprochene Audio-Datei.
  ***

  In Nordspanien sind bei einem schweren Zugunglück mindestens 77 Menschen ums Leben gekommen. Mindestens 130 wurden verletzt. Es sei nicht auszuschließen, dass noch weitere Tote und Verletzte gefunden würden, teilten die Behörden mit. Das Unglück ereignete sich in der autonomen Provinz Galicien. Der Schnellzug kam aus Madrid und war kurz vor dem Bahnhof von Santiago de Compostela entgleist. Laut ersten Informationen soll er zu schnell in eine Kurve eingebogen sein. Mehrere der Waggons hatten sich ineinander verkeilt und wurden völlig zerstört. Ministerpräsident Mariano Rajoy zeigte sich tief betroffen und kündigte an, sich direkt am Unfallort ein Bild der Lage zu machen. In Berlin sprach Außenminister Guido Westerwelle den Angehörigen der Opfer sein Mitgefühl aus.

  ***

  Die USA liefern Ägypten wegen der Unruhen seit dem Sturz von Präsident Mohammed Mursi vorerst keine weiteren Kampfjets. Angesichts der gegenwärtigen Lage in Ägypten sei es derzeit nicht angemessen, mit der Lieferung von F-16-Kampfflugzeugen fortzufahren, sagte ein Pentagon-Sprecher in Washington. Verteidigungsminister Chuck Hagel habe Armeechef Abdel Fattah al-Sisi von der Entscheidung unterrichtet, hieß es. Vorgesehen war die Lieferung vier weiterer Kampfjets. Unklar ist, was aus den 1,3 Milliarden US-Dollar an Militärhilfe wird, die Washington jedes Jahr nach Kairo schickt. Die USA dürfen eigentlich Machthabern, die eine demokratische Regierung zu Fall bringen, keine Unterstützung gewähren. Washington vermeidet es bisher, von einem Staatsstreich in Ägypten zu sprechen.

  ***

  Papst Franziskus hat die Gesellschaft zum Kampf gegen die Drogen-Kartelle aufgerufen und vor einer Legalisierung von Rauschgift gewarnt. Das Kirchenoberhaupt besuchte in Brasilien eine Suchtklinik. In dem Hospital São Francisco de Assis informierte er sich bei Drogenkranken und Ärzten über deren Probleme. Eine Liberalisierung des Drogenkonsums, wie in Teilen Lateinamerikas diskutiert, sei kein geeignetes Mittel gegen die Sucht. Man müsse die dahinter liegenden Probleme angehen, indem man sich etwa für mehr Gerechtigkeit einsetze, erklärte der Papst.

  ***

  In der Spähaffäre steht die Bundesregierung weiter unter Druck. Zur Aufklärung der Praktiken soll an diesem Donnerstag Kanzleramtsminister Ronald Pofalla im Parlamentarischen Kontrollgremium in Berlin beitragen. Der CDU-Politiker ist Koordinator der Geheimdienste und damit auch zuständig für die Frage, inwieweit es eine Zusammenarbeit zwischen Deutschland und den USA beim Abhören gegeben hat. Unterdessen hat das Repräsentantenhaus in Washington entschieden, dass der amerikanische Geheimdienst NSA auch künftig Telefongespräche von US-Bürgern im großen Stil überwachen darf. Die Parlamentskammer stimmte mit 217 zu 205 Stimmen gegen einen Antrag des Republikaners Justin Amash, der dem Programm straffere Zügel anlegen wollte.

  ***

  US-Präsident Barack Obama will mit einem Investitionsprogramm die Mittelschicht im Land stärken. Er sprach sich in einer Grundsatzrede in der Kleinstadt Galesburg in seinem Heimatstaat Illinois für einen Ausbau von Infrastruktur und Bildungssystem aus. Einzelheiten zur Frage, wie die Industrie in den USA gestärkt werden solle, werde er in den kommenden Wochen vorlegen, fügte der Präsident hinzu. Obama sagte weiter, er wolle den Aufbau der Altersvorsorge mit neuen Steuervergünstigungen fördern. Zudem versprach er eine &quot;aggressive&quot; Strategie, um das Bildungssystem auf Vordermann zu bringen. Im Herbst stehen die nächsten Verhandlungen zwischen Obamas Demokraten und den Republikanern über den Haushalt an, zudem geht es um die Anhebung der Schulden-Obergrenze. Bislang haben die Republikaner Reformvorhaben des Präsidenten blockiert.</description>
   <enclosure url="http://radio-download.dw.de/Events/podcasts/de/2288_DKpodcast_lgn_de/AD0A26D6_1-podcast-2288-16975221.mp3" type="audio/mpeg" length="3334656"/>  
   <pubDate>Thu, 25 Jul 2013 09:43:00 GMT</pubDate>
  </item>
  '''
  item_obj = ET.fromstring(item_text)
  poditem = PodItem(item_obj)
  #print poditem.__unicode__()
  import sys
  sys.stdout.write(poditem.__str__())
  # print(poditem)

'''
    #self.rss_xml_data = open(ls.get_poditems_rss_xml_abspath()).read()    
    root = ET.fromstring(self.rss_xml_data)
    channel = root.getchildren()[0]
    items = channel.findall('item')

'''

def process():
  test1()
        
if __name__ == '__main__':
  process()
