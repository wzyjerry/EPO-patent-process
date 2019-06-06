import json

from lxml import etree


'''
lxml helper
'''
def get_attr(elem: etree.Element) -> dict:
    return dict(elem.attrib)

def get_children(parent: etree.Element, children_tag: list) -> dict:
    # TODO: Check attrib
    children = dict()
    for child in parent:
        # Comment
        if callable(child.tag):
            continue
        elif child.tag in children_tag:
            if child.tag not in children:
                children[child.tag] = child
            else:
                if isinstance(children[child.tag], list):
                    children[child.tag].append(child)
                else:
                    children[child.tag] = [children[child.tag], child]
        else:
            raise Exception('gc Warning:', child.tag, 'not resolve.')
    return children

def get_children_group(parent: etree.Element, group: dict) -> dict:
    # TODO: (B561,B563?,B564*)*,(B562,B563?,B564*)*
    # TODO: Check attrib
    result = dict()
    children_group = {x:[] for x in group}
    tmp = {x:{} for x in group}
    for child in parent:
        # Comment
        if callable(child.tag):
            continue
        find = False
        # find which group the tag is belongs to
        for gid in group:
            if child.tag in group[gid]:
                find = True
                if child.tag not in tmp[gid]:
                    tmp[gid][child.tag] = child
                else:
                    # conflict, append tmp to children group
                    children_group[gid].append(tmp[gid])
                    tmp[gid] = {
                        child.tag: child
                    }
            if find:
                break
        if not find:
            raise Exception('gcg Warning:', child.tag, 'not resolve.')
    # append not empty tmp dict to children_group
    for gid in tmp:
        if len(tmp[gid]) > 0:
            children_group[gid].append(tmp[gid])
    # copy not empty dict to result
    for gid in children_group:
        if len(children_group[gid]) > 0:
            result[gid] = children_group[gid]
    return result

def get_inner_content(elem: etree.Element) -> str:
    content = etree.tostring(elem, encoding='utf-8').decode('utf-8')
    begin = content.find('>') + 1
    end = content.rfind('<')
    return content[begin: end]

'''
resolve_common
'''
def resolve_date(elem: etree.Element) -> int:
    '''
    <date>: yyyyMMdd
    '''
    return int(elem.text)

def resolve_bnum(elem: etree.Element) -> int:
    '''
    <bnum>: Issue number of the Gazette
    '''
    return int(elem.text)

def resolve_text(elem: etree.Element) -> str:
    '''
    <text>: str
    '''
    return elem.text

def resolve_sfx(elem: etree.Element) -> str:
    '''
    <sfx>: str
    '''
    return elem.text

def resolve_irf(elem: etree.Element) -> str:
    '''
    <irf>: str
    '''
    return elem.text

def resolve_iid(elem: etree.Element) -> str:
    '''
    <iid>: str
    '''
    return elem.text

def resolve_ctry(elem: etree.Element) -> str:
    '''
    <ctry>: str
    '''
    return elem.text

def resolve_city(elem: etree.Element) -> str:
    '''
    <city>: str
    '''
    return elem.text

def resolve_str(elem: etree.Element) -> str:
    '''
    <str>: str
    '''
    return elem.text

def resolve_adr(elem: etree.Element) -> dict:
    '''
    <adr>: str, city, ctry
    '''
    adr = dict()
    children = get_children(elem, ['str', 'city', 'ctry'])
    if 'str' in children:
        adr['str'] = resolve_str(children['str'])
    if 'city' in children:
        adr['city'] = resolve_city(children['city'])
    if 'ctry' in children:
        adr['ctry'] = resolve_ctry(children['ctry'])
    return adr

def resolve_snm(elem: etree.Element) -> str:
    '''
    <snm>: str
    '''
    return elem.text

def resolve_B716EP(elem: etree.Element) -> dict:
    '''
    <B716EP>: Designated states for the applicant. Used only when some of the designated states are mentioned
    '''
    B716EP = dict()
    children = get_children(elem, ['ctry'])
    B716EP['ctry'] = []
    if isinstance(children['ctry'], list):
        for ctry in children['ctry']:
            B716EP['ctry'].append(resolve_ctry(ctry))
    else:
        B716EP['ctry'].append(resolve_ctry(children['ctry']))
    return B716EP

def resolve_name(elem: etree.Element) -> dict:
    '''
    <name>: snm, sfx, iid, irf, adr
    '''
    name = dict()
    children = get_children(elem, ['snm', 'adr', 'iid', 'irf', 'sfx', 'B716EP'])
    if 'snm' in children:
        name['snm'] = resolve_snm(children['snm'])
    if 'sfx' in children:
        name['sfx'] = resolve_irf(children['sfx'])
    if 'iid' in children:
        name['iid'] = resolve_iid(children['iid'])
    if 'irf' in children:
        name['irf'] = resolve_irf(children['irf'])
    if 'adr' in children:
        name['adr'] = resolve_adr(children['adr'])
    if 'B716EP' in children:
        name['B716EP'] = resolve_B716EP(children['B716EP'])
    return name

def resolve_pnum(elem: etree.Element) -> str:
    '''
    <pnum>: PCT Publication number
    '''
    return elem.text

def resolve_anum(elem: etree.Element) -> str:
    '''
    <anum>: PCT Application number
    '''
    return elem.text

def resolve_dnum(elem: etree.Element) -> dict:
    '''
    <dnum>: Components of a doc and extdoc (doc, extdoc). Document number
    '''
    dnum = dict()
    children = get_children(elem, ['anum', 'pnum'])
    if 'anum' in children:
        dnum['anum'] = resolve_anum(children['anum'])
    if 'pnum' in children:
        dnum['pnum'] = resolve_pnum(children['pnum'])
    return dnum

def resolve_heading(elem: etree.Element) -> dict:
    '''
    <heading>: headings
    '''
    heading = dict()
    heading['attr'] = get_attr(elem)
    heading['content'] = get_inner_content(elem)
    return heading

'''
resolve_list
'''
def resolve_B871(elem: etree.Element) -> dict:
    B871 = dict()
    children = get_children(elem, ['dnum', 'date', 'bnum'])
    if 'dnum' in children:
        B871['dnum'] = resolve_dnum(children['dnum'])
    if 'date' in children:
        B871['date'] = resolve_date(children['date'])
    if 'bnum' in children:
        B871['bnum'] = resolve_bnum(children['bnum'])
    return B871

def resolve_B870(elem: etree.Element) -> dict:
    '''
    <B870>: PCT publication data
    '''
    B870 = dict()
    children = get_children(elem, ['B871'])
    B870['B871'] = resolve_B871(children['B871'])
    return B870

def resolve_B862(elem: etree.Element) -> str:
    '''
    <B862>: Filing language (ISO 639)
    '''
    return elem.text

def resolve_B861(elem: etree.Element) -> dict:
    '''
    <B861>: Document identification
    '''
    B861 = dict()
    children = get_children(elem, ['dnum', 'date'])
    if 'dnum' in children:
        B861['dnum'] = resolve_dnum(children['dnum'])
    if 'date' in children:
        B861['date'] = resolve_date(children['date'])
    return B861

def resolve_B860(elem: etree.Element) -> dict:
    '''
    <B860>: PCT application data
    '''
    B860 = dict()
    children = get_children(elem, ['B861', 'B862'])
    B860['B861'] = resolve_B861(children['B861'])
    if 'B862' in children:
        B860['B862'] = resolve_B862(children['B862'])
    return B860

def resolve_B849EP(elem: etree.Element) -> dict:
    '''
    <B849EP>: Extended state data
    '''
    B849EP = dict()
    children = get_children(elem, ['ctry', 'date'])
    B849EP['ctry'] = resolve_ctry(children['ctry'])
    if 'date' in children:
        B849EP['date'] = resolve_date(children['date'])
    return B849EP

def resolve_B848EP(elem: etree.Element)-> dict:
    '''
    <B848EP>: States to which the patent is validated
    '''
    B848EP = dict()
    children = get_children(elem, ['B849EP'])
    B848EP['B849EP'] = []
    if isinstance(children['B849EP'], list):
        for B849EP in children['B849EP']:
            B848EP['B849EP'].append(resolve_B849EP(B849EP))
    else:
        B848EP['B849EP'].append(resolve_B849EP(children['B849EP']))
    return B848EP

def resolve_B845EP(elem: etree.Element) -> dict:
    '''
    <B845EP>: Extended state data
    '''
    B845EP = dict()
    children = get_children(elem, ['ctry', 'date'])
    B845EP['ctry'] = resolve_ctry(children['ctry'])
    if 'date' in children:
        B845EP['date'] = resolve_date(children['date'])
    return B845EP

def resolve_B844EP(elem: etree.Element)-> dict:
    '''
    <B844EP>: States to which the application/patent is extended
    '''
    B844EP = dict()
    children = get_children(elem, ['B845EP'])
    B844EP['B845EP'] = []
    if isinstance(children['B845EP'], list):
        for B845EP in children['B845EP']:
            B844EP['B845EP'].append(resolve_B845EP(B845EP))
    else:
        B844EP['B845EP'].append(resolve_B845EP(children['B845EP']))
    return B844EP

def resolve_B840(elem: etree.Element) -> list:
    '''
    <B840>: Designated contracting states
    '''
    B840 = list()
    children = get_children(elem, ['ctry'])
    if isinstance(children['ctry'], list):
        for ctry in children['ctry']:
            B840.append(resolve_ctry(ctry))
    else:
        B840.append(resolve_ctry(children['ctry']))
    return B840

def resolve_B831(elem: etree.Element) -> str:
    '''
    <B831>: EPO Declaration statement
    '''
    return elem.text

def resolve_B830(elem: etree.Element) -> dict:
    '''
    <B830>: Information concerning deposit of micro-organisms
    '''
    B830 = dict()
    children = get_children(elem, ['B831'])
    B830['B831'] = resolve_B831(children['B831'])
    return B830

def resolve_B800(elem: etree.Element) -> dict:
    '''
    <B800>: International Convention Data
    '''
    B800 = dict()
    children = get_children(elem, ['B830', 'B840', 'B844EP', 'B848EP', 'B860', 'B870'])
    if 'B830' in children:
        B800['B830'] = resolve_B830(children['B830'])
    if 'B840' in children:
        B800['B840'] = resolve_B840(children['B840'])
    if 'B844EP' in children:
        B800['B844EP'] = resolve_B844EP(children['B844EP'])
    if 'B848EP' in children:
        B800['B848EP'] = resolve_B848EP(children['B848EP'])
    if 'B860' in children:
        B800['B860'] = resolve_B860(children['B860'])
    if 'B870' in children:
        B800['B870'] = resolve_B870(children['B870'])
    return B800

def resolve_B740(elem: etree.Element) -> list:
    '''
    <B740>: Attorney/agent of the applicant(s)
    '''
    B740 = list()
    children = get_children(elem, ['B741'])
    if isinstance(children['B741'], list):
        for agent in children['B741']:
            B740.append(resolve_name(agent))
    else:
        B740.append(resolve_name(children['B741']))
    return B740

def resolve_B730(elem: etree.Element) -> list:
    '''
    <B730>: Grantees
    '''
    B730 = list()
    children = get_children(elem, ['B731'])
    if isinstance(children['B731'], list):
        for grantee in children['B731']:
            B730.append(resolve_name(grantee))
    else:
        B730.append(resolve_name(children['B731']))
    return B730

def resolve_B720(elem: etree.Element) -> list:
    '''
    <B720>: Inventors
    '''
    B720 = list()
    children = get_children(elem, ['B721'])
    if isinstance(children['B721'], list):
        for inventor in children['B721']:
            B720.append(resolve_name(inventor))
    else:
        B720.append(resolve_name(children['B721']))
    return B720

def resolve_B710(elem: etree.Element) -> list:
    '''
    <B710>: Applicants
    '''
    B710 = list()
    children = get_children(elem, ['B711'])
    if isinstance(children['B711'], list):
        for applicant in children['B711']:
            B710.append(resolve_name(applicant))
    else:
        B710.append(resolve_name(children['B711']))
    return B710

def resolve_B700(elem: etree.Element) -> dict:
    '''
    <B700>: Parties concerned with the document
    '''
    B700 = dict()
    children = get_children(elem, ['B710', 'B720', 'B730', 'B740'])
    if 'B710' in children:
        B700['B710'] = resolve_B710(children['B710'])
    if 'B720' in children:
        B700['B720'] = resolve_B720(children['B720'])
    if 'B730' in children:
        B700['B730'] = resolve_B730(children['B730'])
    if 'B740' in children:
        B700['B740'] = resolve_B740(children['B740'])
    return B700

def resolve_cdoc(elem: etree.Element) -> list:
    '''
    <cdoc>: divisional application data
    '''
    cdoc = list()
    children_group = get_children_group(elem, {
        'g': ['dnum', 'date']
    })
    for g in children_group['g']:
        tmp = {}
        if 'dnum' in g:
            tmp['dnum'] = resolve_dnum(g['dnum'])
        if 'date' in g:
            tmp['date'] = resolve_date(g['date'])
        cdoc.append(tmp)
    return cdoc

def resolve_parent(elem: etree.Element) -> dict:
    '''
    <parent>: Parent relation
    '''
    parent = dict()
    children = get_children(elem, ['cdoc'])
    if 'cdoc' in children:
        parent['cdoc'] = []
        if isinstance(children['cdoc'], list):
            for cdoc in children['cdoc']:
                parent['cdoc'].append(resolve_cdoc(cdoc))
        else:
            parent['cdoc'].append(resolve_cdoc(children['cdoc']))
    return parent

def resolve_B620EP(elem: etree.Element) -> dict:
    '''
    <B620EP>: Divisional application(s)
    '''
    B620EP = dict()
    children = get_children(elem, ['parent'])
    if 'parent' in B620EP:
        B620EP['parent'] = resolve_parent(children['parent'])
    return B620EP

def resolve_B600(elem: etree.Element) -> list:
    '''
    <B600>: References to other legally or procedurally related domestic patent documents
    '''
    B600 = list()
    for child in elem:
        # Comment
        if callable(child.tag):
            continue
        if child.tag == 'B620EP':
            B600.append({
                'type': 'B620EP',
                'content': resolve_B620EP(child)
            })
    return B600

def resolve_B598(elem: etree.Element) -> str:
    '''
    <B598>: Figure number on first (title) page
    '''
    return elem.text

def resolve_B590(elem: etree.Element) -> dict:
    '''
    <B590>: Spec. & drawings
    '''
    B590 = dict()
    children = get_children(elem, ['B598'])
    if 'B598' in B590:
        B590['B598'] = resolve_B598(children['B598'])
    return B590

def resolve_B565EP(elem: etree.Element) -> dict:
    '''
    <B565EP>: Date of drawing up and despatch of supplementary search report
    '''
    B565EP = dict()
    children = get_children(elem, ['date'])
    B565EP['date'] = resolve_date(children['date'])
    return B565EP

def resolve_B562(elem: etree.Element) -> dict:
    '''
    <B562>: Non patent citation
    '''
    B562 = dict()
    children = get_children(elem, ['text'])
    if 'text' in children:
        B562['text'] = resolve_text(children['text'])
    return B562

def resolve_B561(elem: etree.Element) -> dict:
    '''
    <B561>: Patent citation
    '''
    B561 = dict()
    children = get_children(elem, ['text'])
    if 'text' in children:
        B561['text'] = resolve_text(children['text'])
    return B561

def resolve_B560(elem: etree.Element) -> dict:
    '''
    <B560>: List of prior art documents
    '''
    B560 = dict()
    children = get_children(elem, ['B561', 'B562', 'B565EP'])
    if 'B561' in children:
        B560['B561'] = []
        if isinstance(children['B561'], list):
            for B561 in children['B561']:
                B560['B561'].append(resolve_B561(B561))
        else:
            B560['B561'].append(resolve_B561(children['B561']))
    if 'B562' in children:
        B560['B562'] = []
        if isinstance(children['B562'], list):
            for B562 in children['B562']:
                B560['B562'].append(resolve_B562(B562))
        else:
            B560['B562'].append(resolve_B562(children['B562']))
    if 'B565EP' in children:
        B560['B565EP'] = resolve_B565EP(children['B565EP'])
    return B560

def resolve_B542(elem: etree.Element) -> str:
    '''
    <B542>: Title of invention
    '''
    return elem.text

def resolve_B541(elem: etree.Element) -> str:
    '''
    <B541>: Lang. of title (ISO 639)
    '''
    return elem.text

def resolve_B540(elem: etree.Element) -> list:
    '''
    <B540>: Title
    '''
    B540 = list()
    children_group = get_children_group(elem, {
        'title': ['B541', 'B542']
    })
    for item in children_group['title']:
        tmp = {}
        if 'B541' in item:
            tmp['B541'] = resolve_B541(item['B541'])
        tmp['B542'] = resolve_B542(item['B542'])
        B540.append(tmp)
    return B540

def resolve_classification_ipcr(elem: etree.Element) -> dict:
    '''
    <classification_ipcr>: <text>50d</text>
    '''
    classification_ipcr = dict()
    classification_ipcr['attr'] = get_attr(elem)
    children = get_children(elem, ['text'])
    if 'text' in children:
        classification_ipcr['text'] = resolve_text(children['text'])
    return classification_ipcr

def resolve_B510EP(elem: etree.Element) -> list:
    '''
    <B510EP>: International Patent Classification (IPCR – in force 01-2006)
    '''
    B510EP = list()
    children = get_children(elem, ['classification-ipcr'])
    if isinstance(children['classification-ipcr'], list):
        for ipcr in children['classification-ipcr']:
            B510EP.append(resolve_classification_ipcr(ipcr))
    else:
        B510EP.append(resolve_classification_ipcr(children['classification-ipcr']))
    return B510EP

def resolve_B500(elem: etree.Element) -> dict:
    '''
    <B500>: Technical Data
    '''
    B500 = dict()
    children = get_children(elem, ['B510EP', 'B540', 'B560', 'B590'])
    if 'B510EP' in children:
        B500['B510EP'] = resolve_B510EP(children['B510EP'])
    if 'B540' in children:
        B500['B540'] = resolve_B540(children['B540'])
    if 'B560' in children:
        B500['B560'] = resolve_B560(children['B560'])
    if 'B590' in children:
        B500['B590'] = resolve_B590(children['B590'])
    return B500

def resolve_B452EP(elem: etree.Element) -> dict:
    '''
    <B452EP>: Date of announcement of intention to grant (after 01.07.2002)
    '''
    B452EP = dict()
    children = get_children(elem, ['date'])
    B452EP['date'] = resolve_date(children['date'])
    return B452EP

def resolve_B450(elem: etree.Element) -> dict:
    '''
    [root]<B450>: Document with grant (second publication)
    '''
    B450 = dict()
    children = get_children(elem, ['date', 'bnum'])
    B450['date'] = resolve_date(children['date'])
    B450['bnum'] = resolve_bnum(children['bnum'])
    return B450

def resolve_B430(elem: etree.Element) -> dict:
    '''
    [root]<B430>: Unexamined document without grant (first publication)
    '''
    B430 = dict()
    children = get_children(elem, ['date', 'bnum'])
    B430['date'] = resolve_date(children['date'])
    B430['bnum'] = resolve_bnum(children['bnum'])
    return B430

def resolve_B405(elem: etree.Element) -> dict:
    '''
    <B405>: Patent Bulletin / Gazette information
    '''
    B405 = dict()
    children = get_children(elem, ['date', 'bnum'])
    B405['date'] = resolve_date(children['date'])
    B405['bnum'] = resolve_bnum(children['bnum'])
    return B405

def resolve_B400(elem: etree.Element) -> dict:
    B400 = dict()
    children = get_children(elem, ['B405', 'B430', 'B450', 'B452EP'])
    if 'B405' in children:
        B400['B405'] = resolve_B405(children['B405'])
    if 'B430' in children:
        B400['B430'] = resolve_B430(children['B430'])
    if 'B450' in children:
        B400['B450'] = resolve_B450(children['B450'])
    if 'B452EP' in children:
        B400['B452EP'] = resolve_B452EP(children['B452EP'])
    return B400
    
def resolve_B330(elem: etree.Element) -> dict:
    '''
    <B330>: Country in which the priority application was filed
    '''
    B330 = dict()
    children = get_children(elem, ['ctry'])
    B330['ctry'] = resolve_ctry(children['ctry'])
    return B330

def resolve_B320(elem: etree.Element) -> dict:
    '''
    <B320>: Priority date
    '''
    B320 = dict()
    children = get_children(elem, ['date'])
    B320['date'] = resolve_date(children['date'])
    return B320

def resolve_B310(elem: etree.Element) -> str:
    '''
    <B310>: Priority number
    '''
    return elem.text

def resolve_B300(elem: etree.Element) -> dict:
    '''
    <B300>:
        (<B310>, <B320>, <B330>)*: Priority data
    '''
    B300 = dict()
    children_group = get_children_group(elem, {
        'priority': ['B310', 'B320', 'B330']
    })
    if 'priority' in children_group:
        B300['priority'] = []
        for item in children_group['priority']:
            tmp = {}
            if 'B310' in item:
                tmp['B310'] = resolve_B310(item['B310'])
            if 'B320' in item:
                tmp['B320'] = resolve_B320(item['B320'])
            if 'B330' in item:
                tmp['B330'] = resolve_B330(item['B330'])
            B300['priority'].append(tmp)
    return B300

def resolve_B260(elem: etree.Element) -> str:
    '''
    [root]<B260>: Publication language
    '''
    return elem.text

def resolve_B251EP(elem: etree.Element) -> str:
    '''
    <B251EP>: Procedure language
    '''
    return elem.text

def resolve_B250(elem: etree.Element) -> str:
    '''
    <B250>: Filing language
    '''
    return elem.text

def resolve_B242(elem: etree.Element) -> dict:
    '''
    <B242>: Date of despatch of the first examination report
    '''
    B242 = dict()
    children = get_children(elem, ['date'])
    B242['date'] = resolve_date(children['date'])
    return B242

def resolve_B241(elem: etree.Element) -> dict:
    '''
    <B241>: Date of request for examination
    '''
    B241 = dict()
    children = get_children(elem, ['date'])
    B241['date'] = resolve_date(children['date'])
    return B241

def resolve_B240(elem: etree.Element) -> dict:
    '''
    <B240>: Dates from which industrial property rights may have effect
    '''
    B240 = dict()
    children = get_children(elem, ['B241', 'B242'])
    if 'B241' in children:
        B240['B241'] = resolve_B241(children['B241'])
    if 'B242' in children:
        B240['B242'] = resolve_B242(children['B242'])
    return B240

def resolve_B220(elem: etree.Element) -> dict:
    '''
    <B220>: Application filing date
    '''
    B220 = dict()
    children = get_children(elem, ['date'])
    B220['date'] = resolve_date(children['date'])
    return B220

def resolve_B210(elem: etree.Element) -> str:
    '''
    [root]<B210>: Application number
    '''
    return elem.text

def resolve_B200(elem: etree.Element) -> dict:
    '''
    <B200>: Domestic filing data
    '''
    B200 = dict()
    children = get_children(elem, ['B210', 'B220', 'B240', 'B250', 'B251EP', 'B260'])
    B200['B210'] = resolve_B210(children['B210'])
    B200['B220'] = resolve_B220(children['B220'])
    if 'B240' in children:
        B200['B240'] = resolve_B240(children['B240'])
    if 'B250' in children:
        B200['B250'] = resolve_B250(children['B250'])
    if 'B251EP' in children:
        B200['B251EP'] = resolve_B251EP(children['B251EP'])
    if 'B260' in children:
        B200['B260'] = resolve_B260(children['B260'])    
    return B200

def resolve_B190(elem: etree.Element) -> str:
    '''
    <B190>: Publishing country or organisation
    '''
    return elem.text

def resolve_B140(elem: etree.Element) -> dict:
    '''
    <B140>: Date of publication
    '''
    B140 = dict()
    children = get_children(elem, ['date'])
    B140['date'] = resolve_date(children['date'])
    return B140

def resolve_B130(elem: etree.Element) -> str:
    '''
    <B130>: Kind of document
    '''
    return elem.text

def resolve_B121EP(elem: etree.Element) -> str:
    '''
    <B121>: Any Descriptive text for B121 (EPO)
    '''
    return elem.text

def resolve_B121(elem: etree.Element) -> str:
    '''
    <B121>: Plain language designation of the kind of document
    '''
    return elem.text

def resolve_B120(elem: etree.Element) -> dict:
    '''
    <B120>: Plain language designation
    '''
    B120 = dict()
    children = get_children(elem, ['B121', 'B121EP'])
    B120['B121'] = resolve_B121(children['B121'])
    if 'B121EP' in children:
        B120['B121EP'] = resolve_B121EP(children['B121EP'])
    return B120

def resolve_B110(elem: etree.Element) -> str:
    '''
    <B110>: Publication number of the document (EPO or WIPO)
    '''
    return elem.text

def resolve_B100(elem: etree.Element) -> dict:
    '''
    <B100>: Document identification
    '''
    B100 = dict()
    children = get_children(elem, ['B110', 'B120', 'B130', 'B140', 'B190'])
    B100['B110'] = resolve_B110(children['B110'])
    if 'B120' in children:
        B100['B120'] = resolve_B120(children['B120'])
    B100['B130'] = resolve_B110(children['B130'])
    B100['B140'] = resolve_B140(children['B140'])
    B100['B190'] = resolve_B190(children['B190'])
    return B100

def resolve_B001EP(elem: etree.Element) -> str:
    '''
    <B001EP>: Selective mask for states involved
    '''
    return elem.text

def resolve_B003EP(elem: etree.Element) -> str:
    '''
    <B003EP>: Indicator 'no A-document published by EPO'
    '''
    return elem.text

def resolve_B005EP(elem: etree.Element) -> str:
    '''
    [useless]<B005EP>: Printer/Producer identification
    '''
    return elem.text

def resolve_B007EP(elem: etree.Element) -> str:
    '''
    [useless]<B007EP>: Reserved for EPO internal use
    '''
    return elem.text

def resolve_B053EP(elem: etree.Element) -> dict:
    '''
    <B053EP>: Additional remarks
    '''
    return elem.text

def resolve_B051EP(elem: etree.Element) -> str:
    '''
    <B051EP>: Language
    '''
    return elem.text

def resolve_B052EP(elem: etree.Element) -> str:
    '''
    <B052EP>: Free Text
    '''
    return elem.text

def resolve_B050EP(elem: etree.Element) -> list:
    '''
    <B050EP>: Free text
    '''
    B050EP = list()
    children_group = get_children_group(elem, {
        'text': ['B051EP', 'B052EP']
    })
    for text in children_group['text']:
        B050EP.append({
            'B051EP': resolve_B051EP(text['B051EP']),
            'B052EP': resolve_B052EP(text['B052EP'])
        })
    return B050EP

def resolve_eptags(elem: etree.Element) -> dict:
    '''
    <eptags>: EPO specific tags
    '''
    eptags = dict()
    children = get_children(elem, ['B001EP', 'B003EP', 'B005EP', 'B007EP', 'B050EP', 'B053EP'])
    if 'B001EP' in children:
        eptags['B001EP'] = resolve_B001EP(children['B001EP'])
    if 'B003EP' in children:
        eptags['B003EP'] = resolve_B003EP(children['B003EP'])
    if 'B005EP' in children:
        eptags['B005EP'] = resolve_B003EP(children['B005EP'])
    if 'B007EP' in children:
        eptags['B007EP'] = resolve_B003EP(children['B007EP'])
    if 'B050EP' in children:
        eptags['B050EP'] = resolve_B050EP(children['B050EP'])
    if 'B053EP' in children:
        eptags['B053EP'] = []
        if isinstance(children['B053EP'], list):
            for B053EP in children['B053EP']:
                eptags['B053EP'].append(resolve_B053EP(B053EP))
        else:
            eptags['B053EP'].append(resolve_B053EP(children['B053EP']))
    return eptags

def resolve_B000(elem: etree.Element) -> dict:
    '''
    <B000>: Office specific system/file information
    '''
    B000 = dict()
    children = get_children(elem, ['eptags'])
    if 'eptags' in children:
        B000['eptags'] = resolve_eptags(children['eptags'])
    return B000

def resolve_SDOBI(elem: etree.Element) -> dict:
    '''
    <SDOBI>: Sub-DOcument for BIbliographic data
    '''
    SDOBI = dict()
    SDOBI['attr'] = get_attr(elem)
    children = get_children(elem, ['B000', 'B100', 'B200', 'B300', 'B400', 'B500', 'B600', 'B700', 'B800'])
    if 'B000' in children:
        SDOBI['B000'] = resolve_B000(children['B000'])
    SDOBI['B100'] = resolve_B100(children['B100'])
    if 'B200' in children:
        SDOBI['B200'] = resolve_B200(children['B200'])
    if 'B300' in children:
        SDOBI['B300'] = resolve_B300(children['B300'])
    if 'B400' in children:
        SDOBI['B400'] = resolve_B400(children['B400'])
    if 'B500' in children:
        SDOBI['B500'] = resolve_B500(children['B500'])
    if 'B600' in children:
        SDOBI['B600'] = resolve_B600(children['B600'])
    if 'B700' in children:
        SDOBI['B700'] = resolve_B700(children['B700'])
    if 'B800' in children:
        SDOBI['B800'] = resolve_B800(children['B800'])
    return SDOBI

def resolve_abstract(elem: etree.Element) -> dict:
    abstract = dict()
    abstract['attr'] = get_attr(elem)
    content = []
    for child in elem:
        # Comment
        if callable(child.tag):
            continue
        content.append({
            'type': child.tag,
            'attr': get_attr(child),
            'content': get_inner_content(child)
        })
    abstract['content'] = content
    return abstract

def resolve_description(elem: etree.Element) -> dict:
    description = dict()
    description['attr'] = get_attr(elem)
    content = []
    for child in elem:
        # Comment
        if callable(child.tag):
            continue
        if child.tag in ['heading', 'p']:
            content.append({
                'type': child.tag,
                'attr': get_attr(child),
                'content': get_inner_content(child)
            })
        else:
            raise Exception('desc Warning:', child.tag, 'not resolve.')
    
    description['content'] = content
    return description

def resolve_claim_text(elem: etree.Element) -> str:
    return get_inner_content(elem)

def resolve_claim(elem: etree.Element) -> dict:
    claim = dict()
    claim['attr'] = get_attr(elem)
    children = get_children(elem, ['claim-text'])
    claim['claim_text'] = []
    if isinstance(children['claim-text'], list):
        for claim_text in children['claim-text']:
            claim['claim_text'].append(resolve_claim_text(claim_text))
    else:
        claim['claim_text'].append(resolve_claim_text(children['claim-text']))
    return claim

def resolve_claims(elem: etree.Element) -> dict:
    claims = dict()
    claims['attr'] = get_attr(elem)
    children = get_children(elem, ['claim'])
    claims['claim'] = []
    if isinstance(children['claim'], list):
        for claim in children['claim']:
            claims['claim'].append(resolve_claim(claim))
    else:
        claims['claim'].append(resolve_claim(children['claim']))
    return claims

def resolve_amended_claims(elem: etree.Element) -> dict:
    amended_claims = dict()
    amended_claims['attr'] = get_attr(elem)
    children = get_children(elem, ['heading', 'claim'])
    if 'heading' in children:
        amended_claims['heading'] = resolve_heading(children['heading'])
    amended_claims['claim'] = []
    if isinstance(children['claim'], list):
        for claim in children['claim']:
            amended_claims['claim'].append(resolve_claim(claim))
    else:
        amended_claims['claim'].append(resolve_claim(children['claim']))
    return amended_claims

def resolve_img(elem: etree) -> dict:
    return {
        'attr': get_attr(elem)
    }

def resolve_figure(elem: etree) -> dict:
    figure = dict()
    figure['attr'] = get_attr(elem)
    children = get_children(elem, ['img'])
    figure['img'] = resolve_img(children['img'])
    return figure

def resolve_drawings(elem: etree.Element) -> dict:
    drawings = dict()
    drawings['attr'] = get_attr(elem)
    children = get_children(elem, ['figure'])
    drawings['figure'] = []
    if isinstance(children['figure'], list):
        for figure in children['figure']:
            drawings['figure'].append(resolve_figure(figure))
    else:
        drawings['figure'].append(resolve_figure(children['figure']))
    return drawings

def resolve_doc_page(elem: etree.Element) -> dict:
    return {
        'attr': get_attr(elem)
    }

def resolve_search_report_data(elem: etree.Element) -> dict:
    search_report_data = dict()
    search_report_data['attr'] = get_attr(elem)
    children = get_children(elem, ['doc-page', 'srep-info', 'srep-for-pub'])
    if 'doc-page' in children:
        search_report_data['doc-page'] = []
        if isinstance(children['doc-page'], list):
            for doc_page in children['doc-page']:
                search_report_data['doc-page'].append(resolve_doc_page(doc_page))
        else:
            search_report_data['doc-page'].append(resolve_doc_page(children['doc-page']))
    else:
        search_report_data['raw'] = get_inner_content(elem)
    return search_report_data

def resolve_ep_reference_list(elem: etree.Element) -> dict:
    ep_reference_list = dict()
    ep_reference_list['attr'] = get_attr(elem)
    content = []
    for child in elem:
        # Comment
        if callable(child.tag):
            continue
        content.append({
            'type': child.tag,
            'attr': get_attr(child),
            'content': get_inner_content(child)
        })
    ep_reference_list['content'] = content
    return ep_reference_list

'''
main
'''
def parse_v1_5(xml: bytes) -> dict:
    patent = dict()
    root = etree.XML(xml)
    patent['attr'] = get_attr(root)
    children = get_children(root, [
        'SDOBI',
        'abstract',
        'description',
        'claims',
        'amended-claims',
        'drawings',
        'search-report-data',
        'ep-reference-list'
    ])
    patent['SDOBI'] = resolve_SDOBI(children['SDOBI'])
    if 'abstract' in children:
        patent['abstract'] = []
        if isinstance(children, list):
            for abstract in children['abstract']:
                patent['abstract'].append(resolve_abstract(abstract))
        else:
            patent['abstract'].append(resolve_abstract(children['abstract']))
    if 'description' in children:
        patent['description'] = resolve_description(children['description'])
    if 'claims' in children:
        patent['claims'] = []
        if isinstance(children['claims'], list):
            for claims in children['claims']:
                patent['claims'].append(resolve_claims(claims))
        else:
            patent['claims'].append(resolve_claims(children['claims']))
    if 'amended-claims' in children:
        patent['amended-claims'] = []
        if isinstance(children['amended-claims'], list):
            for amended_claims in children['amended-claims']:
                patent['amended-claims'].append(resolve_amended_claims(amended_claims))
        else:
            patent['amended-claims'].append(resolve_amended_claims(children['amended-claims']))
    if 'drawings' in children:
        patent['drawings'] = resolve_drawings(children['drawings'])
    if 'search-report-data' in children:
        patent['search-report-data'] = []
        if isinstance(children['search-report-data'], list):
            for search_report_data in children['search-report-data']:
                patent['search-report-data'].append(resolve_search_report_data(search_report_data))
        else:
            patent['search-report-data'].append(resolve_search_report_data(children['search-report-data']))    
    if 'ep-reference-list' in children:
        patent['ep-reference-list'] = resolve_ep_reference_list(children['ep-reference-list'])
    return patent

def generate_md(patent: str) -> str:
    def trans_date(field: dict) -> str:
        text = str(field['date'])
        return '%s.%s.%s' % (text[6:], text[4:6], text[:4])

    def trans_4xx(field: dict) -> str:
        text = str(field['bnum'])
        return '%s Bulletin %s/%s' % (trans_date(field), text[:4], text[4:])
    
    def trans_ipcr(field: dict) -> str:
        text = field['text'].split()
        return '%s %s <sup>(%s.%s)</sup>' % (text[0], text[1], text[2][:4], text[2][4:6])

    def trans_name(field: dict, out_str: bool) -> str:
        adr = field['adr']
        if 'sfx' in field:
            sfx = field['sfx']
        else:
            sfx = ''
        snm = field['snm'] + sfx
        if out_str:
            return '%s<br>%s<br>%s (%s)' % (snm, adr['str'], adr['city'], adr['ctry'])
        else:
            return '%s<br>%s (%s)' % (snm, adr['city'], adr['ctry'])

    def trans_international_an(field: dict) -> str:
        anum = field['B861']['dnum']['anum']
        return 'PCT/%s/%s' % (anum[:6], anum[6:])

    def trans_international_pn(field: dict) -> str:
        B871 = field['B871']
        pnum = B871['dnum']['pnum']
        bnum = str(B871['bnum'])
        return '%s %s/%s (%s Gazette %s/%s)' % (pnum[:2], pnum[2:6], pnum[6:], trans_date(B871), bnum[:4], bnum[4:])
    md = []
    SDOBI = patent['SDOBI']
    B000 = SDOBI['B000']
    eptags = B000['eptags']
    B100 = SDOBI['B100']
    B200 = SDOBI['B200']
    B400 = SDOBI['B400']
    B500 = SDOBI['B500']
    B700 = SDOBI['B700']
    B800 = SDOBI['B800']
    md.append('# (11)(19) **%s %s %s**' % (B100['B190'], format(int(B100['B110']), ',').replace(',', ' '), B100['B130']))
    if 'B120' in B100:
        if 'B121EP' in B100['B120']:
            md.append('## (12) **%s**<br>%s' % (B100['B120']['B121'], B100['B120']['B121EP']))
        else:
            md.append('## (12) **%s**' % B100['B120']['B121'])
    if 'B430' in B400:
        md.append('## (43) Date of publication:<br>**%s**' % trans_4xx(B400['B430']))
    if 'B450' in B400:
        md.append('## (45) Date of publication and mention of the grant of the patent:<br>**%s**' % trans_4xx(B400['B450']))
    md.append('## (21) Application number: **%s**' % B200['B210'])
    md.append('## (22) Date of filing: **%s**' % trans_date(B200['B220']))
    md.append('## (51) Int Cl.:')
    for ipcr in B500['B510EP']:
        md.append('+ ***%s***' % trans_ipcr(ipcr))
    if 'B860' in B800:
        md.append('## (86) International application number:<br>**%s**' % (trans_international_an(B800['B860'])))
    if 'B870' in B800:
        md.append('## (87) International publication number:<br>**%s**' % (trans_international_pn(B800['B870'])))
    md.append('***')
    md.append('## (54)')
    for title in B500['B540']:
        md.append('+ **%s**' % title['B542'])
    md.append('***')
    md.append('## (84) Designated Contracting States:')
    md.append('**%s**' % ' '.join(B800['B840']))
    if 'B844EP' in B800:
        md.append('<br>Designated Extension States:<br>**%s**' % ' '.join([x['ctry'] for x in B800['B844EP']['B845EP']]))
    if 'B848EP' in B800:
        md.append('<br>Designated Validation States:<br>**%s**' % ' '.join([x['ctry'] for x in B800['B848EP']['B849EP']]))
    
    if 'B300' in SDOBI:
        B300 = SDOBI['B300']
        md.append('## (30) Priority:')
        for priority in B300['priority']:
            md.append('+ **%s %s %s**' % (trans_date(priority['B320']), priority['B330']['ctry'], priority['B310']))
    md.append('## (43) Date of publication of application: %s' % trans_4xx(B400['B430']))
    if 'B710' in B700:
        md.append('## (71) Applicant:')
        for applicant in B700['B710']:
            if 'B716EP' in applicant:
                md.append('+ **%s**<br>Designated Contracting States:<br>**%s**' % (trans_name(applicant, False), ' '.join(applicant['B716EP']['ctry'])))
            else:
                md.append('+ **%s**' % trans_name(applicant, False))
    if 'B730' in B700:
        md.append('## (73) Proprietor:')
        for grantee in B700['B730']:
            md.append('+ **%s**' % trans_name(grantee, False))
    md.append('## (72) Inventor:')
    for inventor in B700['B720']:
        md.append('+ **%s**' % trans_name(inventor, False))
    if 'B740' in B700:
        md.append('## (74) Representative:')
        for agent in B700['B740']:
            md.append('+ **%s**' % trans_name(agent, True))
    if 'B560' in B500:
        md.append('## (56) References cited:')
        for patent_citation in B500['B560']['B561']:
            md.append('1. **%s**' % patent_citation['text'])
        md.append('')
        for patent_citation in B500['B560']['B562']:
            md.append('+ **%s**' % patent_citation['text'])
    if 'B050EP' in eptags or 'B053EP' in eptags:
        md.append('<br><br><u>Remarks:</u>')
        if 'B050EP' in eptags:
            for B050EP in eptags['B050EP']:
                md.append('+ %s' % B050EP['B052EP'])
        if 'B053EP' in eptags:
            for B053EP in eptags['B053EP']:
                md.append('+ %s' % B053EP)
    md.append('***')
    if 'abstract' in patent:
        md.append('(57) ')
        abstract = patent['abstract']
        for abst in abstract:
            for content in abst['content']:
                md.append('%s<br>' % content['content'])
        md.append('***')

    if 'description' in patent:
        md.append('**Description**')
        description = patent['description']
        for content in description['content']:
            if content['type'] == 'heading':
                md.append('<br><br>%s<br><br>' % content['content'])
            elif content['type'] == 'p':
                md.append('**[%s]**&nbsp;&nbsp;%s<br>\n' % (content['attr']['num'], content['content']))
        md.append('***')
    if 'claims' in patent:
        for claims in patent['claims']:
            claims_title = 'Claims'
            if claims['attr']['lang'] == 'de':
                claims_title = 'Patentansprüche'
            elif claims['attr']['lang'] == 'fr':
                claims_title = 'Revendications'
            md.append('### **%s**<br><br>' % claims_title)
            for claim in claims['claim']:
                md.append('1. %s<br><br>' % '<br>'.join(claim['claim_text']).replace('\n', '<br>'))
        md.append('***')
    if 'amended-claims' in patent:
        amended_claims = patent['amended-claims']
        for claims in amended_claims:
            md.append('**%s**<br><br>' % claims['heading']['content'])
            for claim in claims['claim']:
                md.append('%s<br><br>' % '<br>'.join(claim['claim_text']).replace('\n', '<br>'))
        md.append('***')
    if 'ep-reference-list' in patent:
        ep_reference_list = patent['ep-reference-list']
        for content in ep_reference_list['content']:
            if content['type'] == 'heading':
                md.append('<br><br>%s<br><br>' % content['content'])
            elif content['type'] == 'p':
                md.append('%s<br>' % content['content'])
    return '\n'.join(md)

if __name__ == '__main__':
    with open('resources/EP18151178NWA1.xml', 'rb') as fin:
        xml = fin.read()
    patent = parse_v1_5(xml)
    with open('data/EP18151178NWA1.md', 'w', encoding='utf-8') as fout:
        fout.write(generate_md(patent))
    # print(json.dumps(patent, indent=4, ensure_ascii=False))
