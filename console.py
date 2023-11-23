#!/usr/bin/python3
""" Console Module """
import cmd
import sys
import re
from models import storage



class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) '
    classes = storage.classes()
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }


    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and isinstance(eval(pline), dict):
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postloop(self) -> None:
        if not sys.__stdin__.isatty():
            print()

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        return True

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        # print()
        return True

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        clsname, kwargs = self.args_parser(args)
        if not clsname:
            print("** class name missing **")
            return
        if clsname not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        new_instance = HBNBCommand.classes[clsname]()
        if kwargs:
            instance_dict = new_instance.to_dict()
            instance_dict.update(kwargs)
            new_instance = HBNBCommand.classes[clsname](**instance_dict)
            objkey = f'{clsname}.{new_instance.id}'
            storage.all()[objkey] = new_instance
        storage.save()
        print(new_instance.id)

    def args_parser(self, args):
        '''parses args for the create method'''
        args = args.split(' ')
        clsname = args[0]
        params = args[1:]

        argsdict = {}
        for item in params:
            if len(item.split('=')) != 2:
                continue
            key = item.split('=')[0]
            val = item.split('=')[1]
            try:
                val = int(val)
            except ValueError:
                try:
                    val = float(val)
                except ValueError:
                    if val.startswith('"') and val.endswith('"'):
                        val = val.strip('"').replace('_', ' ')
                    else:
                        continue
            argsdict[key] = val
        return (clsname, argsdict)

    def do_test(self, line):
        new_instance = State()
        storage.save()
        print(new_instance.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del (storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage._FileStorage__objects.items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, line):
        """
        Updates an instance based on the class name and id by adding\
        or updating attribute (save the change into the JSON file).\
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        """
        args = self.lineparser(line)
        key = self.validate(args)
        if not key:
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if args[2] in ["id", "create_at", "updated_at"]:
            return
        if len(args) < 4:
            print("** value missing **")
            return
        if args[3] is None:
            print("** invalid value **")
            return
        attr = args[2]
        val = args[3]
        objdict = storage.all()[key].to_dict()
        objdict[attr] = val
        inst = HBNBCommand.classes[args[0]](**objdict)
        storage.new(inst)
        storage.save()

    @staticmethod
    def validate(args):
        """validates args and returns the key"""
        if not args:
            print("** class name missing **")
            return None
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return None
        if len(args) < 2:
            print("** instance id missing **")
            return None
        key = f"{args[0]}.{args[1]}"

        if key not in storage.all():
            print("** no instance found **")
            return None

        return key

    @staticmethod
    def lineparser(line, num=-1):
        """Splits the line args and returns a list of them"""
        pattern = re.compile(r"(\d+\.\d+|\d+|\"[^'\"]+?\"|'[^'\"]+?')$")
        if line:
            args = line.split(" ", num)
            if len(args) > 3:
                if re.match(pattern, args[3]):
                    val = args[3].strip("\'\"")
                    if val.isdigit():
                        args[3] = int(val)
                    else:
                        try:
                            args[3] = float(val)
                        except ValueError:
                            args[3] = str(val)
                else:
                    args[3] = None
            return args
        return None

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
