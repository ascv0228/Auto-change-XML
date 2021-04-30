# output string, while is indented to the format of XML 
def xmlAutoIndent(xml_string_list):
    Indent = 0
    output_string_list = []
    output_string =''
    for i in xml_string_list:
        if '\n' in i:
            print('Error : No reset xml string')
            return False
        if i[len(i)-2:] == '/>':
            output_string_list.append([i+'\n', Indent])
        elif i[0:2] == '</' and i[len(i)-1:] == '>':
            Indent -= 1
            if i != xml_string_list[-1]:
                output_string_list.append([i+'\n', Indent])
            else:
                output_string_list.append([i, Indent])
        elif i[0:2] == '<?' and i[len(i)-2:] == '?>':
            output_string_list.append([i, Indent])
        elif i[0] == '<' and i[len(i)-1:] == '>':
            output_string_list.append([i+'\n', Indent])
            Indent += 1
    for item in output_string_list:
        output_string += '    '*item[1] + item[0]
    return output_string

# get all position of substring in string
def find_all(string, substring):
    idx = string.find(substring)
    while idx != -1:
        yield idx
        idx = string.find(substring, idx + 1)

# get a string-list, which a string is partitioned into by keyword and front_or_behind
def reset_str(string, keyword = '<', front_or_behind = 'front'):
    pos_list = list(find_all(string, keyword))
    part_list = []
    if front_or_behind in ['behind', 'Behind', 'BEHIND']:
        pos_list.insert(0,-1)
        for num in range(len(pos_list)-1):
            part_list.append(string[pos_list[num]+1:pos_list[num+1]+1])
    else:
        if front_or_behind not in ['front', 'Front', 'FRONT']:
            print('Error : Wrong Parameter >>> front_or_behind reset to front')
            front_or_behind = 'front'
        print(len(string))
        pos_list.append(len(string))
        print(len(pos_list))
        for num in range(len(pos_list)-1):
            part_list.append(string[pos_list[num]:pos_list[num+1]])
    return part_list

# get a complete string-list by a orginial string-list, keyword and front_or_behind
def reset_str_list(string_list, keyword = '<', front_or_behind = 'front'):
    tmp_str_list = []
    for elem in string_list:
        if elem.count(keyword) == 1:
            tmp_str_list.append(elem)
            continue
        else :
            for item in reset_str(elem, keyword, front_or_behind):
                tmp_str_list.append(item)
    return tmp_str_list

class XmlFileHandling:
    filename_read = r'D:/Code/Git/Auto-change-XML/AndroidManifest_org.xml'
    filename_write = r'D:/Code/Git/Auto-change-XML/test.xml'

    # when the obj built, auto get text from file
    def __init__(self, filename_read=filename_read, filename_write=filename_write):
        self.filename_read = filename_read
        self.filename_write = filename_write
        self.file_read_obj = open(self.filename_read, 'r')
        self.file_write_obj = open(self.filename_write, 'w')
        self.getText(self.file_read_obj)

    # when the obj deleted, auto save text into file
    def __del__(self):
        self.saveXml(self.file_write_obj)
        self.file_read_obj.close()
        self.file_write_obj.close()

    # get all text from file
    def getText(self,fo):
        self.filecontent =[]
        tmp_str_list = fo.read().split('\n')
        if('<?' in tmp_str_list[0] and '?>' in tmp_str_list[0]):
            tmp0_str = tmp_str_list[0][:tmp_str_list[0].find('?>')+2]
            tmp1_str = tmp_str_list[0][tmp_str_list[0].find('?>')+2:]
            tmp_str_list[0] = tmp0_str
            tmp_str_list.insert(1, tmp1_str)
        i = 0
        for elem in tmp_str_list:
            self.filecontent.append(elem.lstrip())

    #save file
    def saveXml(self,fo):
        str2 = self.filecontent
        print(xmlAutoIndent(reset_str_list(str2, '>', 'behind')),file = fo,end = '')

    #get position by string
    def find_small_str(self, find_str):
        idPosition = []
        i = 0
        for line in self.filecontent:
            i+=1
            if (line.find(find_str) != -1):
                idPosition.append(i)
        return idPosition

    #remove small string by position
    def remove_small_str_by_position(self, remove_str, position = None, num = 1):
        if num !=type(1) or num < 1:
            num = 1 
        if position == None:
            position = list(range(len(self.filecontent)))
        elif type(position) == type(1):
            position = [position]
            num = 1
        else:
            position=list(set(position))
            position.sort()
        try:
            tmplist = self.find_small_str(remove_str)
            remove_list = [x for x in tmplist if x in position]
            assert len(remove_list) <= num, \
                f"Error : need remove number {len(remove_list)} > {num}"
        except Exception as err:
            print(err)
        else:
            remove_list.reverse()
            for i in remove_list:
                self.filecontent.pop(i-1)

    #add small string by position
    def add_small_str_by_position(self, add_str, position, up_or_down='down', num = 1):
        if up_or_down in [None,'None']: 
            up_or_down = 'down'
        if num in [None,'None']: 
            num =1
        try:
            assert len(position) >= 1 , 'Error : No Find the find_str'
            assert len(position) <= num , 'Error : More Find the fin_str'
        except Exception as err:
            print(err)
            print('No finish add small string')
            return False
        if up_or_down in ['up','Up','UP']:
            position = [x-1 for x in position ]
        elif up_or_down in ['down','Down','DOWN',None,'None']:
            pass
        else:
            print('Error : Wrong Parameter >>> up_or_down reset to down')
            up_or_down = 'down'
        position.reverse()
        for i in position:
            self.filecontent.insert(i, add_str)
            return True

    #add big string by position
    def add_big_str_by_position(self, add_big_str, position, up_or_down='down', num = 1):
        tmp_list = []
        if up_or_down in ['up','Up','UP']:
            position = [x-1 for x in position ]
        for elem in add_big_str.split('\n'):
            tmp_list.append(elem.lstrip())
        tmp_list.reverse()
        for elem in tmp_list:
            self.add_small_str_by_position(elem, position, num = 1)

# main exec program
def main_exec(obj, add_str_list = None, remove_small_str_list = None):
    if (remove_small_str_list != None):
        for i in remove_small_str_list:
            obj.remove_small_str_by_position(i[0], obj.find_small_str(i[1]), i[2])
#        print('remove_small_str_list')
    if (add_str_list != None):
        for i in add_str_list:
            if i[0].count('\n') ==0:
                obj.add_small_str_by_position(i[0], obj.find_small_str(i[1]), i[2], i[3])
            else:
                obj.add_big_str_by_position(i[0], obj.find_small_str(i[1]), i[2], i[3])
#        print('add_str_list')

if __name__ == "__main__":
    remove_small_str1 = r'<action android:name="android.intent.action.MAIN"/>'
    add_str1 = r'<uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW"/>'
    add_str2 = r'<service android:name="uk.lgl.modmenu.FloatingModMenuService" android:enabled="true" android:exported="false" android:stopWithTask="true"/>'
    add_str3 = r'''<activity android:configChanges="keyboardHidden|orientation|screenSize" android:name="uk.lgl.MainActivity">
         <intent-filter>
             <action android:name="android.intent.action.MAIN"/>
             <category android:name="android.intent.category.LAUNCHER"/>
        </intent-filter>
    </activity>'''



    filename_read = r'D:/Code/Git/Auto-change-XML/AndroidManifest_org.xml'
    filename_write = r'D:/Code/Git/Auto-change-XML/test.xml'

    ## if your line 66 and line 67 finish the file's path, you can build class by "F1 = XmlFileHandling()"
    F1 = XmlFileHandling(filename_read, filename_write)



    ## add_str_list [add_str, string_to_get_position, up_or_down='down', num = 1]
    add_str_list = [[add_str1, '<manifest ','down', None], \
                    [add_str2, '</application>','up', None], \
                    [add_str3, '</application>','up', None]]
    remove_small_str_list = [[remove_small_str1, remove_small_str1, None]]
    main_exec(F1, add_str_list, remove_small_str_list)
    