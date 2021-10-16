import time
from xml.etree import ElementTree


def my_time():
    week = {0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"}
    time_tuple = time.localtime()  # получить struct_time
    weekday = week[time_tuple[6]]
    date_ = time.strftime("%d.%m.%Y", time_tuple)
    time_ = time.strftime("%H:%M", time_tuple)
    date_tuple = (date_, weekday, time_)
    return date_tuple


def task(id_, place, f_name, description, file='incidents.xml'):
    incident_id = {0: "Commission",
                   1: "Wild animals",
                   2: "Bandits",
                   3: "Abyss Mage",
                   4: "The Fatui",
                   5: "Anomaly"
                   }
    n = 0

    tree = ElementTree.parse(file)
    root = tree.getroot()
    for ids in root:
        n = int(ids.attrib['id'])

    id_tag = ElementTree.SubElement(root, 'id')
    id_tag.attrib['id'] = str(n+1)

    status_tag = ElementTree.SubElement(id_tag, 'status')
    status_tag.text = '0'
    type_tag = ElementTree.SubElement(id_tag, 'type')
    type_tag.attrib = {"type": str(id_)}
    date1_tag = ElementTree.SubElement(type_tag, 'date')
    date1_tag.text = ' '.join(my_time())
    place_tag = ElementTree.SubElement(type_tag, 'place')
    place_tag.text = place
    from_tag = ElementTree.SubElement(type_tag, 'from_name')
    from_tag.text = f_name
    desc_tag = ElementTree.SubElement(type_tag, 'description')
    desc_tag.text = description

    report_tag = ElementTree.SubElement(id_tag, 'report')
    date2_tag = ElementTree.SubElement(report_tag, 'date')
    date2_tag.text = ' '
    knight_tag = ElementTree.SubElement(report_tag, 'knight')
    knight_tag.text = ' '
    desc_tag = ElementTree.SubElement(report_tag, 'description')
    desc_tag.text = ' '

    tree.write(file)

    return id_tag.text


def missions(status, file='incidents.xml'):
    incident_id = {'0': "Commission",
                   '1': "Wild animals",
                   '2': "Bandits",
                   '3': "Abyss mages",
                   '4': "The Fatui",
                   '5': "Anomaly",
                   }
    status_id = {'0': "Not complete",
                 '1': "Complete",
                 '2': "Need support"}
    missions_list = {}
    tree = ElementTree.parse(file)
    root = tree.getroot()
    all_ = False
    if int(status) == 3:
        all_ = True
    for ids in root:
        if ids[0].text == str(status) or all_ is True:
            index = ids.attrib["id"]
            missions_list[index] = [ids[0].text, ids[1].attrib['type'], [], []]
            for string in ids[1]:
                missions_list[index][2].append(string.text)
            for rep in ids[2]:
                missions_list[index][3].append(rep.text)
    if len(missions_list) == 0:
        missions_list['0'] = 'empty'
    else:
        for key in missions_list:
            missions_list[key][0] = status_id[missions_list[key][0]]
            missions_list[key][1] = incident_id[missions_list[key][1]]

    return missions_list


def report(id_, status, login_, description, file='incidents.xml', k_file='knights.xml'):
    nametree = ElementTree.parse(k_file)
    names = nametree.getroot()
    k_name = ''
    for ids in names:
        if ids.attrib['id'] == str(login_):
            k_name = ids[0].text

    tree = ElementTree.parse(file)
    root = tree.getroot()

    index = int(id_) - 1

    rep = root[index]
    rep[0].text = str(status)               # status
                                            # report
    rep[2][0].text = ' '.join(my_time())    # date
    rep[2][1].text = k_name                 # knight
    rep[2][2].text = description            # description

    tree.write("incidents.xml")
    print('Mission {} report update. {}'.format(id_, k_name))
    return k_name


def check(id_, file='incidents.xml'):
    tree = ElementTree.parse(file)
    root = tree.getroot()
    n = -1
    id_ = int(id_)
    for ids in root:
        n = int(ids.attrib['id'])
    if id_ > n:
        status_ = 'ID does not exist.'
        return status_
    index = id_ - 1
    rep = root[index]
    if rep[0].text == '1':
        status_ = 'Done.'
    else:
        status_ = 'In progress.'
    return status_


def login(email, password, file='knights.xml'):
    logged = 'Incorrect email or password.'
    tree = ElementTree.parse(file)
    knights = tree.getroot()
    for ids in knights:
        if ids.attrib['email'].lower() == email.lower():
            if ids.attrib['password'] == password:
                logged = ids.attrib['id']
            else:
                logged = False
    return logged


def registration(email, password, rank=0, file='knights.xml'):
    login = ''
    tree = ElementTree.parse(file)
    knights = tree.getroot()
    for ids in knights:
        n = ids.attrib['id']
        login = int(n) + 1

    id_tag = ElementTree.SubElement(knights, 'id')
    id_tag.attrib = {'id': str(login),
                     'email': email,
                     'password': password,
                     'rank': rank}
    tree.write(file)
    return login


def new_account(login, profile, file='knights.xml'):
    tree = ElementTree.parse(file)
    knights = tree.getroot()
    for ids in knights:
        if ids.attrib['id'] == str(login):
            for key in profile:
                if key != 'surname':
                    tag = ElementTree.SubElement(ids, key)
                    tag.text = profile[key]
                tree.write(file)
    for ids in knights:
        if ids.attrib['id'] == str(login):
            if profile['surname'] != '':
                ids[0].attrib['surname'] = profile['surname']
                tree.write(file)


def edit_account(login, rank, profile, file='knights.xml'):
    tree = ElementTree.parse(file)
    knights = tree.getroot()

    return None


def account(login, file='knights.xml'):
    profile = {'rank': '',
               'name': '',
               'surname': '',
               'sex': '',
               'birthday': '',
               'post': '',
               'vision': '',
               'weapon': '',
               'description': '',
               'namepic': '',
               'visionpic': ''
               }
    tree = ElementTree.parse(file)
    knights = tree.getroot()
    for ids in knights:
        if ids.attrib['id'] == str(login):
            profile['rank'] = ids.attrib['rank']
            for key in profile:
                for i in range(len(ids)):
                    if ids[i].tag == key:
                        profile[key] = ids[i].text
                        if ids[i].attrib:
                            profile['surname'] = ids[i].attrib['surname']

    try:
        with open('static/img/' + profile['namepic']) as pic:
            pass
    except FileNotFoundError:
        profile['namepic'] = str('img/unknown.png')
    else:
        profile['namepic'] = str('img/' + profile['namepic'])

    if profile['vision'] == 'None':
        profile['visionpic'] = 'img/Element_unknown.png'
    else:
        profile['visionpic'] = str('img/Element_' + profile['vision'] + '.png')

    return profile


def get_rank(login, file='knights.xml'):
    tree = ElementTree.parse(file)
    knights = tree.getroot()
    rank = '0'
    for ids in knights:
        if ids.attrib['id'] == str(login):
            rank = ids.attrib['rank']
    return rank


if __name__ == '__main__':
    aaa = 'Cyberpunk 2077'
    # print(' '.join(my_time()))
    # print(registration('Ether@monstadt.tw', 'Lum1ne'))
    # profile = {'name': 'Lumine',
    #            'surname': '',
    #            'sex': 'Female',
    #            'birthday': 'September 7th',
    #            'post': 'Honorary Knight',
    #            'vision': 'None',
    #            'weapon': 'Sword',
    #            'description': ''}

    # new_account(12, profile)


    # print(task(5, 'Monstadt', 'Fischl', 'Strange anomaly in Cape Oath'))
    # print()
    # print(report(2, 2, 3, 'Enemies number is 8. Need support.'))
    #
    # m = missions('2')
    #
    # for i in m:
    #     print('{' + i + ': ', m[i], '}', sep='')

    # def avatar():
    #     tree = ElementTree.parse('knights.xml')
    #     root = tree.getroot()
    #
    #     for ids in root:
    #         name = ids[0].text
    #         print(name)
    #         namepic_tag = ElementTree.SubElement(ids, 'namepic')
    #         namepic_tag.text = str(name + '.png')
    #         print(namepic_tag.text)
    #
    #         tree.write('knights.xml')
    #
    #
    # avatar()

    # print(account(4))
