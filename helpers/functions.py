import argparse
import shelve
import copy
import os
from .constants import DISPLAY_WIDTH


def parseArguements():
    __parser = argparse.ArgumentParser(
        prog='aggiestack',
        description='%s - %s' % (
            'AggieStack CLI',
            'A command line interface to manage virtual servers'
        )
    )
    __subparsers = __parser.add_subparsers(
        dest="cmd", help="types of commands"
    )

    # Create server subparser
    __parser_server = __subparsers.add_parser(
        "server",
        help="manipulate virtual instances"
    )
    __subparsers_server = __parser_server.add_subparsers(
        dest="action", help="create, delete or list server"
    )

    # Create server create subparser
    __parser_server_create = __subparsers_server.add_parser(
        "create",
        help="create a virtual instance"
    )
    __parser_server_create.add_argument(
        "--image", type=str, required=True,
        help="image for virtual instance"
    )
    __parser_server_create.add_argument(
        "--flavor", type=str, required=True,
        help="flavor for virtual instance"
    )
    __parser_server_create.add_argument(
        "name", type=str,
        help="name for virtual instance"
    )

    # Create server delete subparser
    __parser_server_delete = __subparsers_server.add_parser(
        "delete",
        help="delete a virtual instance"
    )
    __parser_server_delete.add_argument(
        "name", type=str,
        help="name for virtual instance"
    )

    # Create server list subparser
    __parser_server_list = __subparsers_server.add_parser(
        "list",
        help="list all virtual instances"
    )

    # Create admin subparser
    __parser_admin = __subparsers.add_parser(
        "admin",
        help="run aggiestack in admin mode"
    )
    __subparsers_admin = __parser_admin.add_subparsers(dest="action")

    # Create admin show subparser
    __parser_admin_show = __subparsers_admin.add_parser(
        "show",
        help="list information about datacenter"
    )
    __parser_admin_show.add_argument(
        "element", type=str, choices=["hardware", "instances", "imagecaches"]
    )
    __parser_admin_show.add_argument(
        "rack", type=str, nargs="?"
    )

    # Create admin can_host subparser
    __parser_admin_can_host = __subparsers_admin.add_parser(
        "can_host",
        help="check whether a {flavor} server can spawned on {machine}"
    )
    __parser_admin_can_host.add_argument("machine", type=str)
    __parser_admin_can_host.add_argument("flavor", type=str)

    # Create admin evacuate subparser
    __parser_admin_evacuate = __subparsers_admin.add_parser(
        "evacuate",
        help="remove all machines from a rack {rack}"
    )
    __parser_admin_evacuate.add_argument("rack", type=str)

    # Create admin remove subparser
    __parser_admin_remove = __subparsers_admin.add_parser(
        "remove",
        help="remove machine {machine}"
    )
    __parser_admin_remove.add_argument("machine", type=str)

    # Create admin add subparser
    __parser_admin_add = __subparsers_admin.add_parser(
        "add",
        help="add machine {machine} to rack"
    )
    __parser_admin_add.add_argument("--mem", type=str)
    __parser_admin_add.add_argument("--disk", type=str)
    __parser_admin_add.add_argument("--vcpus", type=str)
    __parser_admin_add.add_argument("-ip", type=str)
    __parser_admin_add.add_argument("-rack", type=str)
    __parser_admin_add.add_argument("machine", type=str)

    # Create show subparser
    __parser_show = __subparsers.add_parser(
        "show",
        help="list information about datacenter"
    )
    __parser_show.add_argument(
        "element", type=str, choices=["hardware", "flavors", "images", "all"]
    )

    # Create config subparser
    __parser_config = __subparsers.add_parser(
        "config",
        help="configure datacenter"
    )
    __parser_config.add_argument(
        "--hardware", type=str,
        help="path of hardware config file"
    )
    __parser_config.add_argument(
        "--flavors", type=str,
        help="path of flavor config file"
    )
    __parser_config.add_argument(
        "--images", type=str,
        help="path of image config file"
    )

    return __parser.parse_args()


def displayData(_dict, _type, _format):
    if(not _dict):
        if(_type == "instance"):
            raise AssertionError("No instances found.")
        raise AssertionError(
            "No %s information found. Run config --%s" % (
                _type, _type
            )
        )
    __data = list()
    __data.append("Displaying %s Information" % _type.title())
    __header = "{:<{width}}".format(
        "name", width=DISPLAY_WIDTH
    )
    for __heading in _format:
        __header += "{:<{width}}".format(
            __heading, width=DISPLAY_WIDTH
        )
    __data.append(__header)
    try:
        for __key in _dict:
            __temp = "{:<{width}}".format(
                __key, width=DISPLAY_WIDTH
            )
            for __sub_key in _dict[__key]:
                if(type(_dict[__key][__sub_key]) is list):
                    __temp += "{:<{width}}".format(
                        ",".join(_dict[__key][__sub_key]),
                        width=DISPLAY_WIDTH
                    )
                else:
                    __temp += "{:<{width}}".format(
                        _dict[__key][__sub_key], width=DISPLAY_WIDTH
                    )
            __data.append(__temp)
    except KeyError as __err:
        raise __err
    return "\n".join(__data)


def getData(_key):
    __path = os.getcwd()
    try:
        os.chdir('data')
    except (WindowsError, OSError) as __err:
        raise Exception("'data' folder not found") from __err
    __data = shelve.open('data')
    try:
        __temp = copy.deepcopy(__data[_key])
    except KeyError:
        __temp = dict()
    __data.close()
    os.chdir(__path)
    return __temp


def storeData(_dict, _key):
    __path = os.getcwd()
    try:
        os.chdir('data')
    except (WindowsError, OSError) as __err:
        raise Exception("'data' folder not found") from __err
    __data = shelve.open('data')
    try:
        __data[_key] = _dict
    except KeyError as __err:
        raise __err
    __data.close()
    os.chdir(__path)

