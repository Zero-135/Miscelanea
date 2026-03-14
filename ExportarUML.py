import os
import re

# -------------------------
# Regex
# -------------------------

class_pattern = re.compile(r'^\s*class\s+([\w:]+)(?:\s*<\s*([\w:]+))?')
module_pattern = re.compile(r'^\s*module\s+([\w:]+)')
def_pattern = re.compile(r'^\s*def\s+([a-zA-Z0-9_!?=]+)\s*(\([^\)]*\))?')
#def_pattern = re.compile(r'^\s*def\s+([a-zA-Z0-9_!?=]+)') Antiguo
attr_pattern = re.compile(r'^\s*attr_(reader|accessor|writer)\s+(.+)')
instance_var_pattern = re.compile(r'@(\w+)')

# -------------------------
# Estructura de datos
# -------------------------

classes = {}
inheritance = []


def ensure_class(name):
    if name not in classes:
        classes[name] = {
            "methods": set(),
            "attributes": set()
        }


# -------------------------
# Parser Ruby
# -------------------------
def parse_ruby_file(filepath):
    current_class = None
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            class_match = class_pattern.match(line)
            module_match = module_pattern.match(line)
            def_match = def_pattern.match(line)
            attr_match = attr_pattern.match(line)

            # -------- class --------
            if class_match:
                class_name = class_match.group(1)
                parent = class_match.group(2)
                current_class = class_name
                ensure_class(class_name)
                if parent:
                    inheritance.append((class_name, parent))
            # -------- module --------
            elif module_match:
                module_name = module_match.group(1)
                current_class = module_name
                ensure_class(module_name)
            # -------- def --------
            elif def_match and current_class:
                method_name = def_match.group(1)
                args = def_match.group(2) or "()"
                classes[current_class]["methods"].add(
                    f"{method_name}{args}"
                )
            #Antiguo
            #elif def_match and current_class:
            #    method = def_match.group(1)
            #    classes[current_class]["methods"].add(method)
            # -------- attr_reader etc --------
            elif attr_match and current_class:
                attrs = re.findall(r':(\w+)', attr_match.group(2))
                for attr in attrs:
                    classes[current_class]["attributes"].add(attr)
            # -------- instance variables --------
            elif current_class:
                vars_found = instance_var_pattern.findall(line)
                for v in vars_found:
                    classes[current_class]["attributes"].add(v)


# -------------------------
# Escanear carpeta
# -------------------------
def scan_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".rb"):
                filepath = os.path.join(root, file)
                parse_ruby_file(filepath)


# -------------------------
# Generar PlantUML
# -------------------------
def generate_plantuml(output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("@startuml\n\n")
        f.write("skinparam classAttributeIconSize 0\n\n")

        for cls, data in classes.items():
            f.write(f"class {cls} {{\n")
            for attr in sorted(data["attributes"]):
                f.write(f"  +{attr}\n")
            if data["attributes"] and data["methods"]:
                f.write("  --\n")
            for method in sorted(data["methods"]):
                f.write(f"  {method}\n")
            f.write("}\n\n")

        for child, parent in inheritance:
            f.write(f"{parent} <|-- {child}\n")
        f.write("\n@enduml\n")


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    ruta_scripts = r"C:\Users\Walter Rivas\Documents\PokeProject V4\Data\Scripts"   # cambia aquí si tu carpeta se llama distinto
    scan_directory(ruta_scripts)
    generate_plantuml("pokemon_essentials_uml.puml")
    print("UML generado en: pokemon_essentials_uml.puml")