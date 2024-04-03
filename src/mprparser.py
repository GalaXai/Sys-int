from .mrp import MRP

class MRPparser:
    @staticmethod
    def parse(data: dict) -> list[MRP]:
        objects = {}
        for key, value in data.items():
            
            # check if has lower_level
            if len(value) > 5 and value[5]:
                # check if objects already created
                for obj in value[5]:
                    if obj not in objects:
                        # create it
                        objects[obj] = MRP(obj, *data[obj])
                
                value[5] = [objects[obj] for obj in value[5]]
                obj = MRP(key, *value)
            obj = MRP(key, *value)
            objects[obj.name] = obj
        return objects