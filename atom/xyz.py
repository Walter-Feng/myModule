import atom


def to_xyz(atom_list):
    string = str(len(atom_list)) + "\n\n"

    string += atom.atoms_to_string_template(atom_list)

    return string


def write_to_xyz(f, atom_list):
    with open(f, "w") as file:
        file.write(to_xyz(atom_list))