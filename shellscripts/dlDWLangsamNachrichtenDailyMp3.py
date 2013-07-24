#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

This script picks up all YouTube video ids on the local directory and downwards from it.
The video ids that can be found are those that end a filename before its extension.

Created on 05/jul/2013

@author: friend
'''

from datetime import date, timedelta
from lxml import etree

DW_LANGSAM_NACHRICHTEN_PODCAST_RSS_URL = 'http://rss.dw.de/xml/DKpodcast_lgn_de'

class PodcastItem(object):
  '''
   <item>
     <guid isPermaLink="true">http://www.dw.de/24-07-2013-langsam-gesprochene-nachrichten/a-16972987?maca=de-DKpodcast_lgn_de-2288-xml-mrss</guid>
     <title>24.07.2013 – Langsam gesprochene Nachrichten</title>
     <link>http://www.dw.de/24-07-2013-langsam-gesprochene-nachrichten/a-16972987?maca=de-DKpodcast_lgn_de-2288-xml-mrss</link>
     <description>Trainiere dein Hörverstehen mit den Nachrichten der Deutschen Welle von Mittwoch – als Text und als verständlich gesprochene Audio-Datei.
    ***
  
    Bei Protesten gegen die Regierung in Bulgarien ist es zu schweren Ausschreitungen zwischen Demonstranten und der Polizei gekommen. Mit einem massiven Aufgebot hatten die Sicherheitskräfte eine Blockade des Parlamentsgebäudes aufgelöst. Die dort festsitzenden rund 100 Minister, Abgeordneten, Gewerkschafter und Experten wurden in Sicherheit gebracht. Laut Staatsmedien wurden zehn Menschen verletzt, darunter zwei Polizisten. Mit der Blockade wollten die Menschen gegen eine Aufstockung des Haushalts 2013 protestieren. Präsident Rosen Plewneliew rief zur Ruhe auf, damit eine weitere Eskalation vermieden werde. Aus Wut über Korruption, Vetternwirtschaft und Verelendung gehen seit Mitte Juni jeden Abend tausende Bulgaren auf die Straße. Das südosteuropäische Land steckt in einer tiefen politischen Krise, seit die konservative Vorgängerregierung im Februar nach monatelangen Protesten das Handtuch warf. Die vorgezogene Parlamentswahl im Mai hatte eine politische Pattsituation hervorgebracht
  
    ***
  
    Mit Musikdarbietungen und einem großen Open-Air-Gottesdienst am berühmten Strand von Copacabana in Rio de Janeiro ist der 28. Weltjugendtag der katholischen Kirche eröffnet worden. Trotz zeitweilig strömenden Regens und einem Temperatursturz auf 15 Grad kamen mehrere hunderttausend Jugendliche aus aller Welt zu dem Gelände am Meer. Papst Franziskus, der sich bereits in Brasilien aufhält, wird erstmals am Donnerstag mit den Jugendlichen zusammenkommen. Insgesamt werden zum Weltjugendtag bis zu zwei Millionen Teilnehmer aus rund 170 Ländern erwartet, unter ihnen knapp 2.000 aus Deutschland.
  
    ***
  
    Vor der Küste Indonesiens ist ein Boot mit Flüchtlingen gesunken. Mindestens drei Menschen kamen ums Leben, rund 160 konnten aus stürmischer See vor der Westküste der Hauptinsel Java gerettet werden. Die Überlebenden kamen nach Angaben der Polizei aus Bangladesch, Sri Lanka, Irak und aus dem Iran. Jedes Jahr versuchen Tausende Flüchtlinge von Indonesien aus, in oft überladenen und nicht seetüchtigen Booten nach Australien zu gelangen. Nach australischen Angaben erreichten seit Jahresbeginn bereits 15.000 Flüchtlinge auf illegalen Wegen ihr Ziel. Der Umgang mit ihnen ist ein wichtiges Thema vor der Parlamentswahl im September. Am Freitag hatte Premierminister Kevin Rudd mitgeteilt, gemäß einem mit Papua-Neuguinea geschlossenen Abkommen würden Bootsflüchtlinge künftig dorthin geschickt.
  
    ***
  
    Im Südsudan hat Staatschef Salva Kiir das gesamte Kabinett entlassen. Wie der ebenfalls von seinem Amt entbundene bisherige Informationsminister Barnaba Marial Benjamin in der Hauptstadt Juba mitteilte, machte Kiir zwei Jahre nach der Unabhängigkeit Südsudans von seinem verfassungsmäßigen Recht Gebrauch, die Regierung umzubilden. Neubesetzungen wurden zunächst nicht mitgeteilt. Ein starkes Aufgebot der Sicherheitskräfte ist im Einsatz. Erst im Juni hatte Kiir zwei wichtige Minister unter dem Vorwurf der Verwicklung in einen Korruptionsskandal entlassen. Im vergangenen Jahr sorgte er zudem für die Entlassung von dutzenden Generälen. Dem erst 2011 unabhängig gewordenen Land drohen zudem ab der kommenden Woche enorme wirtschaftliche Probleme. Dann soll die Ölproduktion eingestellt werden, nachdem der Sudan angekündigt hatte, seine Leitungen für den Transport zu schließen. Die meisten Ölreserven liegen zwar im Süden, das Öl wird aber über Leitungen durch den Norden nach Port Sudan transportiert. Khartum wirft Juba vor, Rebellengruppen zu unterstützen, die die sudanesische Regierung stürzen wollen.
  
    ***
  
    Die mexikanischen Sicherheitskräfte haben bei mehreren Einsätzen im ganzen Land 151 Menschen aus der Gewalt von Schleppern befreit. Allein 94 Einwanderer seien in einem Lastwagen im Bundesstaat Chiapas im Süden des Landes entdeckt worden, teilte die Einwanderungsbehörde mit. Tausende Migranten vor allem aus Mittelamerika passieren jedes Jahr Mexiko auf dem Weg in die USA. Oft werden sie Opfer krimineller Banden, die sie entführen oder zwangsrekrutieren. Im Bundesstaat Chihuahua im Norden Mexikos sind bei einem schweren Feuergefecht zwischen mutmaßlichen Angehörigen konkurrierender Drogenkartelle sechs Menschen getötet worden. Chihuahua ist seit Jahren einer der Brennpunkte im Drogenkrieg zwischen rivalisierenden Kartellen und den Sicherheitsbehörden.</description>
     <category>Deutsch XXL</category>
     <itunes:author>DW.DE | Deutsche Welle</itunes:author>
     <itunes:keywords>Langsam gesprochene Nachrichten, Deutschkurse, Deutsch lernen, lernen, langsam, Nachrichten, gesprochen, deutsch, Kurs</itunes:keywords>
     <itunes:explicit>clean</itunes:explicit>
     <enclosure url="http://radio-download.dw.de/Events/podcasts/de/2288_DKpodcast_lgn_de/19C7028F_1-podcast-2288-16972987.mp3" type="audio/mpeg" length="3111056"/>
     <itunes:duration>06:21</itunes:duration>
     <pubDate>Wed, 24 Jul 2013 08:17:00 GMT</pubDate>
  </item>
  '''

  def __init__(self, poditem_date):
    self.poditem_date = poditem_date
  
  def pickup_next_items_to_download(self):
    '''
    
    '''
    deltatime_elapsed_since = date.today() - self.poditem_date
    poditems_to_download = []
    next_date = self.poditem_date + timedelta(days=1)
    for _ in xrange(deltatime_elapsed_since.days):
      next_poditem = PodcastItem(next_date)
      poditems_to_download.append(next_poditem)
      next_date = next_date + timedelta(days=1)
    return poditems_to_download
  
  def form_german_date_dict(self):
    intday   = self.poditem_date.day
    intmonth = self.poditem_date.month
    intyear  = self.poditem_date.year
    return {'intday':intday, 'intmonth':intmonth,'intyear':intyear}
    
  def fetch_mp3_and_save_transcript(self, rss_xml_data):
    '''
     <title>24.07.2013 – Langsam gesprochene Nachrichten</title>
    24.07.2013
    '''
    german_date_str = '%(intday)02d.%(intmonth)02d.%(intyear)02d' %self.form_german_date_dict()
    root = etree.XML(rss_xml_data)
    nodes = root.find('//title')
    for node in nodes:
      if node.text.startswith(german_date_str):
        item = node.getparent()
        enclosure = item.get('enclosure')
        url = enclosure.get('url')
        print url
        description = item.get('description')
        print description 
    
    

class DwLangsamNachrichtenPodcastData(object):

  def __init__(self):
    pass
  
  def get_last_saved_item(self):
    '''
<enclosure url="http://radio-download.dw.de/Events/podcasts/de/2288_DKpodcast_lgn_de/19C7028F_1-podcast-2288-16972987.mp3" type="audio/mpeg" length="3111056"/>
         
    '''
    
    pass
  

class DwLangsamNachrichtenPodcast(object):
  
  def __init__(self):
    pass
    self.go_download_if_day_has_elapsed()
  
  def go_download_if_day_has_elapsed(self):
    podcast_data = DwLangsamNachrichtenPodcastData()
    last_item = podcast_data.get_last_saved_item() 
    items_to_download = last_item.pickup_days_yet_to_download()
    for item_to_download in items_to_download:
      item_to_download.fetch_mp3_and_save_transcript(podcast_data)


def process():
  DwLangsamNachrichtenPodcast()
        
if __name__ == '__main__':
  process()
