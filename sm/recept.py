
def ingredstr_to_list_dict(ingred_str: str):
    ingredients = ingred_str.split('\n')

    ingred_kbd=[]
    ingred_list=[]
    ingred_dict = {}

    for ingr in ingredients:
        ingr_list=ingr.split(' - ')
        ingr_list_list = ingr_list[1].split(' ')

        if '/' in ingr_list_list[0]:
            ii_list = ingr_list_list[0].split('/')
            ii_float = float(ii_list[0]) / float(ii_list[1])
            ingr_list_list[0] = str(ii_float)

        elif ',' in ingr_list_list[0]:
            ii_list = ingr_list_list[0].split(',')
            ii_float = float(ii_list[0]) + float(ii_list[1])/10
            ingr_list_list[0] = str(ii_float)

        elif not ingr_list_list[0].isnumeric():
            #ingr_list_list[0] = 0
            ingr_list_list.insert(0,0)

        ingred_dict[ingr_list[0]] = ingr_list_list
        ingred_kbd.append([ingr_list[0]])
        ingred_list.append(ingr_list[0])

    return ingred_dict, ingred_list, ingred_kbd





def dict_to_str(ingred_dict, coef) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {float(value[0]):.1f} - {float(value[0])*coef:.1f}   {' '.join(value[1:])}" for key, value in ingred_dict.items()]
    return "\n".join(facts).join(["\n", "\n"])


def dict_to_str_start(ingred_dict) -> str:
    """Helper function for formatting the gathered user info."""

    facts = [f"{key} - {float(value[0]):.1f}  {' '.join(value[1:])}" for key, value in ingred_dict.items()]
    return "\n".join(facts).join(["\n", "\n"])








