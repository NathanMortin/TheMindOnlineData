import xmltodict


class Analyzer:
    def __init__(self, xml_file_name):
        self.xml_file_name = xml_file_name
        self.xml_dict = {}

    def interpretation(self):
        with open(self.xml_file_name, 'r', encoding='utf-8') as file:
            xml_data = file.read()
        xml_dict = xmltodict.parse(xml_data)
        new_xml_dict = self.xml_dict_pars(xml_dict)
        self.set_xml_dict(new_xml_dict)

    def set_xml_dict(self, xml_dict):
        self.xml_dict = xml_dict

    def get_xml_dict(self):
        return self.xml_dict

    def xml_dict_pars(self, var):

        if type(var) == list:
            new_var = []
            for item in var:
                new_var.append(self.xml_dict_pars(item))
            return new_var

        if type(var) != dict:
            return var

        new_var = {}
        var_type = "dict"
        for key in var:
            if key == "@type":
                var_type = var[key]
                continue

            value = self.xml_dict_pars(var[key])
            if var_type == "dict":
                new_var[key] = value
            elif var_type == "bool":
                if value == "True":
                    return True
                else:
                    return False
            elif var_type == "str":
                return str(value)
            elif var_type == "int":
                return int(value)
            elif var_type == "float":
                return float(value)
            elif var_type == "list":
                if type(value) == list:
                    return value
                else:
                    return [value]
            else:
                new_var[key] = value

        return new_var


game_analyzer = Analyzer("May-18-2022_17-06-49.xml")
game_analyzer.interpretation()


