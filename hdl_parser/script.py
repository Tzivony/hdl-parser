import hdlparse.vhdl_parser as vhdl
from hdlparse.vhdl_parser import VhdlComponent


def main():
    vhdl_comps = parse_vhdl('./examples/vhdl_example.vhd')
    
    inst_in_vlog(vhdl_comps[0], './examples/out.v')


"""
Creates a list of objects representing components(modules) found in a vhdl file
"""
def parse_vhdl(filepath):
    vhdl_ex = vhdl.VhdlExtractor()
    vhdl_comps = vhdl_ex.extract_objects(filepath, VhdlComponent)

    return vhdl_comps


"""
Creates a verilog module instanciation from a vhdl component
"""
def inst_in_vlog(component, filepath):
    module_name = component.name + "_wrapper"
    inst_name =  module_name + "_i"
    param_string = ""
    ports_string = ""
    
    if len(component.generics) == 0:
        param_string = " "

    elif len(component.generics) == 1:
        generic = component.generics[0]
        param_string = " #(.%s(%s)) " % (generic.name, generic.name)
        
    else:
        param_string = " #(\n"
        
        for generic in component.generics:
            param_string += "\t.%s(%s),\n" % (generic.name, generic.name)
        
        param_string = param_string[:-2] # Cutting last ",\n"
        param_string += "\n) "
    
    
    if len(component.ports) == 0:
        raise Exception("Module has no ports")

    elif len(component.generics) == len(component.ports) == 1:
        port = component.ports[0]
        ports_string = " (.%s(%s));" % (port.name, port.name)
    
    else:
        ports_string = " (\n"
        
        for port in component.ports:
            ports_string += "\t.%s(%s),\n" % (port.name, port.name)
        
        ports_string = ports_string[:-2] # Cutting last ",\n"
        ports_string += "\n);"
    
    
    buffer = module_name + param_string + inst_name + ports_string
    
    with open(filepath, "w") as file:
        file.write(buffer)

    
def print_vhdl(component):
    print('Component "{}":'.format(component.name))

    print('  Generics:')
    for p in component.generics:
        print('\t{:20}{:8} {}'.format(p.name, p.mode, p.data_type))

    print('  Ports:')
    for p in component.ports:
        print('\t{:20}{:8} {}'.format(p.name, p.mode, p.data_type ))


if __name__ == '__main__':
    main()