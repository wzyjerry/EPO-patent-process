# parser version 1.0.0 2019/06/11
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
    if elem.text == None:
        return 0
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

def resolve_syn(elem: etree.Element) -> str:
    '''
    <syn>: str
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

def resolve_B718EP(elem: etree.Element) -> dict:
    '''
    <B718EP>: Effective date for transfer of rights
    '''
    B718EP = dict()
    children = get_children(elem, ['date'])
    B718EP['date'] = resolve_date(children['date'])
    return B718EP

def resolve_B725EP(elem: etree.Element) -> dict:
    B725EP = dict()
    children = get_children(elem, ['text'])
    B725EP['text'] = []
    if isinstance(children['text'], list):
        for text in children['text']:
            B725EP['text'].append(resolve_text(text))
    else:
        B725EP['text'].append(resolve_text(children['text']))
    return B725EP

def resolve_B736EP(elem: etree.Element) -> dict:
    '''
    <B716EP>: Designated states for the grantee. Used only when some of the designated states are mentioned
    '''
    B736EP = dict()
    children = get_children(elem, ['ctry'])
    B736EP['ctry'] = []
    if isinstance(children['ctry'], list):
        for ctry in children['ctry']:
            B736EP['ctry'].append(resolve_ctry(ctry))
    else:
        B736EP['ctry'].append(resolve_ctry(children['ctry']))
    return B736EP

def resolve_B738EP(elem: etree.Element) -> dict:
    '''
    <B738EP>: Effective date for transfer of rights
    '''
    B738EP = dict()
    children = get_children(elem, ['date'])
    B738EP['date'] = resolve_date(children['date'])
    return B738EP

def resolve_name(elem: etree.Element) -> dict:
    '''
    <name>: snm, adr, iid, irf, sfx, syn, B716EP, B718EP, B725EP, B736EP, B738EP
    '''
    name = dict()
    children = get_children(elem, ['snm', 'adr', 'iid', 'irf', 'sfx', 'syn', 'B716EP', 'B718EP', 'B725EP', 'B736EP', 'B738EP'])
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
    if 'syn' in children:
        name['syn'] = []
        if isinstance(children['syn'], list):
            for syn in children['syn']:
                name['syn'].append(resolve_syn(syn))
        else:
            name['syn'].append(resolve_syn(children['syn']))
    if 'B716EP' in children:
        name['B716EP'] = resolve_B716EP(children['B716EP'])
    if 'B718EP' in children:
        name['B718EP'] = resolve_B718EP(children['B718EP'])
    if 'B725EP' in children:
        name['B725EP'] = resolve_B725EP(children['B725EP'])
    if 'B736EP' in children:
        name['B736EP'] = resolve_B736EP(children['B736EP'])
    if 'B738EP' in children:
        name['B738EP'] = resolve_B738EP(children['B738EP'])
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
    children = get_children(elem, ['text', 'anum', 'pnum'])
    if 'text' in children:
        dnum['text'] = resolve_text(children['text'])
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

def resolve_kind(elem: etree.Element) -> dict:
    '''
    <kind>: Document kind code
    '''
    return elem.text

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

def resolve_pdoc(elem: etree.Element) -> list:
    '''
    <pdoc>: parent application data
    '''
    pdoc = list()
    children_group = get_children_group(elem, {
        'g': ['dnum', 'date']
    })
    for g in children_group['g']:
        tmp = {}
        if 'dnum' in g:
            tmp['dnum'] = resolve_dnum(g['dnum'])
        if 'date' in g:
            tmp['date'] = resolve_date(g['date'])
        pdoc.append(tmp)
    return pdoc

def resolve_parent(elem: etree.Element) -> dict:
    '''
    <parent>: Parent relation
    '''
    parent = dict()
    children = get_children(elem, ['cdoc', 'pdoc'])
    if 'cdoc' in children:
        parent['cdoc'] = []
        if isinstance(children['cdoc'], list):
            for cdoc in children['cdoc']:
                parent['cdoc'].append(resolve_cdoc(cdoc))
        else:
            parent['cdoc'].append(resolve_cdoc(children['cdoc']))
    if 'pdoc' in children:
        parent['pdoc'] = []
        if isinstance(children['pdoc'], list):
            for pdoc in children['pdoc']:
                parent['pdoc'].append(resolve_pdoc(pdoc))
        else:
            parent['pdoc'].append(resolve_pdoc(children['pdoc']))
    return parent

'''
resolve_list
'''
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

def resolve_claim_text(elem: etree.Element) -> str:
    return get_inner_content(elem)

def resolve_claims_statement(elem: etree.Element) -> dict:
    claims_statement = dict()
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
            raise Exception('claims statement Warning:', child.tag, 'not resolve.')
    claims_statement['content'] = content
    return claims_statement

def resolve_amended_claims_statement(elem: etree.Element) -> dict:
    amended_claims_statement = dict()
    amended_claims_statement['attr'] = get_attr(elem)
    children = get_children(elem, ['claims-statement'])
    amended_claims_statement['claims-statement'] = []
    if isinstance(children['claims-statement'], list):
        for claims_statement in children['claims-statement']:
            amended_claims_statement['claims-statement'].append(resolve_claims_statement(claims_statement))
    else:
        amended_claims_statement['claims-statement'].append(resolve_claims_statement(children['claims-statement']))
    return amended_claims_statement

def resolve_amended_claims(elem: etree.Element) -> dict:
    amended_claims = dict()
    amended_claims['attr'] = get_attr(elem)
    children = get_children(elem, ['heading', 'claim', 'amended-claims-statement'])
    if 'heading' in children:
        amended_claims['heading'] = resolve_heading(children['heading'])
    amended_claims['claim'] = []
    if isinstance(children['claim'], list):
        for claim in children['claim']:
            amended_claims['claim'].append(resolve_claim(claim))
    else:
        amended_claims['claim'].append(resolve_claim(children['claim']))
    if 'amended-claims-statement' in children:
        amended_claims['amended-claims-statement'] = []
        if isinstance(children['amended-claims-statement'], list):
            for amended_claims_statement in children['amended-claims-statement']:
                amended_claims['amended-claims-statement'].append(resolve_amended_claims_statement(amended_claims_statement))
        else:
            amended_claims['amended-claims-statement'].append(resolve_amended_claims_statement(children['amended-claims-statement']))
    return amended_claims

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

def resolve_B880(elem: etree.Element) -> dict:
    '''
    <B880>: Publication of the deferred search report
    '''
    B880 = dict()
    children = get_children(elem, ['date', 'bnum'])
    if 'date' in children:
        B880['date'] = resolve_date(children['date'])
    if 'bnum' in children:
        B880['bnum'] = resolve_bnum(children['bnum'])
    return B880

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
    children = get_children(elem, ['B830', 'B840', 'B844EP', 'B848EP', 'B860', 'B870', 'B880'])
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
    if 'B880' in children:
        B800['B880'] = resolve_B880(children['B880'])
    return B800

def resolve_B796(elem: etree.Element) -> dict:
    '''
    <B796>: Designated states concerned
    '''
    B796 = dict()
    children = get_children(elem, ['ctry'])
    B796['ctry'] = []
    if isinstance(children['ctry'], list):
        for ctry in children['ctry']:
            B796['ctry'].append(resolve_ctry(ctry))
    else:
        B796['ctry'].append(resolve_ctry(children['ctry']))
    return B796

def resolve_B791(elem: etree.Element) -> dict:
    B791 = dict()
    children = get_children(elem, ['dnum', 'date', 'kind', 'snm', 'iid', 'adr', 'B796'])
    B791['dnum'] = resolve_dnum(children['dnum'])
    B791['date'] = resolve_date(children['date'])
    if 'kind' in children:
        B791['kind'] = resolve_kind(children['kind'])
    if 'snm' in children:
        B791['snm'] = resolve_snm(children['snm'])
    if 'iid' in children:
        B791['iid'] = resolve_iid(children['iid'])
    if 'adr' in children:
        B791['adr'] = resolve_adr(children['adr'])
    if 'B796' in children:
        B791['B796'] = resolve_B796(children['B796'])
    return B791

def resolve_B790(elem: etree.Element) -> dict:
    B790 = dict()
    children = get_children(elem, ['B791'])
    if 'B791' in children:
        B790['B791'] = []
        if isinstance(children['B791'], list):
            for B791 in children['B791']:
                B790['B791'].append(resolve_B791(B791))
        else:
            B790['B791'].append(resolve_B791(children['B791']))
    return B790

def resolve_B788(elem: etree.Element) -> dict:
    '''
    <B788>: Date of termination of the opposition procedure
    '''
    B788 = dict()
    children = get_children(elem, ['date'])
    B788['date'] = resolve_date(children['date'])
    return B788

def resolve_B787(elem: etree.Element) -> dict:
    '''
    <B787>: Date of rejection of the opposition procedure
    '''
    B787 = dict()
    children = get_children(elem, ['date'])
    B787['date'] = resolve_date(children['date'])
    return B787

def resolve_B784(elem: etree.Element) -> dict:
    '''
    <B784>: Attorney/agent of the opponent
    '''
    return resolve_name(elem)

def resolve_B781(elem: etree.Element) -> dict:
    '''
    <B781>: Opponent data
    '''
    B781 = dict()
    children = get_children(elem, ['dnum', 'date', 'kind', 'snm', 'iid', 'adr', 'B784'])
    B781['dnum'] = resolve_dnum(children['dnum'])
    B781['date'] = resolve_date(children['date'])
    B781['kind'] = resolve_kind(children['kind'])
    if 'snm' in children:
        B781['snm'] = resolve_snm(children['snm'])
    if 'iid' in children:
        B781['iid'] = resolve_iid(children['iid'])
    if 'adr' in children:
        B781['adr'] = resolve_adr(children['adr'])
    if 'B784' in children:
        B781['B784'] = resolve_B784(children['B784'])
    return B781

def resolve_B780(elem: etree.Element) -> dict:
    '''
    <B780>: Opposition(s)
    '''
    B780 = dict()
    children = get_children(elem, ['B781', 'B787', 'B788'])
    if 'B781' in children:
        B780['B781'] = []
        if isinstance(children['B781'], list):
            for B781 in children['B781']:
                B780['B781'].append(resolve_B781(B781))
        else:
            B780['B781'].append(resolve_B781(children['B781']))
    if 'B787' in children:
        B780['B787'] = resolve_B787(children['B787'])
    if 'B788' in children:
        B780['B788'] = resolve_B788(children['B788'])
    return B780

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
    children = get_children(elem, ['B710', 'B720', 'B730', 'B740', 'B780', 'B790'])
    if 'B710' in children:
        B700['B710'] = resolve_B710(children['B710'])
    if 'B720' in children:
        B700['B720'] = resolve_B720(children['B720'])
    if 'B730' in children:
        B700['B730'] = resolve_B730(children['B730'])
    if 'B740' in children:
        B700['B740'] = resolve_B740(children['B740'])
    if 'B780' in children:
        B700['B780'] = resolve_B780(children['B780'])
    if 'B790' in children:
        B700['B790'] = resolve_B790(children['B790'])
    return B700

def resolve_B620EP(elem: etree.Element) -> dict:
    '''
    <B620EP>: Divisional application(s)
    '''
    B620EP = dict()
    children = get_children(elem, ['parent'])
    if 'parent' in children:
        B620EP['parent'] = resolve_parent(children['parent'])
    return B620EP

def resolve_B620(elem: etree.Element) -> dict:
    '''
    <B620>: Parent application data
    '''
    B620 = dict()
    children = get_children(elem, ['parent'])
    B620['parent'] = resolve_parent(children['parent'])
    return B620

def resolve_B600(elem: etree.Element) -> dict:
    '''
    <B600>: References to other legally or procedurally related domestic patent documents
    '''
    B600 = dict()
    children = get_children(elem, ['B620', 'B620EP'])
    if 'B620' in children:
        B600['B620'] = resolve_B620(children['B620'])
    if 'B620EP' in children:
        B600['B620EP'] = resolve_B620EP(children['B620EP'])
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

def resolve_B566EP(elem: etree.Element) -> dict:
    '''
    <B566EP>: Date of dispatch for correction to the search report
    '''
    B566EP = dict()
    children = get_children(elem, ['date'])
    B566EP['date'] = resolve_date(children['date'])
    return B566EP

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
    children = get_children(elem, ['B561', 'B562', 'B565EP', 'B566EP'])
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
    if 'B566EP' in children:
        B560['B566EP'] = resolve_B566EP(children['B566EP'])
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

def resolve_B517EP(elem: etree.Element) -> str:
    '''
    <B517EP>: Non-obligatory suppl. class. - no longer used in IPCR - but for changes to any old files it may be present
    '''
    return elem.text

def resolve_B516(elem: etree.Element) -> str:
    '''
    <B516>: Will contain "version" edition statement indicator 8 or, for earlier files 7, etc
    '''
    return elem.text

def resolve_B514(elem: etree.Element) -> str:
    '''
    <B514>: as B517EP
    '''
    return elem.text

def resolve_B513(elem: etree.Element) -> str:
    '''
    <B513>: Non inventive classification
    '''
    return elem.text

def resolve_B512(elem: etree.Element) -> str:
    '''
    <B512>: Inventive classification would be B511 & B512
    '''
    return elem.text

def resolve_B511(elem: etree.Element) -> str:
    '''
    <B511>: First information
    '''
    return elem.text

def resolve_B510(elem: etree.Element) -> dict:
    B510 = dict()
    children = get_children(elem, ['B516', 'B511', 'B512', 'B513', 'B514', 'B517EP'])
    if 'B516' in children:
        B510['B516'] = resolve_B516(children['B516'])
    B510['B511'] = resolve_B511(children['B511'])
    if 'B512' in children:
        B510['B512'] = []
        if isinstance(children['B512'], list):
            for B512 in children['B512']:
                B510['B512'].append(resolve_B512(B512))
        else:
            B510['B512'].append(resolve_B512(children['B512']))
    if 'B513' in children:
        B510['B513'] = []
        if isinstance(children['B513'], list):
            for B513 in children['B513']:
                B510['B513'].append(resolve_B513(B513))
        else:
            B510['B513'].append(resolve_B513(children['B513']))
    if 'B514' in children:
        B510['B514'] = []
        if isinstance(children['B514'], list):
            for B514 in children['B514']:
                B510['B514'].append(resolve_B514(B514))
        else:
            B510['B514'].append(resolve_B514(children['B514']))
    if 'B517EP' in children:
        B510['B517EP'] = resolve_B517EP(children['B517EP'])    
    return B510

def resolve_B500(elem: etree.Element) -> dict:
    '''
    <B500>: Technical Data
    '''
    B500 = dict()
    children = get_children(elem, ['B510', 'B510EP', 'B540', 'B560', 'B590'])
    if 'B510' in children:
        B500['B510'] = resolve_B510(children['B510'])
    if 'B510EP' in children:
        B500['B510EP'] = resolve_B510EP(children['B510EP'])
    if 'B540' in children:
        B500['B540'] = resolve_B540(children['B540'])
    if 'B560' in children:
        B500['B560'] = resolve_B560(children['B560'])
    if 'B590' in children:
        B500['B590'] = resolve_B590(children['B590'])
    return B500

def resolve_B480(elem: etree.Element) -> dict:
    '''
    <B480>: Corrigendum issued data
    '''
    B480 = dict()
    children = get_children(elem, ['date', 'bnum'])
    if 'date' in children:
        B480['date'] = resolve_date(children['date'])
    if 'bnum' in children:
        B480['bnum'] = resolve_bnum(children['bnum'])
    return B480

def resolve_B477(elem: etree.Element) -> dict:
    '''
    [root]<B477>: Document printed as amended, third level of publication (e.g. EPO 'B2')
    '''
    B477 = dict()
    children = get_children(elem, ['date', 'bnum'])
    if 'date' in children:
        B477['date'] = resolve_date(children['date'])
    if 'bnum' in children:
        B477['bnum'] = resolve_bnum(children['bnum'])
    return B477

def resolve_B475(elem: etree.Element) -> list:
    '''
    <B475>: Lapse of a patent
    '''
    B475 = list()
    children_group = get_children_group(elem, {
        'g': ['date', 'ctry']
    })
    for g in children_group['g']:
        tmp = {}
        if 'date' in g:
            tmp['date'] = resolve_date(g['date'])
        if 'ctry' in g:
            tmp['ctry'] = resolve_ctry(g['ctry'])
        B475.append(tmp)
    return B475

def resolve_B472(elem: etree.Element) -> dict:
    '''
    <B472>: Term of grant
    '''
    B472 = dict()
    children = get_children(elem, ['B475'])
    if 'B475' in children:
        children['B475'] = resolve_B475(children['B475'])
    return B472

def resolve_B4530EP(elem: etree.Element) -> dict:
    '''
    <B4530EP>: existing INID code (45) will be used with the title: "Date of publication and mention of the limitation decision:"
    Note: limitation-sequence relates to the number in <B090EP>
    '''
    B4530EP = dict()
    B4530EP['attr'] = get_attr(elem)
    children = get_children(elem, ['kind', 'date', 'bnum'])
    B4530EP['kind'] = resolve_kind(children['kind'])
    B4530EP['date'] = resolve_date(children['date'])
    B4530EP['bnum'] = resolve_bnum(children['bnum'])
    return B4530EP

def resolve_B453EP(elem: etree.Element) -> dict:
    '''
    <B453EP>: Limitation decision
    '''
    B453EP = dict()
    children = get_children(elem, ['B4530EP'])
    B453EP['B4530EP'] = []
    if isinstance(children['B4530EP'], list):
        for B4530EP in children['B4530EP']:
            B453EP['B4530EP'].append(resolve_B4530EP(B4530EP))
    else:
        B453EP['B4530EP'].append(resolve_B4530EP(children['B4530EP']))
    return B453EP

def resolve_B452EP(elem: etree.Element) -> dict:
    '''
    <B452EP>: Date of announcement of intention to grant (after 01.07.2002)
    '''
    B452EP = dict()
    children = get_children(elem, ['date'])
    B452EP['date'] = resolve_date(children['date'])
    return B452EP

def resolve_B451EP(elem: etree.Element) -> dict:
    '''
    <B451EP>: Date of announcement of intention to grant
    '''
    B451EP = dict()
    children = get_children(elem, ['date'])
    B451EP['date'] = resolve_date(children['date'])
    return B451EP

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
    children = get_children(elem, ['B405', 'B430', 'B450', 'B451EP', 'B452EP', 'B453EP', 'B472', 'B477', 'B480'])
    if 'B405' in children:
        B400['B405'] = resolve_B405(children['B405'])
    if 'B430' in children:
        B400['B430'] = resolve_B430(children['B430'])
    if 'B450' in children:
        B400['B450'] = resolve_B450(children['B450'])
    if 'B451EP' in children:
        B400['B451EP'] = resolve_B451EP(children['B451EP'])
    if 'B452EP' in children:
        B400['B452EP'] = resolve_B452EP(children['B452EP'])
    if 'B453EP' in children:
        B400['B453EP'] = resolve_B453EP(children['B453EP'])
    if 'B472' in children:
        B400['B472'] = resolve_B472(children['B472'])
    if 'B477' in children:
        B400['B477'] = resolve_B477(children['B477'])
    if 'B480' in children:
        B400['B480'] = resolve_B480(children['B480'])
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

def resolve_B300(elem: etree.Element) -> list:
    '''
    <B300>:
        (<B310>, <B320>, <B330>)*: Priority data
    '''
    B300 = list()
    children_group = get_children_group(elem, {
        'g': ['B310', 'B320', 'B330']
    })
    for g in children_group['g']:
        B300.append({
            'B310': resolve_B310(g['B310']),
            'B320': resolve_B320(g['B320']),
            'B330': resolve_B330(g['B330'])
        })
    return B300

def resolve_B270(elem: etree.Element) -> dict:
    '''
    <B270>: Previously filed application
    '''
    B270 = dict()
    children = get_children(elem, ['dnum', 'date', 'ctry'])
    B270['dnum'] = resolve_dnum(children['dnum'])
    B270['date'] = resolve_date(children['date'])
    B270['ctry'] = resolve_ctry(children['ctry'])
    return B270

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

def resolve_B246(elem: etree.Element) -> dict:
    '''
    <B246>: Date of resumption of proceedings (Rule 14 / Rule 142)
    '''
    B246 = dict()
    children = get_children(elem, ['date'])
    B246['date'] = resolve_date(children['date'])
    return B246

def resolve_B245EP(elem: etree.Element) -> str:
    '''
    <B245EP>: Suspension/Interruption indicator
    '''
    return elem.text

def resolve_B245(elem: etree.Element) -> dict:
    '''
    <B245>: Date of suspension (Rule 14) / Interruption (Rule 142) of proceedings
    '''
    B245 = dict()
    children = get_children(elem, ['date'])
    B245['date'] = resolve_date(children['date'])
    return B245

def resolve_B243(elem: etree.Element) -> dict:
    '''
    <B243>: Date of 'patent maintained as amended'
    '''
    B243 = dict()
    children = get_children(elem, ['date'])
    B243['date'] = resolve_date(children['date'])
    return B243

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
    children = get_children(elem, ['B241', 'B242', 'B243', 'B245', 'B245EP', 'B246'])
    if 'B241' in children:
        B240['B241'] = resolve_B241(children['B241'])
    if 'B242' in children:
        B240['B242'] = resolve_B242(children['B242'])
    if 'B243' in children:
        B240['B243'] = resolve_B243(children['B243'])
    if 'B245' in children:
        B240['B245'] = resolve_B245(children['B245'])
    if 'B245EP' in children:
        B240['B245EP'] = resolve_B245EP(children['B245EP'])
    if 'B246' in children:
        B240['B246'] = resolve_B246(children['B246'])
    return B240

def resolve_B238(elem: etree.Element) -> dict:
    '''
    <B238EP>: Date of decision for reestablishment of rights
    '''
    B238 = dict()
    children = get_children(elem, ['date'])
    B238['date'] = resolve_date(children['date'])
    return B238

def resolve_B238EP(elem: etree.Element) -> dict:
    '''
    <B238EP>: Date of receipt of request for reestablishment of rights
    '''
    B238EP = dict()
    children = get_children(elem, ['date'])
    B238EP['date'] = resolve_date(children['date'])
    return B238EP

def resolve_B236(elem: etree.Element) -> dict:
    '''
    <B236>: Date of withdrawal of application
    '''
    B236 = dict()
    children = get_children(elem, ['date'])
    B236['date'] = resolve_date(children['date'])
    return B236

def resolve_B230(elem: etree.Element) -> dict:
    '''
    <B230>: Other dates
    '''
    B230 = dict()
    children = get_children(elem, ['B236', 'B238EP', 'B238'])
    if 'B236' in children:
        B230['B236'] = resolve_B236(children['B236'])
    if 'B238EP' in children:
        B230['B238EP'] = resolve_B238EP(children['B238EP'])
    if 'B238' in children:
        B230['B238'] = resolve_B238(children['B238'])
    return B230

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
    children = get_children(elem, ['B210', 'B220', 'B230', 'B240', 'B250', 'B251EP', 'B260', 'B270'])
    B200['B210'] = resolve_B210(children['B210'])
    B200['B220'] = resolve_B220(children['B220'])
    if 'B230' in children:
        B200['B230'] = resolve_B230(children['B230'])
    if 'B240' in children:
        B200['B240'] = resolve_B240(children['B240'])
    if 'B250' in children:
        B200['B250'] = resolve_B250(children['B250'])
    if 'B251EP' in children:
        B200['B251EP'] = resolve_B251EP(children['B251EP'])
    if 'B260' in children:
        B200['B260'] = resolve_B260(children['B260'])
    if 'B270' in children:
        B200['B270'] = resolve_B270(children['B270'])
    return B200

def resolve_B190(elem: etree.Element) -> str:
    '''
    <B190>: Publishing country or organisation
    '''
    return elem.text

def resolve_B1552(elem: etree.Element) -> str:
    '''
    <B1552>: Part text
    '''
    return elem.text

def resolve_B1551(elem: etree.Element) -> str:
    '''
    <B1551>: Part language
    '''
    return elem.text

def resolve_B155(elem: etree.Element) -> list:
    '''
    <B155>: Affected parts of document
    '''
    B155 = list()
    children_group = get_children_group(elem, {
        'g': ['B1551', 'B1552']
    })
    for g in children_group['g']:
        B155.append({
            'B1551': resolve_B1551(g['B1551']),
            'B1552': resolve_B1552(g['B1552'])
        })
    return B155

def resolve_B1542(elem: etree.Element) -> str:
    '''
    <B1542>: Note text
    '''
    return elem.text

def resolve_B1541(elem: etree.Element) -> str:
    '''
    <B1541>: Note language
    '''
    return elem.text

def resolve_B154(elem: etree.Element) -> list:
    '''
    <B154>: Standard notes
    '''
    B154 = list()
    children_group = get_children_group(elem, {
        'g': ['B1541', 'B1542']
    })
    for g in children_group['g']:
        B154.append({
            'B1541': resolve_B1551(g['B1541']),
            'B1542': resolve_B1552(g['B1542'])
        })
    return B154

def resolve_B153(elem: etree.Element) -> str:
    '''
    <B153>: Affected INID codes</B153>
    '''
    return elem.text

def resolve_B151(elem: etree.Element) -> str:
    '''
    <B151>: Supplementary correction code
    '''
    return elem.text

def resolve_B150(elem: etree.Element) -> dict:
    '''
    <B150>: Patent correction information
    '''
    B150 = dict()
    children = get_children(elem, ['B151', 'B153', 'B154', 'B155'])
    if 'B151' in children:
        B150['B151'] = resolve_B151(children['B151'])
    if 'B153' in children:
        B150['B153'] = resolve_B153(children['B153'])
    if 'B154' in children:
        B150['B154'] = resolve_B154(children['B154'])
    if 'B155' in children:
        B150['B155'] = resolve_B155(children['B155'])
    return B150

def resolve_B140(elem: etree.Element) -> dict:
    '''
    <B140>: Date of publication
    '''
    B140 = dict()
    children = get_children(elem, ['date'])
    B140['date'] = resolve_date(children['date'])
    return B140

def resolve_B132EP(elem: etree.Element) -> str:
    '''
    <B132EP>: Original kind code
    '''
    return elem.text

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
    children = get_children(elem, ['B110', 'B120', 'B130', 'B132EP', 'B140', 'B150', 'B190'])
    B100['B110'] = resolve_B110(children['B110'])
    if 'B120' in children:
        B100['B120'] = resolve_B120(children['B120'])
    B100['B130'] = resolve_B110(children['B130'])
    if 'B132EP' in children:
        B100['B132EP'] = resolve_B132EP(children['B132EP'])
    B100['B140'] = resolve_B140(children['B140'])
    if 'B150' in children:
        B100['B150'] = resolve_B150(children['B150'])
    B100['B190'] = resolve_B190(children['B190'])
    return B100

def resolve_B0933EP(elem: etree.Element) -> dict:
    '''
    <B0933EP>: Full payment received on
    '''
    B0933EP = dict()
    children = get_children(elem, ['date'])
    B0933EP['date'] = resolve_date(children['date'])
    return B0933EP

def resolve_B0932EP(elem: etree.Element) -> dict:
    '''
    <B0932EP>: Translation received on
    '''
    B0932EP = dict()
    children = get_children(elem, ['date'])
    B0932EP['date'] = resolve_date(children['date'])
    return B0932EP

def resolve_B0931EP(elem: etree.Element) -> dict:
    '''
    <B0931EP>: Despatched on
    '''
    B0931EP = dict()
    children = get_children(elem, ['date'])
    B0931EP['date'] = resolve_date(children['date'])
    return B0931EP

def resolve_B093EP(elem: etree.Element) -> dict:
    '''
    <B093EP>: Limitation procedure - Limitation request allowed fields
    '''
    B093EP = dict()
    children = get_children(elem, ['B0931EP', 'B0932EP', 'B0933EP'])
    B093EP['B0931EP'] = resolve_B0931EP(children['B0931EP'])
    if 'B0932EP' in children:
        B093EP['B0932EP'] = resolve_B0932EP(children['B0932EP'])
    if 'B0933EP' in children:
        B093EP['B0933EP'] = resolve_B0933EP(children['B0933EP'])
    return B093EP

def resolve_B0914EP(elem: etree.Element) -> dict:
    '''
    <B0914EP>: Date of payment
    '''
    B0914EP = dict()
    children = get_children(elem, ['date'])
    B0914EP['date'] = resolve_date(children['date'])
    return B0914EP

def resolve_B0913EP(elem: etree.Element) -> str:
    '''
    <B0912EP>: Limitation kind
    '''
    return elem.text

def resolve_B0912EP(elem: etree.Element) -> str:
    '''
    <B0913EP>: Decision code
    '''
    return elem.text

def resolve_B0911EP(elem: etree.Element) -> dict:
    '''
    <B0911EP>: Date of filing
    '''
    B0911EP = dict()
    children = get_children(elem, ['date'])
    B0911EP['date'] = resolve_date(children['date'])
    return B0911EP

def resolve_B091EP(elem: etree.Element) -> dict:
    '''
    <B091EP>: Limitation procedure - Initial filing
    '''
    B091EP = dict()
    children = get_children(elem, ['B0911EP', 'B0912EP', 'B0913EP', 'B0914EP'])
    B091EP['B0911EP'] = resolve_B0911EP(children['B0911EP'])
    if 'B0912EP' in children:
        B091EP['B0912EP'] = resolve_B0912EP(children['B0912EP'])
    if 'B0913EP' in children:
        B091EP['B0913EP'] = resolve_B0913EP(children['B0913EP'])
    if 'B0914EP' in children:
        B091EP['B0914EP'] = resolve_B0914EP(children['B0914EP'])
    return B091EP

def resolve_B0900EP(elem: etree.Element) -> dict:
    '''
    <B0900EP>: sub-group of B090EP
    '''
    B0900EP = dict()
    B0900EP['attr'] = get_attr(elem)
    children = get_children(elem, ['B091EP', 'B093EP'])
    B0900EP['B091EP'] = []
    if isinstance(children['B091EP'], list):
        for B091EP in children['B091EP']:
            B0900EP['B091EP'].append(resolve_B091EP(B091EP))
    else:
        B0900EP['B091EP'].append(resolve_B091EP(children['B091EP']))
    if 'B093EP' in children:
        B0900EP['B093EP'] = resolve_B093EP(children['B093EP'])
    return B0900EP

def resolve_B090EP(elem: etree.Element) -> dict:
    '''
    <B090EP>: Limitation procedure
    '''
    B090EP = dict()
    children = get_children(elem, ['B0900EP'])
    B090EP['B0900EP'] = []
    if isinstance(children['B0900EP'], list):
        for B0900EP in children['B0900EP']:
            B090EP['B0900EP'].append(resolve_B0900EP(B0900EP))
    else:
        B090EP['B0900EP'].append(resolve_B0900EP(children['B0900EP']))
    return B090EP

def resolve_B078EP(elem: etree.Element) -> dict:
    '''
    <B078EP>: Date of 'No opposition filed
    '''
    B078EP = dict()
    children = get_children(elem, ['date'])
    B078EP['date'] = resolve_date(children['date'])
    return B078EP

def resolve_B0756EP(elem: etree.Element) -> str:
    '''
    <B0756EP>: Kind of decision : R01 to R12
    '''
    return elem.text

def resolve_B0755EP(elem: etree.Element) -> dict:
    '''
    <B0755EP>: Date of decision
    '''
    B0753EP = dict()
    children = get_children(elem, ['date'])
    B0753EP['date'] = resolve_date(children['date'])
    return B0753EP

def resolve_B0753EP(elem: etree.Element) -> dict:
    '''
    <B0753EP>: Date of notice of petition (May be included at a later date)
    '''
    B0753EP = dict()
    children = get_children(elem, ['date'])
    B0753EP['date'] = resolve_date(children['date'])
    return B0753EP

def resolve_B0752EP(elem: etree.Element) -> str:
    '''
    <B0752EP>: Petitioner code
    '''
    return elem.text

def resolve_B0751EP(elem: etree.Element) -> str:
    '''
    <B0751EP>: Appeal number
    '''
    return elem.text

def resolve_B0750EP(elem: etree.Element) -> dict:
    '''
    Petition for review number (As we can have multiple petitions for review). Comprises a unique number for a given year, e.g. R0001/08
    '''
    B0750EP = dict()
    B0750EP['attr'] = get_attr(elem)
    children = get_children(elem, ['B0751EP', 'B0752EP', 'B0753EP', 'B0755EP', 'B0756EP'])
    if 'B0751EP' in children:
        B0750EP['B0751EP'] = resolve_B0751EP(children['B0751EP'])
    if 'B0752EP' in children:
        B0750EP['B0752EP'] = resolve_B0752EP(children['B0752EP'])
    if 'B0753EP' in children:
        B0750EP['B0753EP'] = resolve_B0753EP(children['B0753EP'])
    if 'B0755EP' in children:
        B0750EP['B0755EP'] = resolve_B0755EP(children['B0755EP'])
    if 'B0756EP' in children:
        B0750EP['B0756EP'] = resolve_B0756EP(children['B0756EP'])
    return B0750EP

def resolve_B075EP(elem: etree.Element) -> dict:
    '''
    <B075EP>: Petition for review
    '''
    B075EP = dict()
    children = get_children(elem, ['B0750EP'])
    B075EP['B0750EP'] = []
    if isinstance(children['B0750EP'], list):
        for B0750EP in children['B0750EP']:
            B075EP['B0750EP'].append(resolve_B0750EP(B0750EP))
    else:
        B075EP['B0750EP'].append(resolve_B0750EP(children['B0750EP']))
    return B075EP

def resolve_B070EP(elem: etree.Element) -> str:
    '''
    <B070EP>: B publication technical field (subsequently filed technical information)
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

def resolve_B015EP(elem: etree.Element) -> str:
    '''
    <B015EP>: Number of copies to be printed
    '''
    return elem.text

def resolve_B011EP(elem: etree.Element) -> dict:
    '''
    <B011EP>: Serial number date and states
    '''
    B011EP = dict()
    children = get_children(elem, ['date', 'dnum', 'ctry'])
    B011EP['date'] = resolve_date(children['date'])
    B011EP['dnum'] = resolve_dnum(children['dnum'])
    if 'ctry' in children:
        B011EP['ctry'] = []
        if isinstance(children['ctry'], list):
            for ctry in children['ctry']:
                B011EP['ctry'] = resolve_ctry(ctry)
        else:
            B011EP['ctry'] = resolve_ctry(children['ctry'])
    return B011EP

def resolve_B010EP(elem: etree.Element) -> dict:
    '''
    <B010EP>: Other rights and legal means of execution
    '''
    B010EP = dict()
    children = get_children(elem, ['B011EP'])
    B010EP['B011EP'] = []
    if isinstance(children['B011EP'], list):
        for B011EP in children['B011EP']:
            B010EP['B011EP'].append(resolve_B011EP(B011EP))
    else:
        B010EP['B011EP'].append(resolve_B011EP(children['B011EP']))
    return B010EP

def resolve_B009EP(elem: etree.Element) -> dict:
    '''
    <B009EP>: Text from B725EP tag in the three EPO official languages
    Note: The text language order is German, English and French.
    '''
    B009EP = dict()
    children = get_children(elem, ['text'])
    B009EP['text'] = []
    if isinstance(children['text'], list):
        for text in children['text']:
            B009EP['text'].append(resolve_text(text))
    else:
        B009EP['text'].append(resolve_text(children['text']))
    return B009EP

def resolve_B008EP(elem: etree.Element) -> str:
    '''
    <B008EP>: Indicator for "small changes" === 8
    '''
    return elem.text

def resolve_B007EP(elem: etree.Element) -> str:
    '''
    [useless]<B007EP>: Reserved for EPO internal use
    '''
    return elem.text

def resolve_B005EP(elem: etree.Element) -> str:
    '''
    [useless]<B005EP>: Printer/Producer identification
    '''
    return elem.text

def resolve_B004EP(elem: etree.Element) -> str:
    '''
    <B004EP>: Re-establishment of rights indicator
    '''
    return elem.text

def resolve_B003EP(elem: etree.Element) -> str:
    '''
    <B003EP>: Indicator 'no A-document published by EPO'
    '''
    return elem.text

def resolve_B001EP(elem: etree.Element) -> str:
    '''
    <B001EP>: Selective mask for states involved
    '''
    return elem.text

def resolve_eptags(elem: etree.Element) -> dict:
    '''
    <eptags>: EPO specific tags
    '''
    eptags = dict()
    children = get_children(elem, [
        'B001EP',
        'B003EP',
        'B004EP',
        'B005EP',
        'B007EP',
        'B008EP',
        'B009EP',
        'B010EP',
        'B015EP',
        'B050EP',
        'B053EP',
        'B070EP',
        'B075EP',
        'B078EP',
        'B090EP'])
    if 'B001EP' in children:
        eptags['B001EP'] = resolve_B001EP(children['B001EP'])
    if 'B003EP' in children:
        eptags['B003EP'] = resolve_B003EP(children['B003EP'])
    if 'B004EP' in children:
        eptags['B004EP'] = resolve_B004EP(children['B004EP'])
    if 'B005EP' in children:
        eptags['B005EP'] = resolve_B005EP(children['B005EP'])
    if 'B007EP' in children:
        eptags['B007EP'] = resolve_B007EP(children['B007EP'])
    if 'B008EP' in children:
        eptags['B008EP'] = resolve_B008EP(children['B008EP'])
    if 'B009EP' in children:
        eptags['B009EP'] = resolve_B009EP(children['B009EP'])
    if 'B010EP' in children:
        eptags['B010EP'] = resolve_B010EP(children['B010EP'])
    if 'B015EP' in children:
        eptags['B015EP'] = resolve_B015EP(children['B015EP'])
    if 'B050EP' in children:
        eptags['B050EP'] = resolve_B050EP(children['B050EP'])
    if 'B053EP' in children:
        eptags['B053EP'] = []
        if isinstance(children['B053EP'], list):
            for B053EP in children['B053EP']:
                eptags['B053EP'].append(resolve_B053EP(B053EP))
        else:
            eptags['B053EP'].append(resolve_B053EP(children['B053EP']))
    if 'B070EP' in children:
        eptags['B070EP'] = resolve_B070EP(children['B070EP'])
    if 'B075EP' in children:
        eptags['B075EP'] = resolve_B075EP(children['B075EP'])
    if 'B078EP' in children:
        eptags['B078EP'] = resolve_B078EP(children['B078EP'])
    if 'B090EP' in children:
        eptags['B090EP'] = resolve_B090EP(children['B090EP'])
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

'''
main
'''
def parse(xml: bytes) -> dict:
    patent = {
        'version': '1.0.0'
    }
    root = etree.XML(xml)
    patent['attr'] = get_attr(root)
    children = get_children(root, [
        'SDOBI',
        'abstract',
        'description',
        'claims',
        'amended-claims',
        'amended-claims-statement',
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
    if 'amended-claims-statement' in children:
        patent['amended-claims-statement'] = []
        if isinstance(children['amended-claims-statement'], list):
            for amended_claims_statement in children['amended-claims-statement']:
                patent['amended-claims-statement'].append(resolve_amended_claims_statement(amended_claims_statement))
        else:
            patent['amended-claims-statement'].append(resolve_amended_claims_statement(children['amended-claims-statement']))
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

if __name__ == '__main__':
    with open('resources/EP17785948NWA1.xml', 'rb') as fin:
        xml = fin.read()
    patent = parse(xml)
    pass
    from generate_md import generate_md
    with open('data/EP17785948NWA1.md', 'w', encoding='utf-8') as fout:
        fout.write(generate_md(patent))
    # import json
    # print(json.dumps(patent, indent=4, ensure_ascii=False))
