"""modules imports
"""
import pandas as pd

class generic_helper:
    """generic tools
    """

    def coordinates_validator(self, coordinates: list, projection_system: str = '4326'):
        """to validate coordinates, according to projection system
        @return: list
        """
        if len(coordinates) != 2:
            raise ValueError("Coordinates list must be of size 2") from None
        coordinates[0] = float(coordinates[0])
        coordinates[1] = float(coordinates[1])
        if projection_system == '4326' and float(coordinates[1]) >= 1 \
                    and float(coordinates[1]) <= 4 and float(coordinates[0]) >= 45 \
                    and float(coordinates[0]) <= 52:
            tmp = coordinates[0]
            coordinates[0] = coordinates[1]
            coordinates[1] = tmp

        if projection_system == '4326' and (float(coordinates[0]) < 1 or float(coordinates[0]) > 4):
            raise ValueError(str(coordinates[0]) + " : longitude must have a value between 1 \
                        and 4") from None

        if projection_system == '4326' \
                    and (float(coordinates[1]) < 45 or float(coordinates[1]) > 52):
            raise ValueError(str(coordinates[2]) + " : latitude must have a value between 45 \
                        and 52") from None

        return coordinates

    def str_to_list(self, str_list: str):
        """removes quotes and spaces in a string list, and split it in a list
        @return: list
        """
        if str_list == "":
            return []

        return str_list\
            .replace(" ", "")\
            .replace("'", "")\
            .replace('"','')\
            .split(',')

    def get_zone_attributes(self, zone_type: str, has_geometry: bool = True):
        """get zone attributes
        @return: string
        """
        select = ""
        group_by = ""
        directions: list = ["start", "end"]
        for direction in directions:
            select = select + \
                        f", \"{direction}\".{zone_type}_id {zone_type}_{direction}_id, \
                        \"{direction}\".{zone_type}_name {zone_type}_{direction}_name"
            group_by =  group_by + \
                        f", \"{direction}\".{zone_type}_id, \"{direction}\".{zone_type}_name"
            if zone_type == "iris":
                select = select + \
                            f", \"{direction}\".city_id city_{direction}_id, \
                            unaccent(\"{direction}\".city_name) city_{direction}_name"
                group_by = group_by + \
                            f", \"{direction}\".city_id, unaccent(\"{direction}\".city_name)"
            if zone_type == "city":
                select = select + \
                        f", \"{direction}\".department_id department_{direction}_id"
                group_by = group_by + f", \"{direction}\".department_id"
            if has_geometry:
                select = select + f", st_union(\"{direction}\".geometry) {zone_type}_{direction}_geometry"

        return [select, group_by]

    def get_day_types_id_from_name(self, day_type_list: list):
        """get list of day types ids from day names
        0 is Sunday, 6 is Saturday
        @return: string
        """
        day_types: list = []

        for day_type in day_type_list:
            if day_type == "sunday":
                day_types.append(0)
            elif day_type == "monday":
                day_types.append(1)
            elif day_type == "tuesday":
                day_types.append(2)
            elif day_type == "wednesday":
                day_types.append(3)
            elif day_type == "thursday":
                day_types.append(4)
            elif day_type == "friday":
                day_types.append(5)
            elif day_type == "saturday":
                day_types.append(6)
        return day_types

    def get_day_types_name_from_id(self, day_type_list: list):
        """get list of days from day ids
        0 is Sunday, 6 is Saturday
        @return: string
        """
        day_types: list = []

        for day_type in day_type_list:
            day_type = int(day_type)
            if day_type == 0:
                day_types.append("sunday")
            elif day_type == 1:
                day_types.append("monday")
            elif day_type == 2:
                day_types.append("tuesday")
            elif day_type == 3:
                day_types.append("wednesday")
            elif day_type == 4:
                day_types.append("thursday")
            elif day_type == 5:
                day_types.append("friday")
            elif day_type == 6:
                day_types.append("saturday")
        return day_types

    def str_to_dataframe(self, string: str, separator: str = ';',
                         line_end = '\n', set_header = True):
        """transform str to datafram
        @return: DataFrame
        """
        dat = [x.split(separator) for x in string.split(line_end)][1:-1]
        df = pd.DataFrame(dat)
        if set_header:
            df = df.T.set_index(0, drop = True).T # flip, set ix, flip back
        return df
