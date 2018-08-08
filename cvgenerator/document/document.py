from pylatex import Document, TikZ, PageStyle, Package, Head, Command, NoEscape, UnsafeCommand, NewPage, Tabular, \
	TextColor, FlushRight, Section, MultiColumn, Tabularx, Itemize, VerticalSpace, NewLine
from pylatex.base_classes import CommandBase, Environment
from pylatex.utils import bold
import json
import requests


class SubtitleCommand(CommandBase):
	"""
	A class representing a custom LaTeX command.

	This class represents a custom LaTeX command named
	``exampleCommand``.
	"""

	_latex_name = 'subtitle'
	packages = [Package('titling')]


class MulticolsEnvironment(Environment):
	"""A class to wrap LaTeX's alltt environment."""
	_latex_name = 'multicols'
	packages = [Package('multicol')]

def addHeaderImage(doc, image_path):
	doc.packages.append(Package('fancyhdr'))
	doc.packages.append(Package('tikzpagenodes'))
	doc.preamble.append(Command("usetikzlibrary", "calc"))

	header = PageStyle("header")
	headerImage = TikZ(options=["remember picture", "overlay"])
	drawCommand = '\draw  let \p1=($(current page.north)-(current page header area.south)$), \
	\\n1={veclen(\\x1,\y1)} in \
	node [opacity = 0.5,inner sep=0,outer sep=0,below right] \
	at (current page.north west){\includegraphics[width=\paperwidth,height=\\n1]{' + image_path + '}};'
	headerImage.append(NoEscape(drawCommand))
	with header.create(Head("L")):
		header.append(headerImage)

	doc.preamble.append(header)
	doc.change_document_style("header")


def defineColor(colorName, rValue, gValue, bValue):
	doc.add_color(name=colorName, model="RGB", description='%s, %s, %s' % (str(rValue), str(gValue), str(bValue)))


def defineAdditionalUtil(doc):
	defineColor('lightgray', 220, 220, 220)
	defineColor('darkgray', 197, 197, 197)
	defineColor('sectiongray', 137, 139, 144)
	defineColor('cegekagreen', 122, 178, 40)
	defineColor('cegekablue', 51, 107, 159)

	doc.packages.append(Package('tabularx'))
	doc.preamble.append(
		Command('newcolumntype', arguments='g', extra_arguments=NoEscape('>{\\columncolor{lightgray}}l')))
	doc.preamble.append(Command('newcolumntype', arguments='L', options=1, extra_arguments=NoEscape(
		'>{\\raggedright\let\\newline\\\\\\arraybackslash\hspace{0pt}}m{#1}')))
	doc.preamble.append(Command('newcolumntype', arguments='C', options=1, extra_arguments=NoEscape(
		'>{\\centering\let\\newline\\\\\\arraybackslash\hspace{0pt}}m{#1}')))
	doc.preamble.append(Command('newcolumntype', arguments='R', options=1, extra_arguments=NoEscape(
		'>{\\raggedleft\let\\newline\\\\\\arraybackslash\hspace{0pt}}m{#1}')))


	doc.packages.append(Package('titling'))
	doc.preamble.append(Command('pretitle', NoEscape('\\begin{flushright}\\LARGE')))
	subtitle_command = UnsafeCommand('newcommand', '\subtitle', options=1,
									 extra_arguments=r'\posttitle{ \par\end{flushright} \begin{flushright}\large{\bfseries\color{cegekablue} #1 }\end{flushright} \vspace{-5ex}}')
	doc.preamble.append(subtitle_command)


def setSectionColor(doc, color):
	doc.packages.append(Package('titlesec'))
	doc.preamble.append(Command('titleformat', NoEscape('\\section'),
								extra_arguments=[NoEscape('\\color{%s}\\normalfont\\Large\\bfseries' % color),
												 NoEscape('\\color{%s}\\thesection' % color), '1em', '']))


def setTableLinesColor(doc, color):
	doc.packages.append(Package('colortbl'))
	doc.preamble.append(Command('arrayrulecolor', color))


def defineStyleOptions(doc):
	doc.packages.append(Package('fontspec'))
	doc.preamble.append(Command('setmainfont', 'Calibri'))

	setSectionColor(doc, 'sectiongray')
	setTableLinesColor(doc, 'darkgray')
	doc.preamble.append(NoEscape('\\def\\arraystretch{1.5}'))
	doc.preamble.append(Command('setlength', NoEscape('\\parindent'), extra_arguments=['0pt']))


def setTitle(doc, name, job_title):
	doc.preamble.append(Command('title', 'CV ' + name))
	doc.preamble.append(Command('subtitle', job_title))
	doc.preamble.append(Command('date', ''))


def addIntro(doc):
	with doc.create(MulticolsEnvironment(arguments="2")) as multicolsEnvironment:
		with doc.create(Tabular('ll')) as table:
			table.add_row((TextColor('cegekablue', bold('Geboortedatum:')), '01/01/1991'))
			table.add_row((TextColor('cegekablue', bold('Geslacht:')), 'M'))
			table.add_row((TextColor('cegekablue', bold('Nationaliteit:')), 'Belg'))
		multicolsEnvironment.append(Command('columnbreak'))
		with doc.create(FlushRight()) as flushright:
			flushright.append("Profielbeschrijving - overzicht van vakkundigheid en ervaring")


def addProfessionalExperience(doc):
	doc.append(Section("PROFESSIONELE ERVARING", numbering=False))
	with doc.create(Tabularx('g X', width=2)) as tabularx:
		tabularx.append(Command('rowcolor', 'cegekagreen'))
		tabularx.add_row([MultiColumn(2, align='l', data=TextColor('white', bold('CEGEKA')))])
		tabularx.add_row([bold("Periode"), "Augustus 1900 - Juni 1901"])
		tabularx.add_hline()
		tabularx.add_row([bold("Klant"), ""])
		tabularx.add_hline()
		tabularx.add_row([bold("Project"), ""])
		tabularx.add_hline()
		tabularx.add_row([bold("Rol"), ""])
		tabularx.add_hline()
		tabularx.add_row([bold("Omschrijving"), ""])
		tabularx.add_hline()
		verantwoordelijkheden = Itemize()
		verantwoordelijkheden.add_item("verantwoordelijkheid 1")
		verantwoordelijkheden.add_item("verantwoordelijkheid 2")
		tabularx.add_row([bold("Verantwoordelijkheden"), verantwoordelijkheden])
		tabularx.add_hline()
		tabularx.add_row([bold("Omgeving"), ""])
		tabularx.add_hline()


def addTraining(doc, trainings):
	doc.append(Section("OPLEIDING", numbering=False))

	with doc.create(Tabularx('X | l | c')) as tabularx:
		tabularx.append(Command('rowcolor', 'cegekagreen'))
		tabularx.add_row([TextColor('white', bold('DIPLOMA')), TextColor('white', bold('INSTELLING')), TextColor('white', bold('JAAR'))])
		tabularx.add_row(['Bachelor Informatica', 'KU Leuven', '2000'])
		tabularx.add_hline()
		tabularx.add_row(['Bachelor Informatica', 'KU Leuven', '2000'])
		tabularx.add_hline()

	doc.append(NewLine())
	doc.append(VerticalSpace('1.5cm'))

	with doc.create(Tabularx('X | l | c')) as tabularx:
		tabularx.append(Command('rowcolor', 'cegekagreen'))
		tabularx.add_row([TextColor('white', bold('CERTIFICATEN')), TextColor('white', bold('INSTELLING')), TextColor('white', bold('JAAR'))])
		tabularx.add_row(['Certified Java', 'Oracle', '2000'])
		tabularx.add_hline()
		tabularx.add_row(['Certified Java', 'Oracle', '2000'])
		tabularx.add_hline()

	doc.append(NewLine())
	doc.append(VerticalSpace('1.5cm'))

	with doc.create(Tabularx('X | l | c')) as tabularx:
		tabularx.append(Command('rowcolor', 'cegekagreen'))
		tabularx.add_row([TextColor('white', bold('TRAINING/CURSUSSEN')), TextColor('white', bold('INSTELLING')), TextColor('white', bold('JAAR'))])
		for training in trainings:
			tabularx.add_row([training['title'], training['organisation'], training['year']])
			tabularx.add_hline()


def addTitle(doc, name, job_title):
	setTitle(doc, name, job_title)
	doc.append(Command('maketitle'))
	doc.change_page_style("fancy")


if __name__ == '__main__':
	username = 'pieterb'
	url = 'http://cvtool-cgk-node.azurewebsites.net/graphql'
	data = '{"query":"{employeeByAdName(adName:\\\"' + username + '\\\"){id,firstName,lastName,projects{name},technologyRatings{name}}}"}'
	response = requests.post(url, data=data,headers={'Content-Type':'application/json'})
	employeeData = response.json()['data']['employeeByAdName'][0]
	firstName = employeeData['firstName']
	lastName = employeeData['lastName']
	trainings = []
	job_title = ""

	# with open('../resources/employee.json') as json_data:
	# 	employeeData = json.load(json_data)
	#
	# firstName = employeeData['firstName']
	# lastName = employeeData['lastName']
	# job_title = employeeData['job title']
	# trainings = employeeData['trainings']

	geometry_options = {"top": "4cm", "bottom": "2.5cm", "left": "2.5cm", "right": "2.5cm", "headsep": "0cm"}

	doc = Document(geometry_options=geometry_options)

	defineAdditionalUtil(doc)

	defineStyleOptions(doc)


	addHeaderImage(doc, '../resources/header.png')
	addTitle(doc, firstName + ' ' + lastName, job_title)
	addIntro(doc)
	addProfessionalExperience(doc)
	addTraining(doc, trainings)

	doc.generate_pdf("template", compiler='LuaLaTeX')
