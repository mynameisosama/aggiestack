from . import admin

def checkRackCache(_rk, _image_name):
    if _image_name not in _rk["images"]:
        return False
    return True
    
def cacheImage(_rk, _image, _image_name):
    _rk['space-available'] = str(
        int(_rk['space-available']) - int(_image['size'])
    )
    if _image_name not in _rk["images"]:
        _rk["images"].append(_image_name)

def deleteInstance(hw_dict, fl_dict, vm_dict, instance):
    _fl = fl_dict[vm_dict[instance]["flavor"]]
    _hw = hw_dict[vm_dict[instance]["machine"]]
    _hw["mem"] = str(
        int(_hw["mem"]) + int(_fl["mem"])
    )
    _hw["num-disks"] = str(
        int(_hw["num-disks"]) + int(_fl["num-disks"])
    )
    _hw["num-vcpus"] = str(
        int(_hw["num-vcpus"]) + int(_fl["num-vcpus"])
    )
    vm_dict.pop(instance) 


def migrateInstance(im_dict, rk_dict, hw_dict, fl_dict, vm_dict, instance):
    __bad_rack = vm_dict[instance]["rack"]
    __candidate_machines = dict()
    for __machine in hw_dict:
        if not hw_dict[__machine]["rack"] == __bad_rack:
            __candidate_machines[__machine] = hw_dict[__machine]
    _vm = lambda: None
    setattr(_vm, "name", instance)
    setattr(_vm, "image", vm_dict[instance]["image"])
    setattr(_vm, "flavor", vm_dict[instance]["flavor"])
    deleteInstance(hw_dict, fl_dict, vm_dict, instance)
    createInstance(rk_dict, __candidate_machines, fl_dict, im_dict, vm_dict, _vm)


def createInstance(rk_dict, hw_dict, fl_dict, im_dict, vm_dict, instance):
    def spawnInstance(_hw, _fl):
        _hw["mem"] = str(
            int(_hw["mem"]) - int(_fl["mem"])
        )
        _hw["num-disks"] = str(
            int(_hw["num-disks"]) - int(_fl["num-disks"])
        )
        _hw["num-vcpus"] = str(
            int(_hw["num-vcpus"]) - int(_fl["num-vcpus"])
        )

    for __machine in hw_dict:
        __canSpawn = admin.canSpawn(
            hw_dict[__machine], fl_dict[instance.flavor]
        )
        if(__canSpawn == "Yes"):
            spawnInstance(hw_dict[__machine], fl_dict[instance.flavor])
            if(
                not checkRackCache(
                    rk_dict[hw_dict[__machine]['rack']], instance.image
                )
            ):
                cacheImage(
                    rk_dict[hw_dict[__machine]['rack']],
                    im_dict[instance.image],
                    instance.image
                )
            vm_dict[instance.name] = {
                "machine": __machine,
                "rack": hw_dict[__machine]['rack'],
                "image": instance.image,
                "flavor": instance.flavor
            }
            break
    else:
        raise AssertionError(
            "No candidate machine found for %s" % instance.name
        )
