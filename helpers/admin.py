from . import server


def canSpawn(_hw, _fl):
    try:
        if(int(_fl["mem"]) <= int(_hw["mem"])):
            if(int(_fl["num-disks"]) <= int(_hw["num-disks"])):
                if(int(_fl["num-vcpus"]) <= int(_hw["num-vcpus"])):
                    return "Yes"
        return "No"
    except KeyError as __err:
        raise __err


def evacuateMachine(_im_dict, _rk_dict, _vm_dict, _hw_dict, _fl_dict, _machine):
    __hw_instances = filter(
        lambda x: _vm_dict[x]["machine"] == _machine,
        [__vm for __vm in _vm_dict]
    )
    for __vm in __hw_instances:
        server.migrateInstance(_im_dict, _rk_dict, _hw_dict, _fl_dict, _vm_dict, __vm)
    _hw_dict.pop(_machine)


def evacuateRack(_rk_name, _rk_dict, _hw_dict, _vm_dict, _im_dict, _fl_dict):
    __rk_machines = filter(
        lambda x: _hw_dict[x]["rack"] == _rk_name,
        [__machine for __machine in _hw_dict]
    )
    for __machine in __rk_machines:
        evacuateMachine(_im_dict, _rk_dict, _vm_dict, _hw_dict, _fl_dict, __machine)
    for __im in _im_dict:
        if __im in _rk_dict[_rk_name]["images"]:
            _rk_dict[_rk_name]["space-available"] = str(
                int(_rk_dict[_rk_name]["space-available"]) + int(
                    _im_dict[__im]["size"]
                )
            )
    _rk_dict[_rk_name]["images"] = list()


def addMachine(_hw_dict, _machine):
    _hw_dict[_machine.machine] = {
        "rack": _machine.rack,
        "ip": _machine.ip,
        "mem": _machine.mem,
        "num-disks": _machine.disk,
        "num-vcpus": _machine.vcpus
    }


def removeMachine(_hw_dict, _vm_dict, _machine):
    for _vm in _vm_dict:
        if _machine == _vm_dict[_vm]["machine"]:
            raise AssertionError(
                "Cannot remove machine it has instances running on it."
            )
    _hw_dict.pop(_machine)
