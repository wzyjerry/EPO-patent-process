def trans_date(field: dict) -> str:
        text = str(field['date'])
        return '%s.%s.%s' % (text[6:], text[4:6], text[:4])

def trans_4xx(field: dict, lang: str) -> str:
    text = str(field['bnum'])
    return '%s %s %s/%s' % (trans_date(field), labels['bulletin'][lang], text[:4], text[4:])

def trans_ipc(field: str) -> str:
    field = field.split()
    return '%s %s %s %s' % (field[0][1:], field[1][:2], field[1][2:], field[2])

def trans_ipcr(field: dict) -> str:
    text = field['text'].split()
    return '%s %s <sup>(%s.%s)</sup>' % (text[0], text[1], text[2][:4], text[2][4:6])

def trans_name(field: dict, out_str: bool) -> str:
    if 'B725EP' in field:
        return '<br>'.join(field['B725EP']['text'])
    if 'sfx' in field:
        sfx = field['sfx']
    else:
        sfx = ''
    snm = field['snm'] + sfx
    if 'adr' not in field or len(field['adr']) == 0:
        return snm
    adr = field['adr']
    if out_str and 'str' in adr:
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

def trans_doc(field: dict) -> str:
    dnum = field['dnum']
    anum = dnum['anum']
    if 'pnum' in dnum:
        pnum = dnum['pnum']
        return '%s / %s' % (anum, format(int(pnum), ',').replace(',', ' '))
    else:
        return anum
labels = {
    15: {
        'de': [
            'Korrekturinformation',
            'Korrigierte Fassung Nr.',
            'Korrekturen, siehe'
        ],
        'en': [
            'Correction information',
            'Corrected version no',
            'Corrections, see'
        ],
        'fr': [
            'Information de correction',
            'Version corrigée no',
            'Corrections, voir'
        ]
    },
    21: {
        'de': 'Anmeldenummer',
        'en': 'Application number',
        'fr': 'Numéro de dépôt'
    },
    22: {
        'de': 'Anmeldetag',
        'en': 'Date of filing',
        'fr': 'Date de dépôt'
    },
    30: {
        'de': 'Priorität',
        'en': 'Priority',
        'fr': 'Priorité'
    },
    43: {
        'de': {
            'A1': 'Veröffentlichungstag',
            'A3': 'Veröffentlichungstag A2',
            'A8': 'Veröffentlichungstag',
            'A9': 'Veröffentlichungstag',
            'B1': 'Veröffentlichungstag der Anmeldung',
            'B2': 'Veröffentlichungstag der Anmeldung',
            'B3': 'Veröffentlichungstag der Anmeldung',
            'B9': 'Veröffentlichungstag der Anmeldung'
        },
        'en': {
            'A1': 'Date of publication',
            'A3': 'Date of publication A2',
            'A8': 'Date of publication',
            'A9': 'Date of publication',
            'B1': 'Date of publication of application',
            'B2': 'Date of publication of application',
            'B3': 'Date of publication of application',
            'B9': 'Date of publication of application'
        },
        'fr': {
            'A1': 'Date de publication',
            'A3': 'Date de publication A2',
            'A8': 'Date de publication',
            'A9': 'Date de publication',
            'B1': 'Date de publication de la demande',
            'B2': 'Date de publication de la demande',
            'B3': 'Date de publication de la demande',
            'B9': 'Date de publication de la demande'
        }
    },
    45: {
        'de': {
            'B1': 'Veröffentlichungstag und Bekanntmachung des Hinweises auf die Patenterteilung',
            'B2': {
                45: 'Hinweis auf die Patenterteilung',
                47: 'Veröffentlichungstag und Bekanntmachung des Hinweises auf die Entscheidung über den Einspruch'
            },
            'B9': {
                45: 'Hinweis auf die Patenterteilung',
                47: 'Veröffentlichungstag und Bekanntmachung des Hinweises auf die Entscheidung über den Einspruch'
            }
        },
        'en': {
            'B1': 'Date of publication and mention of the grant of the patent',
            'B2': {
                45: 'Mention of the grant of the patent',
                47: 'Date of publication and mention of the opposition decision:'
            },
            'B9': {
                45: 'Mention of the grant of the patent',
                47: 'Date of publication and mention of the opposition decision:'
            }
        },
        'fr': {
            'B1': 'Date de publication et mention de la délivrance du brevet',
            'B2': {
                45: 'Mention de la délivrance du brevet',
                47: 'Date de publication et mention de la décision concernant l’opposition'
            },
            'B9': {
                45: 'Mention de la délivrance du brevet',
                47: 'Date de publication et mention de la décision concernant l’opposition'
            }
        }
    },
    48: {
        'de': 'Corrigendum ausgegeben am',
        'en': 'Corrigendum issued on',
        'fr': 'Corrigendum publié le'
    },
    51: {
        'de': 'Int Cl.',
        'en': 'Int Cl.',
        'fr': 'Int Cl.',
    },
    56: {
        'de': 'Entgegenhaltungen',
        'en': 'References cited',
        'fr': 'Documents cités'            
    },
    60: {
        'de': 'Teilanmeldung',
        'en': 'Divisional application',
        'fr': 'Demande divisionnaire'
    },
    71: {
        'de': 'Anmelder',
        'en': 'Applicant',
        'fr': 'Demandeur'
    },
    72: {
        'de': 'Erfinder',
        'en': 'Inventor',
        'fr': 'Inventeur'
    },
    73: {
        'de': 'Patentinhaber',
        'en': 'Proprietor',
        'fr': 'Titulaire'
    },
    74: {
        'de': 'Vertreter',
        'en': 'Representative',
        'fr': 'Mandataire'
    },
    84: {
        'de': [
            'Benannte Vertragsstaaten',
            'Benannte Erstreckungsstaaten',
            'Benannte Validierungsstaaten'
        ],
        'en': [
            'Designated Contracting States',
            'Designated Extension States',
            'Designated Validation States'
        ],
        'fr': [
            'Etats contractants désignés',
            'Etats d’extension désignés',
            'Etats de validation désignés'
        ]
    },
    86: {
        'de': 'Internationale Anmeldenummer',
        'en': 'International application number',
        'fr': 'Numéro de dépôt international'
    },
    87: {
        'de': 'Internationale Veröffentlichungsnummer',
        'en': 'International publication number',
        'fr': 'Numéro de publication internationale'
    },
    88: {
        'de': 'Veröffentlichungstag A3',
        'en': 'Date of publication A3',
        'fr': 'Date de publication A3'
    },
    'bulletin': {
        'de': 'Patentblatt',
        'en': 'Bulletin',
        'fr': 'Bulletin'
    },
    'description': {
        'de': 'Beschreibung',
        'en': 'Description',
        'fr': 'Description'
    },
    'remarks': {
        'de': 'Bemerkungen',
        'en': 'Remarks'
    }
}

def generate_md(patent: str) -> str:
    md = []
    
    kind = patent['attr']['kind']
    lang = patent['attr']['lang']

    SDOBI = patent['SDOBI']
    B000 = SDOBI['B000']
    eptags = B000['eptags']
    B100 = SDOBI['B100']
    B200 = SDOBI['B200']
    B400 = SDOBI['B400']
    B500 = SDOBI['B500']
    B700 = SDOBI['B700']
    B800 = SDOBI['B800']
    md.append('# (11)(19) **%s %s %s**' % (B100['B190'], format(int(B100['B110']), '0>7,').replace(',', ' '), B100['B130']))
    if 'B120' in B100:
        if 'B121EP' in B100['B120']:
            md.append('## (12) **%s**<br>%s' % (B100['B120']['B121'], B100['B120']['B121EP']))
        else:
            md.append('## (12) **%s**' % B100['B120']['B121'])
    if kind in ['A3']:
        md.append('## (88) %s:<br>**%s**' % (labels[88][lang], trans_4xx(B800['B880'], lang)))
    if kind in ['B1']:
        md.append('## (45) %s:<br>**%s**' % (labels[45][lang][kind], trans_4xx(B400['B450'], lang)))
    if kind in ['A8', 'A9', 'B9']:
        B150 = B100['B150']
        md.append('## (15) %s:<br>' % labels[15][lang][0])
        B151 = B150['B151']
        if B151[0] == 'W':
            md.append('**%s %s (%s %s)**<br>' % (labels[15][lang][1], B151[1:], B151, B100['B132EP']))
        else:
            raise Exception('not W')
        # TODO: Mismatch here. eg. EP10153923W1B9
        # TODO: EP12812953W1B9
        md.append('**%s**<br>' % labels[15][lang][2])
        for B155 in B150['B155']:
            if B155['B1551'] == lang:
                if 'B153' in B150:
                    md.append('**%s&emsp;&emsp;INID code(s)&emsp;&emsp;%s**' % (B155['B1552'], B150['B153']))
                elif 'B154' in B150:
                    for B154 in B150['B154']:
                        if B154['B1541'] == lang:
                            md.append('**%s**<br>**%s**' % (B155['B1552'], B154['B1542']))
                else:
                    md.append('<br>**%s**<br>' % (B155['B1552']))
        md.append('## (48) %s:<br>**%s**' % (labels[48][lang], trans_4xx(B400['B480'], lang)))
    if kind in ['B2', 'B9']:
        if 'B477' in B400:
            md.append('## (45) %s<br>**%s**' % (labels[45][lang][kind][47], trans_4xx(B400['B477'], lang)))
        md.append('## (45) %s<br>**%s**' % (labels[45][lang][kind][45], trans_4xx(B400['B450'], lang)))
    if kind in ['B3']:
        md.append('## (45) Date of publication and mention of the limitation decision:<br>')
        for B4530EP in B400['B453EP']['B4530EP']:
            md.append('1. **%s-%s %s**' % (B4530EP['kind'], B4530EP['attr']['limitation-sequence'], trans_4xx(B4530EP, lang)))
        md.append('## (45) Mention of the grant of the patent:<br>**%s**' % trans_4xx(B400['B450'], lang))
    if kind in ['A1', 'A3', 'A8', 'A9']:
        md.append('## (43) %s:<br>**%s**' % (labels[43][lang][kind], trans_4xx(B400['B430'], lang)))
    md.append('## (21) %s: **%s**' % (labels[21][lang], B200['B210']))
    md.append('## (22) %s: **%s**' % (labels[22][lang], trans_date(B200['B220'])))
    if 'B510' in B500:
        B510 = B500['B510']
        md.append('## (51) %s<sup>%s</sup>:' % (labels[51][lang], B510['B516']))
        md.append('+ **%s**' % trans_ipc(B510['B511']))
        if 'B512' in B510:
            for B512 in B510['B512']:
                md.append('+ %s' % trans_ipc(B512))
        if 'B513' in B510:
            for B513 in B510['B513']:
                md.append('+ %s' % trans_ipc(B513))
        if 'B514' in B510:
            md.append('+ %s' % B510['B517EP'])
    if 'B510EP' in B500:
        md.append('## (51) %s:' % labels[51][lang])
        for ipcr in B500['B510EP']:
            md.append('+ ***%s***' % trans_ipcr(ipcr))
    if 'B860' in B800:
        md.append('## (86) %s:<br>**%s**' % (labels[86][lang], trans_international_an(B800['B860'])))
    if 'B870' in B800:
        md.append('## (87) %s:<br>**%s**' % (labels[87][lang], trans_international_pn(B800['B870'])))
    md.append('***')
    md.append('## (54)')
    for B540 in B500['B540']:
        if B540['B541'] == patent['attr']['lang']:
            md.append('+ **%s**' % B540['B542'])
        else:
            md.append('+ %s' % B540['B542'])
    md.append('***')
    md.append('## (84) %s:' % labels[84][lang][0])
    md.append('**%s**' % ' '.join(B800['B840']))
    if 'B844EP' in B800:
        md.append('<br>%s:<br>**%s**' % (labels[84][lang][1], ' '.join([x['ctry'] for x in B800['B844EP']['B845EP']])))
    if 'B848EP' in B800:
        md.append('<br>%s:<br>**%s**' % (labels[84][lang][2], ' '.join([x['ctry'] for x in B800['B848EP']['B849EP']])))
    if 'B300' in SDOBI:
        B300 = SDOBI['B300']
        md.append('## (30) %s:' % labels[30][lang])
        for priority in B300:
            md.append('+ **%s %s %s**' % (trans_date(priority['B320']), priority['B330']['ctry'], priority['B310']))
    if 'B600' in SDOBI:
        B600 = SDOBI['B600']
        if 'B620' in B600:
            B620 = B600['B620']['parent']
            md.append('## (62) Document number(s) of the earlier application(s) in accordance with Art. 76 EPC:')
            for pdoc_list in B620['pdoc']:
                for pdoc in pdoc_list:
                    md.append('+ **%s**' % trans_doc(pdoc))
    if 'B270' in B200:
        B270 = B200['B270']
        md.append('## (27) Previously filed application:')
        md.append('+ **%s %s %s**' % (trans_date(B270), B270['ctry'], B270['dnum']['anum']))
    if kind in ['B1', 'B2', 'B3', 'B9']:
        md.append('## (43) %s: **%s**' % (labels[43][lang][kind], trans_4xx(B400['B430'], lang)))
    if 'B600' in SDOBI:
        B600 = SDOBI['B600']
        if 'B620EP' in B600:
            B620EP = B600['B620EP']['parent']
            md.append('## (60) %s:' % labels[60][lang])
            for cdoc_list in B620EP['cdoc']:
                for cdoc in cdoc_list:
                    md.append('+ **%s**' % trans_doc(cdoc))
    if 'B710' in B700:
        md.append('## (71) %s:' % labels[71][lang])
        for applicant in B700['B710']:
            if 'B716EP' in applicant:
                md.append('+ **%s**<br>Designated Contracting States:<br>**%s**' % (trans_name(applicant, False), ' '.join(applicant['B716EP']['ctry'])))
            else:
                md.append('+ **%s**' % trans_name(applicant, False))
    if 'B730' in B700:
        md.append('## (73) %s:' % labels[73][lang])
        for grantee in B700['B730']:
            if 'B736EP' in grantee:
                md.append('+ **%s**<br>Designated Contracting States:<br>**%s**' % (trans_name(grantee, False), ' '.join(grantee['B736EP']['ctry'])))
            else:
                md.append('+ **%s**' % trans_name(grantee, False))
    md.append('## (72) %s:' % labels[72][lang])
    for inventor in B700['B720']:
        md.append('+ **%s**' % trans_name(inventor, False).strip())
    if 'B740' in B700:
        md.append('## (74) %s:' % labels[74][lang])
        for agent in B700['B740']:
            md.append('+ **%s**' % trans_name(agent, True))
    if 'B560' in B500:
        B560 = B500['B560']
        md.append('## (56) %s:' % labels[56][lang])
        if 'B561' in B560:
            B561 = B560['B561']
            for patent_citation in B561:
                md.append('1. **%s**' % patent_citation['text'])
        if 'B562' in B560:
            B562 = B560['B562']
            md.append('')
            for patent_citation in B562:
                md.append('+ **%s**' % patent_citation['text'])
    if 'B050EP' in eptags or 'B053EP' in eptags or 'B070EP' in eptags:
        md.append('<br><br><u>%s:</u>' % labels['remarks'][lang])
        if 'B050EP' in eptags:
            for B050EP in eptags['B050EP']:
                md.append('+ %s' % B050EP['B052EP'])
        if 'B053EP' in eptags:
            for B053EP in eptags['B053EP']:
                md.append('+ %s' % B053EP)
        if 'B070EP' in eptags:
            md.append('+ %s' % eptags['B070EP'])
    md.append('***')
    if 'abstract' in patent:
        md.append('(57) ')
        abstract = patent['abstract']
        for abst in abstract:
            for content in abst['content']:
                md.append('%s<br>' % content['content'])
        md.append('***')
    if 'description' in patent:
        md.append('**%s**<br>' % labels['description'][lang])
        description = patent['description']
        for content in description['content']:
            if content['type'] == 'heading':
                md.append('<br>%s<br>' % content['content'])
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
                md.append('1. %s<br><br>' % '<br>'.join(claim['claim_text']).replace('\n', '<br>'))
            if 'amended-claims-statement' in claims:
                amended_claims_statement = claims['amended-claims-statement']
                for item in amended_claims_statement:
                    for claims_statement in item['claims-statement']:
                        for content in claims_statement['content']:
                            if content['type'] == 'heading':
                                md.append('<br><br>**%s**<br><br>' % content['content'])
                            elif content['type'] == 'p':
                                md.append('%s<br>\n' % content['content'])
        md.append('***')
    if 'amended-claims-statement' in patent:
        amended_claims_statement = patent['amended-claims-statement']
        for item in amended_claims_statement:
            for claims_statement in item['claims-statement']:
                for content in claims_statement['content']:
                    if content['type'] == 'heading':
                        md.append('<br><br>**%s**<br><br>' % content['content'])
                    elif content['type'] == 'p':
                        md.append('%s<br>\n' % content['content'])
        md.append('***')
    if 'ep-reference-list' in patent:
        ep_reference_list = patent['ep-reference-list']
        for content in ep_reference_list['content']:
            if content['type'] == 'heading':
                md.append('<br><br>%s<br><br>' % content['content'])
            elif content['type'] == 'p':
                md.append('%s<br>' % content['content'])
    return '\n'.join(md)
