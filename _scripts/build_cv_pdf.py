#!/usr/bin/env python3
"""Build David Jin's printable CV from the website's rendered article.cv-content.

Usage: python3 build_cv_pdf.py INPUT_RENDERED_CV_HTML OUTPUT_PDF
Requires ReportLab only. Font discovery uses portable system fonts when present,
then ReportLab's bundled Bitstream Vera fonts. Optional CV_PDF_FONT_DIR can point
to a directory containing the LiberationSerif and LiberationSans TTF families.
The PDF contains only the current CV article, omitting details, download actions,
and repeated action links. All visible source text and unique links are retained.
"""
from __future__ import annotations

import argparse
import html
import os
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

import reportlab
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, HRFlowable, KeepTogether, PageBreak, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)


@dataclass
class Node:
    tag: str
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    def has_class(self, name):
        return name in self.attrs.get('class', '').split()

    def find_all(self, tag=None, cls=None):
        result = []
        for child in self.children:
            if isinstance(child, Node):
                if (tag is None or child.tag == tag) and (cls is None or child.has_class(cls)):
                    result.append(child)
                result.extend(child.find_all(tag, cls))
        return result


class TreeParser(HTMLParser):
    VOID = set('area base br col embed hr img input link meta param source track wbr'.split())

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('root')
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                self.stack = self.stack[:index]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def normalize(text):
    # ASCII hyphens prevent nonbreaking or unsupported dash glyphs in print.
    return re.sub(r'\s+', ' ', text.translate(str.maketrans({
        '\u2010': '-', '\u2011': '-', '\u2012': '-', '\u2013': '-',
        '\u2014': '-', '\u2212': '-', '\u00a0': ' ',
    })))


def omit(node):
    return (node.tag in {'details', 'script', 'style', 'nav', 'footer'}
            or node.has_class('cv-download')
            or (node.tag == 'a' and ('download' in node.attrs
                                    or node.attrs.get('href', '').lower().startswith('mailto:'))))


def text_of(node):
    if isinstance(node, str):
        return normalize(node)
    if omit(node):
        return ''
    if node.tag == 'br':
        return ' '
    return ''.join(text_of(c) for c in node.children)


ACCENT = '#284e66'
INK = '#22272b'
MUTED = '#5b6268'
RULE = '#aab9c2'


def markup(node):
    if isinstance(node, str):
        return html.escape(normalize(node))
    if omit(node):
        return ''
    content = ''.join(markup(c) for c in node.children)
    if node.tag == 'br':
        return '<br/>'
    if node.tag in {'strong', 'b'}:
        return f'<b>{content}</b>'
    if node.tag in {'em', 'i'}:
        return f'<i>{content}</i>'
    if node.tag in {'sup', 'sub'}:
        return f'<{node.tag}>{content}</{node.tag}>'
    if node.tag == 'a' and node.attrs.get('href'):
        url = urljoin('https://jindavid.me/', node.attrs['href'])
        return f'<link href="{html.escape(url, quote=True)}" color="{ACCENT}">{content}</link>'
    return content


def register_fonts():
    candidates = []
    if os.environ.get('CV_PDF_FONT_DIR'):
        candidates.append(Path(os.environ['CV_PDF_FONT_DIR']))
    candidates.extend([
        Path('/usr/share/fonts/truetype/liberation2'),
        Path('/usr/share/fonts/truetype/liberation'),
        Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype',
    ])
    font_dir = next((p for p in candidates if (p / 'LiberationSerif-Regular.ttf').is_file()), None)
    if font_dir:
        for alias, family in [('CVSerif', 'LiberationSerif'), ('CVSans', 'LiberationSans')]:
            for suffix, weight in [('', 'Regular'), ('-Bold', 'Bold'), ('-Italic', 'Italic'), ('-BoldItalic', 'BoldItalic')]:
                pdfmetrics.registerFont(TTFont(alias + suffix, str(font_dir / f'{family}-{weight}.ttf')))
            pdfmetrics.registerFontFamily(alias, normal=alias, bold=alias + '-Bold', italic=alias + '-Italic', boldItalic=alias + '-BoldItalic')
    else:
        font_dir = Path(reportlab.__file__).parent / 'fonts'
        for alias in ['CVSerif', 'CVSans']:
            for suffix, file in [('', 'Vera.ttf'), ('-Bold', 'VeraBd.ttf'), ('-Italic', 'VeraIt.ttf'), ('-BoldItalic', 'VeraBI.ttf')]:
                pdfmetrics.registerFont(TTFont(alias + suffix, str(font_dir / file)))
            pdfmetrics.registerFontFamily(alias, normal=alias, bold=alias + '-Bold', italic=alias + '-Italic', boldItalic=alias + '-BoldItalic')


def make_styles():
    base = dict(fontName='CVSerif', fontSize=10.6, leading=13.2, textColor=colors.HexColor(INK),
                allowWidows=0, allowOrphans=0, splitLongWords=0)
    styles = {'body': ParagraphStyle('body', **base, spaceAfter=3)}
    for name, changes in {
        'name': dict(fontName='CVSerif', fontSize=29, leading=32, spaceAfter=0),
        'label': dict(fontName='CVSans', fontSize=9.2, leading=12, textColor=colors.HexColor(MUTED), alignment=TA_RIGHT),
        'contact': dict(fontSize=10.3, leading=13, spaceAfter=0),
        'h2': dict(fontName='CVSans-Bold', fontSize=10.7, leading=13, textColor=colors.HexColor(ACCENT), spaceBefore=9, spaceAfter=3, keepWithNext=True),
        'h3': dict(fontName='CVSerif-Bold', fontSize=11.1, leading=13.5, spaceBefore=3, spaceAfter=1, keepWithNext=True),
        'meta': dict(fontSize=9.8, leading=12, textColor=colors.HexColor(MUTED), spaceAfter=3, keepWithNext=True),
        'subhead': dict(fontName='CVSans-Bold', fontSize=9.5, leading=12, spaceBefore=8, spaceAfter=5, keepWithNext=True, textColor=colors.HexColor(MUTED)),
        'pubtitle': dict(fontName='CVSerif-Bold', fontSize=11.2, leading=13.7, spaceAfter=3, keepWithNext=True),
        'authors': dict(fontSize=10.6, leading=13.2, spaceAfter=2, keepWithNext=True),
        'venue': dict(fontSize=10.2, leading=12.7, spaceAfter=0, textColor=colors.HexColor(MUTED)),
        'bullet': dict(fontSize=10.6, leading=13.2, leftIndent=10, firstLineIndent=-10, spaceAfter=2),
        'talk': dict(fontSize=10.6, leading=13.2, leftIndent=10, firstLineIndent=-10, spaceAfter=7),
    }.items():
        styles[name] = ParagraphStyle(name, parent=styles['body'], **changes)
    return styles


def section_heading(node, styles):
    return [Paragraph(html.escape(text_of(node).strip().upper()), styles['h2']),
            HRFlowable(width='100%', thickness=0.55, color=colors.HexColor(RULE), spaceAfter=4)]


def paper_flowables(article, styles):
    title = article.find_all(cls='publication-title')[0]
    authors = article.find_all(cls='publication-authors')[0]
    venue = article.find_all(cls='publication-venue')[0]
    included = {a.attrs.get('href') for a in title.find_all('a')}
    actions = []
    for group in article.find_all(cls='publication-links'):
        for a in group.find_all('a'):
            href = a.attrs.get('href')
            if href and href not in included and not omit(a):
                actions.append(markup(a))
                included.add(href)
    venue_markup = markup(venue).strip()
    if actions:
        venue_markup += '  |  ' + '  |  '.join(actions)
    return KeepTogether([
        Paragraph(markup(title).strip(), styles['pubtitle']),
        Paragraph(markup(authors).strip(), styles['authors']),
        Paragraph(venue_markup, styles['venue']),
        Spacer(1, 13),
    ])


def split_sections(article):
    intro, sections = [], []
    for node in article.children:
        if not isinstance(node, Node) or omit(node):
            continue
        if node.tag == 'h2':
            sections.append((node, []))
        elif sections:
            sections[-1][1].append(node)
        else:
            intro.append(node)
    return intro, sections


def regular_section(heading, content, styles):
    flow = section_heading(heading, styles)
    section_id = heading.attrs.get('id')
    previous_tag = None
    for node in content:
        if node.tag == 'h3':
            flow.append(Paragraph(markup(node).strip(), styles['h3']))
        elif node.tag == 'p':
            key = 'meta' if previous_tag == 'h3' else 'body'
            flow.append(Paragraph(markup(node).strip(), styles[key]))
        elif node.tag in {'ul', 'ol'}:
            for item in (c for c in node.children if isinstance(c, Node) and c.tag == 'li'):
                style = styles['talk'] if section_id == 'talks' else styles['bullet']
                flow.append(Paragraph('&#8226;  ' + markup(item).strip(), style))
        previous_tag = node.tag
    return flow


class CVDocument(BaseDocTemplate):
    def __init__(self, path, name):
        super().__init__(path, pagesize=letter, leftMargin=49, rightMargin=49,
                         topMargin=42, bottomMargin=40, title=f'{name} - Curriculum vitae',
                         author=name, subject='Academic curriculum vitae',
                         creator='David Jin CV generator (ReportLab)', pageCompression=1)
        self.person_name = name
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(PageTemplate(id='cv', frames=[frame], onPage=self.decorate))

    def decorate(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(colors.HexColor(MUTED))
        canvas.setFont('CVSans', 8)
        if doc.page > 1:
            canvas.drawString(self.leftMargin, letter[1] - 26, self.person_name)
            canvas.drawRightString(letter[0] - self.rightMargin, letter[1] - 26, 'Curriculum vitae')
        canvas.setStrokeColor(colors.HexColor(RULE))
        canvas.setLineWidth(0.45)
        canvas.line(self.leftMargin, 29, letter[0] - self.rightMargin, 29)
        canvas.drawString(self.leftMargin, 17, self.person_name)
        canvas.drawRightString(letter[0] - self.rightMargin, 17, str(doc.page))
        canvas.restoreState()


def build(source, destination):
    parser = TreeParser()
    parser.feed(Path(source).read_text(encoding='utf-8'))
    articles = parser.root.find_all('article', 'cv-content')
    if len(articles) != 1:
        raise ValueError('Expected one article.cv-content in the rendered HTML')
    article = articles[0]
    intro, sections = split_sections(article)
    # Fail closed if the current source accidentally restores either removed field.
    current_text = text_of(article)
    if re.search(r'\bResearch experience\b', current_text, re.I):
        raise ValueError('CV source unexpectedly contains Research experience')
    if re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', current_text):
        raise ValueError('CV source unexpectedly contains an email address')
    contact = next(n for n in intro if n.tag == 'p')
    name = text_of(contact.find_all('strong')[0]).strip()
    register_fonts()
    styles = make_styles()
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    doc = CVDocument(str(destination), name)
    flow = []
    title_row = Table([[Paragraph(html.escape(name), styles['name']),
                        Paragraph('CURRICULUM VITAE', styles['label'])]], colWidths=[doc.width * 0.65, doc.width * 0.35])
    title_row.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
                                   ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                                   ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 5)]))
    flow.append(title_row)
    contact_links = [markup(a) for a in contact.find_all('a') if not omit(a)]
    flow.append(Paragraph('  ·  '.join(contact_links), styles['contact']))
    for node in intro:
        if node.tag == 'p' and node is not contact:
            flow.append(Paragraph(markup(node), styles['contact']))
    flow.append(Spacer(1, 3))
    for heading, content in sections:
        section_id = heading.attrs.get('id')
        if section_id in {'publications', 'talks'}:
            flow.append(PageBreak())
        if section_id == 'publications':
            flow.extend(section_heading(heading, styles))
            for node in content:
                if node.tag == 'h3':
                    flow.append(Paragraph(markup(node).strip(), styles['subhead']))
                elif node.tag == 'ol':
                    for paper in node.find_all('article'):
                        flow.append(paper_flowables(paper, styles))
        else:
            flow.extend(regular_section(heading, content, styles))
    doc.build(flow)
    print(f'Created {destination}')


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('input_rendered_cv_html')
    cli.add_argument('output_pdf')
    args = cli.parse_args()
    build(args.input_rendered_cv_html, args.output_pdf)
